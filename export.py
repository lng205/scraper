"""
This module is used to export the data from the database to a csv file.
"""

import csv
import db
from markdownify import markdownify as md

def export_data():
    """
    This function exports the data from the database to a csv file.
    """
    with open('data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Votes', 'Answers', 'Views', 'Time', 'Title', 'Question', 'Top_Answer', 'Top_Answer_Votes', 'url'])
        for id in db.get_ids():
            row = db.get_data(id)
            row[6] = md(row[6]) if row[6] is not None else None
            row[7] = md(row[7]) if row[7] is not None else None
            row.append(f"https://stackoverflow.com/questions/{id}")
            writer.writerow(row)


if __name__ == "__main__":
    export_data()