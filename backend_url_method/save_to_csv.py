import csv

def save_to_csv(data_list, filename):
    """
    Saves a list of dictionaries to a CSV file. Assumes all dictionaries have the same keys.
    
    Parameters:
    - data_list: List of dictionaries to be saved.
    - filename: Name of the CSV file to save the data to.
    """
    # Check if the data_list is not empty and proceed
    if data_list:
        # Use the keys from the first dictionary as fieldnames
        fieldnames = data_list[0].keys()

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)

        print(f'Data successfully written to {filename}')
    else:
        print("The data list is empty. No file was created.")
