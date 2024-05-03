import csv

def save_to_csv(data_list, filename):
    """
    Saves a list of data to a CSV file. The data can be a list of dictionaries or a list of strings.
    
    Parameters:
    - data_list: List of data (dictionaries or strings) to be saved.
    - filename: Name of the CSV file to save the data to.
    """
    if not data_list:
        print("The data list is empty. No file was created.")
        return

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Check if the first item is a string to determine the write method
        if isinstance(data_list[0], str):
            writer = csv.writer(csvfile)
            for data in data_list:
                writer.writerow([data])  # Wrap data in a list to ensure it's written to one column per row
        elif isinstance(data_list[0], dict):  # Check if the first item is a dictionary
            fieldnames = data_list[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)

    print(f'Data successfully written to {filename}')
