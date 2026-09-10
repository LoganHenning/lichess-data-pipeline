# Import Python's built-in CSV library
# This lets us read and write CSV files
import csv


# Import Python's built-in JSON library
# This lets us save the validation report as a JSON file
import json


# Open the raw games CSV file for reading
with open("data/games.csv", newline="") as file:


    # Read each CSV row as a dictionary
    # Example:
    # {"game_id": 1, "white_player": "Alice", ...}
    reader = csv.DictReader(file)


    # Define the columns that every valid input file must contain
    required_columns = ["game_id", "white_player", "black_player", "result"]


    # Display the actual column names found in the CSV
    print(reader.fieldnames)


    # Create an empty list to store any required columns that are missing
    missing_columns = []


    # Check every required column
    for column in required_columns:

        # If the required column is not in the CSV header,
        # add it to the missing_columns list
        if column not in reader.fieldnames:
            missing_columns.append(column)

    # Display any missing columns
    print("Missing columns:", missing_columns)


    # Count the total number of rows processed
    row_count = 0

    # Store game IDs that have already been seen
    # A set is useful because it quickly checks whether a value already exists
    seen_game_ids = set()

    # Store rows that pass all validation checks
    valid_rows = []

    # Count duplicate game IDs
    duplicate_count = 0

    # Count blank required values
    blank_value_count = 0


    # Loop through every row in the CSV
    for row in reader:

        # Increase the total row count
        row_count = row_count + 1

        # Assume the row is valid unless a validation check fails
        is_valid = True


        # Check each required column for blank values
        for column in required_columns:

            # If a required field is blank,
            # record the problem and mark the row invalid
            if row[column] == "":
                print("Blank value found:", row)

                blank_value_count = blank_value_count + 1
                is_valid = False


        # Check whether this game_id has already appeared
        if row["game_id"] in seen_game_ids:

            # Report the duplicate
            print("Duplicate game_id found:", row["game_id"])

            duplicate_count = duplicate_count + 1
            is_valid = False

        else:

            # If this is the first time seeing the game_id,
            # add it to the set
            seen_game_ids.add(row["game_id"])

        # Only keep rows that passed every validation check
        if is_valid:
            valid_rows.append(row)


    # Display the total number of rows processed
    print("Row count:", row_count)


    # Display the rows that passed validation
    print("Valid rows:", valid_rows)


# Open clean_games.csv for writing
with open("data/clean_games.csv", "w", newline="") as file:

    # Create a CSV writer using the same required column names
    writer = csv.DictWriter(file, fieldnames=required_columns)

    # Write the CSV header row
    writer.writeheader()

    # Write all valid rows to the cleaned output file
    writer.writerows(valid_rows)


# Build a summary of the validation results
validation_report = {
    "total_rows": row_count,
    "valid_rows": len(valid_rows),
    "missing_columns": missing_columns,
    "duplicate_count": duplicate_count,
    "blank_value_count": blank_value_count
}


# Display the validation report
print("Validation report:", validation_report)


# Open the JSON report file for writing
with open("data/validation_report.json", "w") as file:

    # Save the validation report as formatted JSON
    # intent=4 makes teh JSON easier for humans to read
    json.dump(validation_report, file, indent=4)