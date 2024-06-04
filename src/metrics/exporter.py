import csv as csv
from typing import Dict


class Exporter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def export_to_csv(dictionary: Dict):
        with open('metrics.csv', 'w', newline='') as csvFile:
            writer = csv.DictWriter(csvFile, dictionary.keys())
            writer.writeheader()
            writer.writerow(dictionary)
