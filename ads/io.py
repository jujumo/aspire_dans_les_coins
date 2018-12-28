__author__ = 'jumo'
import csv

CSV_SEP = ';'


def to_csv(filepath, ads):
    # collect the properties
    properties = set(['id', 'type'])
    for _, offer in ads.items():
        properties.update(offer.properties())

    with open(filepath, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=properties)
        writer.writeheader()
        for idx, offer in ads.items():
            new_ads = offer.__dict__
            new_ads['type'] = type(offer).__name__
            writer.writerow(new_ads)
