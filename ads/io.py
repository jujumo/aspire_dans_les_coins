__author__ = 'jumo'
import pandas as pd


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
