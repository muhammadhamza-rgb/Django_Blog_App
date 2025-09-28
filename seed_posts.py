import csv
import os

import django
from django.contrib.auth.hashers import make_password

# Correct settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

input_file = r"D:\Project\users.csv"
output_file = r"D:\Project\users_hashed.csv"

with open(input_file, newline="") as infile, open(
    output_file, "w", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["hashed_password"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        row["hashed_password"] = make_password(row["password"])
        writer.writerow(row)

print(f"Hashed passwords saved to {output_file}")
