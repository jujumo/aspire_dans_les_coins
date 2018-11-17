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
