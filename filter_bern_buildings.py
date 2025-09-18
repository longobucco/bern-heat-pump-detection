import csv

input_file = 'electricity/ElectricityProductionPlant.csv'
output_file = 'dataset/BernBuildings.csv'

# This script filters the CSV file for rows where 'Canton' is 'BE' (ALL buildings in Bern)

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    filtered_rows = [row for row in reader if row.get('Canton') == 'BE']

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    if filtered_rows:
        writer = csv.DictWriter(csvfile, fieldnames=filtered_rows[0].keys())
        writer.writeheader()
        writer.writerows(filtered_rows)
    else:
        print('No matching rows found.')
