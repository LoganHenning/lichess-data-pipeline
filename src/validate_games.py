import csv
import json

with open("data/games.csv", newline="") as file:
    reader = csv.DictReader(file)

    required_columns = ["game_id", "white_player", "black_player", "result"]

    print(reader.fieldnames)

    missing_columns = []

    for column in required_columns:
        if column not in reader.fieldnames:
            missing_columns.append(column)

    print("Missing columns:", missing_columns)

    row_count = 0
    seen_game_ids = set()
    valid_rows= []
    duplicate_count = 0
    blank_value_count = 0

    for row in reader:
        row_count = row_count + 1
        is_valid = True

        for column in required_columns:
            if row[column] == "":
                print("Blank value found:", row)
                blank_value_count = blank_value_count + 1
                is_valid = False

        if row["game_id"] in seen_game_ids:
            print("Duplicate game_id found:", row["game_id"])
            duplicate_count = duplicate_count + 1
            is_valid = False
        else:
            seen_game_ids.add(row["game_id"])

        if is_valid:
            valid_rows.append(row)

    print("Row count:", row_count)

    print("Valid rows:", valid_rows)

with open("data/clean_games.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=required_columns)

    writer.writeheader()
    writer.writerows(valid_rows)

validation_report = {
    "total_rows": row_count,
    "valid_rows": len(valid_rows),
    "missing_columns": missing_columns,
    "duplicate_count": duplicate_count,
    "blank_value_count": blank_value_count
}

print("Validation report:", validation_report)

with open("data/validation_report.json", "w") as file:
    json.dump(validation_report, file, indent=4)