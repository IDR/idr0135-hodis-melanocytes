import csv
import argparse
import io


DESC = """
Splits a column with multiple entries into separate columns with
one entry / column.
"""

parser = argparse.ArgumentParser(description=DESC)
parser.add_argument("-s", help="Split character", default=";")
parser.add_argument("column", help="Column name")
parser.add_argument("file", help="Annotations file")
args = parser.parse_args()

with open(args.file, mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    rows = list(csv_reader)
    max = 0
    for row in rows:
        values = row[args.column].split(args.s)
        if len(values) > max:
            max = len(values)

    field_names = [n for n in csv_reader.fieldnames if n != args.column]
    for i in range(0, max):
        field_names.append(f"{args.column} {(i+1)}")

    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=field_names)
    csv_writer.writeheader()
    for row in rows:
        values = row[args.column].split(args.s)
        row.pop(args.column)
        for i, value in enumerate(values):
            row[f"{args.column} {(i+1)}"] = value
        csv_writer.writerow(row)
    print(output.getvalue())
