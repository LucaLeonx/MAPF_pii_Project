import csv as csv

class Exporter():
    def __init__(self) -> None:
        pass

    def export_to_CSV(self, dictionary : dict):
        with open('out.csv','w',newline='') as csvFile:
            writer = csv.DictWriter(csvFile,dictionary.keys())
            writer.writeheader()
            writer.writerow()