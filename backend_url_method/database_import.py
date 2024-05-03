import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.types import Integer, String, Float, Boolean
import sqlalchemy as sa
from dotenv import load_dotenv
import csv
from io import StringIO
from gemini_REST_schema import gemini_schema
import chardet

def abbreviate_name(long_name):
    """
    Abbreviates a long table name based on predefined mappings to ensure it fits within database name limits.

    Args:
    - long_name (str): The original long name of the table.

    Returns:
    - str: A shorter, abbreviated version of the name capped at 63 characters.
    """
    words = long_name.split('_')
    abbreviations = {
        'institution': 'inst',
        'education': 'edu',
        'enrolment': 'enrl',
        'student': 'stdnt',
        'information': 'info',
        'department': 'dept'
        # Add more abbreviations as needed
    }
    shortened = [abbreviations.get(word, word) for word in words]
    abbreviated_name = '_'.join(shortened)
    return abbreviated_name[:63]  # Ensure the final name is within the PostgreSQL limit


# Detect encoding of the CSV file
def detect_encoding(file_path):
    """
    Detects the encoding of a file using the chardet library.

    Args:
    - file_path (str): The path to the file for which to detect the encoding.

    Returns:
    - str: The detected encoding of the file.
    """
    with open(file_path, 'rb') as file:
        return chardet.detect(file.read())['encoding']

def json_to_sqlalchemy_type(json_type):
    """
    Converts JSON data types to SQLAlchemy column types.

    Args:
    - json_type (str): JSON type as a string.

    Returns:
    - SQLAlchemy type: Corresponding SQLAlchemy data type.
    """
    return {
        'integer': Integer,
        'double': Integer,
        'string': String,
        'float': Float,
        'boolean': Boolean
    }.get(json_type, String)  # Default to String if type unknown

def create_table_from_json(json_schema, engine, table_name):
    """
    Creates a database table from a JSON schema using SQLAlchemy.

    Args:
    - json_schema (dict): Schema of the table in dictionary format.
    - engine (SQLAlchemy Engine): Database engine where the table will be created.
    - table_name (str): Name of the table to create.
    """
    metadata = MetaData()
    columns = [Column(name, json_to_sqlalchemy_type(props['type'])) for name, props in json_schema.items()]
    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine)  # Creates the table
    print(f"Table {table_name} created with schema based on JSON.")


def load_data(csv_path, table_name, engine):
    """
    Loads data from a CSV file into a specified table in the database.

    Args:
    - csv_path (str): Path to the CSV file.
    - table_name (str): Name of the database table.
    - engine: Database engine to use.
    """
    try:
        encoding = detect_encoding(csv_path)
        df_csv = pd.read_csv(csv_path, encoding=encoding)
        df_csv.to_sql(table_name, engine, if_exists='append', index=False)
        print(f"Data successfully loaded into {table_name} from {csv_path}")
    except Exception as e:
        print(f"Failed to load data from {csv_path} into {table_name}: {e}")

def process_json_files(directory, engine):
    """
    Processes all JSON files in a directory to create database tables and load data from corresponding CSV files.
    Each JSON file contains a schema definition, which is used to create a table in the database, and it's expected
    that there's a corresponding CSV file with the actual data to populate the table.

    Args:
    - directory (str): Directory containing the JSON files.
    - engine: Database engine to use for creating tables and loading data.
    """
    import json
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            json_file_path = os.path.join(directory, filename)
            with open(json_file_path, 'r') as file:
                json_text = json.dumps(json.load(file))
            base_name = filename.replace('.json', '')
            table_name = abbreviate_name(base_name.replace('-', '_'))

            # Generate the prompt to analyze JSON text for schema generation
            prompt = f"""
            Analyze this JSON text and provide just the database schema in comma-separated fashion. Expected sample response:
            Field,Type
            xx1, yyy1
            xx2, yyy2

            You can find database schema details given within the "field" parameter with id, name, and type. Please ignore ID and extract the name and type details from here and nothing else.
            Please do not provide any comments from your side. Just return the comma-separated texts.
            """
            # Get schema in CSV format from the API
            csv_schema = gemini_schema(prompt, json_text)
            csv_schema_text = csv_schema['candidates'][0]['content']['parts'][0]['text']

            # Parse the CSV schema text to a dictionary format expected by create_table_from_json
            schema_dict = parse_csv_to_schema(csv_schema_text)

            # Create a table based on the schema
            create_table_from_json(schema_dict, engine, table_name)

            # Assume the corresponding CSV file has the same base name
            csv_path = json_file_path.replace('.json', '.csv')
            if os.path.exists(csv_path):
                load_data(csv_path, table_name, engine)

def parse_csv_to_schema(csv_schema):
    """
    Parses a CSV formatted string to a dictionary schema suitable for creating SQLAlchemy tables.

    Args:
    - csv_schema (str): CSV formatted string representing the table schema.

    Returns:
    - dict: Schema dictionary suitable for use with SQLAlchemy.
    """
    schema = {}
    reader = csv.reader(StringIO(csv_schema))
    for row in reader:
        if row:  # Ensure row is not empty
            schema[row[0]] = {'type': json_to_sqlalchemy_type(row[1].strip().lower())}
    return schema

def read_json_as_text(json_file_path):
    """
    Reads a JSON file and returns its contents as a JSON formatted string.

    Args:
    - json_file_path (str): Path to the JSON file.

    Returns:
    - str: JSON formatted text.
    """
    import json
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    json_text = json.dumps(json_data)
    return json_text


