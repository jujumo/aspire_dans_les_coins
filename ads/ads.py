__author__ = 'jumo'
import pandas as pd
import logging


class Offer(object):
    @staticmethod
    def properties_required():
        """ defines the list of optional attributes """
        return ['url']

    def __init__(self, **kwargs):
        # check all required props are there
        requirements = [required in kwargs for required in self.properties_required()]
        if not all(requirements):
            missing = [missing for missing in self.properties_required() if missing not in kwargs]
            mgs = 'missing required arg {} for class {}'.format(','.join(missing), type(self))
            logging.error(mgs)
            raise ValueError(mgs)

        # also registers all of them, even the none required
        self.__dict__ = kwargs

    def properties(self):
        return [p for p in self.__dict__]

    def properties_optional(self):
        return [optional for optional in self.__dict__ if optional not in self.properties_required()]


class Sale(Offer):
    @staticmethod
    def properties_required():
        """ defines the list of optional attributes """
        return Offer.properties_required() + [
            'price',
            'location',
            'zip',
            'date_grabbed',
            # 'date_creation',
        ]


class SaleEstate(Sale):
    @staticmethod
    def properties_required():
        """ defines the list of optional attributes """
        return Sale.properties_required() + [
            'real_estate_category',
            'surface']


def to_pandas(ad_dict):
    # collect the properties
    p = set(['id', 'type'])
    for _, offer in ad_dict.items():
        p.update(offer.properties())

    table = pd.DataFrame(columns=p)
    table = table.set_index('id')
    for idx, offer in ad_dict.items():
        new_ads = offer.__dict__
        new_ads['type'] = type(offer).__name__
        new_ads = pd.Series(new_ads)
        table.at[idx] = new_ads

    table.where(table.notnull(), None)
    return table


def from_pandas(df):
    ad_dict = dict()
    for index, r in df.iterrows():
        d = r.to_dict()
        class_name = d['type']
        klass = globals()[class_name]
        c = klass(**d)
        ad_dict[index] = c
    return ad_dict


CSV_SEP = ';'


def from_csv_to_pandas(filepath):
    df = pd.read_csv(filepath, sep=CSV_SEP)
    df = df.set_index('id')
    return df


def from_pandas_to_csv(filepath, df):
    df.to_csv(filepath, sep=CSV_SEP)


def from_csv(filepath):
    df = from_csv_to_pandas(filepath)
    return from_pandas(df)


def to_csv(filepath, ads):
    table = to_pandas(ads)
    table.to_csv(filepath, sep=CSV_SEP)
