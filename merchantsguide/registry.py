"""
Registry
========

Keeps information on alien-Roman numeral mapping and mineral unit prices.
"""
from numbers import Number

from singleton_decorator import singleton


@singleton
class Registry:
    """
    Keeps information on alien-Roman numeral mapping and mineral unit prices.

    Implemented as a singleton.
    """
    def reset(self):
        """
        Resets the entire registry.

        :return: None
        """
        self.alien_numerals = {}
        self.mineral_prices = {}

    def __init__(self):
        """
        Default constructor.
        """
        self.alien_numerals = {}
        self.mineral_prices = {}

    def update_numeral(self, alien: str, roman: str):
        """
        Update the numeral registry with an alien-Roman pair.

        :param alien: an alien numeral
        :param roman: a Roman numeral
        :return: None
        """
        self.alien_numerals[alien] = roman

    def update_mineral(self, mineral: str, price: Number):
        """
        Update the mineral registry with the unit price of a mineral.

        :param mineral: a mineral name
        :param price: the unit price
        :return: None
        """
        self.mineral_prices[mineral] = price

    def get_numeral(self, numeral: str):
        """
        Given an alien numeral, retrieve the corresponding Roman numeral.

        :param numeral: an alien numeral
        :return: the corresponding Roman numeral
        :raise ValueError: if the alien numeral has no corresponding Roman numeral
        """
        try:
            return self.alien_numerals[numeral]
        except KeyError:
            raise ValueError(f"Unknown alien numeral '{numeral}'")

    def get_mineral(self, mineral: str) -> Number:
        """
        Given the name of a mineral, retrieve its unit price.

        :param mineral: a mineral name
        :return: the unit price
        :raise ValueError: if the mineral's price is unknown
        """
        try:
            return self.mineral_prices[mineral]
        except KeyError:
            raise ValueError(f"Unknown mineral '{mineral}'")
