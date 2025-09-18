import csv

input_file = 'electricity/ElectricityProductionPlant.csv'
output_file = 'electricity/ElectricityProductionPlant_filtered.csv'

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    filtered_rows = [row for row in reader if row.get(
        'Canton') == 'BE' and row.get('SubCategory') == 'subcat_2']

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    if filtered_rows:
        writer = csv.DictWriter(csvfile, fieldnames=filtered_rows[0].keys())
        writer.writeheader()
        writer.writerows(filtered_rows)
    else:
        print('No matching rows found.')
