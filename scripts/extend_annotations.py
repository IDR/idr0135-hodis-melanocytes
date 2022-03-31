import io
import csv
import re
import argparse


DESC = """
Dupliate rows by extending the Image Names. For example an svs image
called EH-15740-001.svs might be imported as three images
EH-15740-001.svs [0], EH-15740-001.svs [label image] and EH-15740-001.svs [macro image],
but the annotations.csv only has one entry for the EH-15740-001.svs file.
Then you can run:
python extend_annotations.py annotations.csv -r ' [0]' ' [label image]' ' [macro image]' > out.csv
to fix the annotations.
"""

parser = argparse.ArgumentParser(description=DESC)
parser.add_argument('-r', action="store_true", default=False,
                    help='Remove the original row')
parser.add_argument("file", help="Annotations file")
parser.add_argument("extensions", help="The extension to add", nargs='+')
args = parser.parse_args()

with open(args.file, mode='r') as csv_file_in:
    csv_reader = csv.DictReader(csv_file_in)
    org_rows = list(csv_reader)

    output = io.StringIO()
    csv_writer = csv.DictWriter(output, fieldnames=csv_reader.fieldnames)
    csv_writer.writeheader()
    for org_row in org_rows:
        if not args.r:
            csv_writer.writerow(org_row)
        org_image_name = org_row["Image Name"]
        for extension in args.extensions:
            org_row["Image Name"] = f"{org_image_name}{extension}"
            csv_writer.writerow(org_row)
    print(output.getvalue())