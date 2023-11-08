import csv

# Input and output file paths
input_file = '../../input/variable_names_full.csv'
output_file = '../../input/Variable_Names.csv'

# Open the input CSV file for reading and the output CSV file for writing
with open(input_file, 'r', newline='') as input_csv, open(output_file, 'w', newline='') as output_csv:
    reader = csv.DictReader(input_csv)
    fieldnames = reader.fieldnames  # Get the header from the input CSV

    # Write the header to the output CSV
    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
    writer.writeheader()

    # Iterate through the rows in the input CSV
    for row in reader:
        # Check if the "variable_name" column has a value (non-empty string)
        if row["variable_name"]:
            row["variable_name"] = row["variable_name"].replace("-","_")
            writer.writerow(row)

print(f"Compressed csv with corrected naming conventions written to '{output_file}'.")
