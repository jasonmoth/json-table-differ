import os
import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, filename='diff_results.log', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_json_files(directory):
    json_files = [file for file in os.listdir(directory) if file.endswith('.json')]
    if not json_files:
        raise FileNotFoundError("No JSON files found in the directory.")
    return json_files

def validate_json_structure(data):
    if not isinstance(data, list):
        return False
    if not all(isinstance(item, dict) for item in data):
        return False
    keys = data[0].keys()
    return all(item.keys() == keys for item in data)

def check_unique_identifier(data, unique_id):
    seen = set()
    for item in data:
        if item[unique_id] in seen:
            return False
        seen.add(item[unique_id])
    return True

def diff_tables(fileA_data, fileB_data, unique_id):
    uniqueA = {item[unique_id] for item in fileA_data}
    uniqueB = {item[unique_id] for item in fileB_data}

    in_A_not_in_B = [item[unique_id] for item in fileA_data if item[unique_id] not in uniqueB]
    in_B_not_in_A = [item[unique_id] for item in fileB_data if item[unique_id] not in uniqueA]

    common_ids = uniqueA.intersection(uniqueB)
    discrepancies = []
    for itemA in fileA_data:
        if itemA[unique_id] in common_ids:
            itemB = next(item for item in fileB_data if item[unique_id] == itemA[unique_id])
            differences = [key for key in itemA if itemA[key] != itemB[key]]
            if differences:
                discrepancies.append({unique_id: itemA[unique_id], 'differences': differences})

    return in_A_not_in_B, in_B_not_in_A, discrepancies

def main():
    print("="*50)
    print("Welcome to the JSON Diff Tool!")
    print("="*50)
    print("This program compares two JSON files in the current directory.")
    print("The JSON files must contain arrays of objects with identical keys.")
    print("You will be asked to select two files and a unique identifier key.")
    print("The program will output:")
    print("  - Unique identifiers of rows in the first file not in the second.")
    print("  - Unique identifiers of rows in the second file not in the first.")
    print("  - Attributes with discrepancies between the common rows.")
    print("Ensure your JSON files are correctly formatted to avoid errors.")
    print("="*50)
    
    directory = '.'
    try:
        json_files = load_json_files(directory)
    except FileNotFoundError as e:
        logging.error(str(e))
        print(str(e))
        return

    print("JSON files found:")
    for i, file in enumerate(json_files):
        print(f"{i + 1}. {file}")

    try:
        fileA_index = int(input("Enter the number of the first file to diff: ")) - 1
        fileB_index = int(input("Enter the number of the second file to diff: ")) - 1

        fileA = json_files[fileA_index]
        fileB = json_files[fileB_index]

        with open(fileA, 'r', encoding='utf-8') as f:
            fileA_data = json.load(f)
        with open(fileB, 'r', encoding='utf-8') as f:
            fileB_data = json.load(f)

        if not (validate_json_structure(fileA_data) and validate_json_structure(fileB_data)):
            logging.error("One or both files are not valid arrays of objects or their schemas do not match.")
            print("One or both files are not valid arrays of objects or their schemas do not match.")
            return

        print(f"Keys in the JSON objects: {list(fileA_data[0].keys())}")
        unique_id = input("Enter the key to use as the unique identifier: ")

        if not (check_unique_identifier(fileA_data, unique_id) and check_unique_identifier(fileB_data, unique_id)):
            logging.error("The unique identifier is not unique in one or both files.")
            print("The unique identifier is not unique in one or both files.")
            return

        in_A_not_in_B, in_B_not_in_A, discrepancies = diff_tables(fileA_data, fileB_data, unique_id)

        # Output to CLI and log
        output_in_A_not_in_B = "\n".join(in_A_not_in_B)
        output_in_B_not_in_A = "\n".join(in_B_not_in_A)
        
        print(f"Rows in {fileA} not in {fileB}: \n" + output_in_A_not_in_B)
        logging.info(f"Rows in {fileA} not in {fileB}: \n" + output_in_A_not_in_B)
        
        print(f"Rows in {fileB} not in {fileA}: \n" + output_in_B_not_in_A)
        logging.info(f"Rows in {fileB} not in {fileA}: \n" + output_in_B_not_in_A)
        
        if discrepancies:
            for discrepancy in discrepancies:
                discrepancy_message = f"Discrepancies in record {discrepancy[unique_id]}: {', '.join(discrepancy['differences'])}"
                print(discrepancy_message)
                logging.info(discrepancy_message)
        else:
            print("No discrepancies found between the two files.")
            logging.info("No discrepancies found between the two files.")

        print(f"Differences have been logged to diff_results.log")

    except (IndexError, ValueError) as e:
        logging.error("Invalid input or error processing files.")
        print(f"Error: {e}")

    input("Press any key to exit.")

if __name__ == "__main__":
    main()
