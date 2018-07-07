__author__ = 'jumo'


class Offer(object):
    @staticmethod
    def properties_required():
        """ defines the list of optional attributes """
        return ['url']

    @staticmethod
    def properties_optional():
        """ defines the list of optional attributes """
        return []

    def __init__(self, **kwargs):
        for p in self.properties_required():
            if p not in kwargs:
                print(kwargs)
                raise ValueError('missing required arg {} for class {}'.format(p, type(self)))
            self.__dict__[p] = kwargs.get(p)

        for p in self.properties_optional():
            self.__dict__[p] = kwargs.get(p)


class Sale(Offer):
    @staticmethod
    def properties_required():
        """ defines the list of optional attributes """
        return Offer.properties_required() + [
            'price',
            'location',
            'zip',
            'date_grabbed'
        ]

    @staticmethod
    def properties_optional():
        """ defines the list of optional attributes """
        return Offer.properties_optional() + [
            'date_creation',
            'thumb'
        ]


class SaleEstate(Sale):
    @staticmethod
    def properties_required():
        """ defines the list of optional attributes """
        return Sale.properties_required() + [
            'category',
            'surface']

    @staticmethod
    def properties_optional():
        """ defines the list of optional attributes """
        return Sale.properties_optional() + [
            'rooms',
            'real_estate']

