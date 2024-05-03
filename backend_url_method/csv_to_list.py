import csv

def csv_to_list(csv_file_path):
    """
    Converts a CSV file to a list of dictionaries where each dictionary represents
    one row of the CSV, with keys being the column headers.

    Parameters:
    - csv_file_path (str): The file path of the CSV file to read.

    Returns:
    - list: A list of dictionaries containing the data from the CSV file.
    """    
    catalogData = []  # Initialize an empty list to store our data
    
    # Open the CSV file in read mode and ensure proper handling of character encoding
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        # Use the csv.DictReader to automatically read the first line as fieldnames
        reader = csv.DictReader(file)
        
        # Iterate over the CSV rows and add each row to the list as a dictionary
        for row in reader:
            catalogData.append(row)
    # Return the list containing all rows of the CSV as dictionaries    
    return catalogData

