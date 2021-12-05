from abc import ABC, abstractmethod

from merchantsguide.roman2int import roman2int
from merchantsguide.registry import Registry


def _alien2roman(alien: [str]):
    return "".join(map(Registry().get_numeral, alien))


class BaseCommand(ABC):
    """
    A Command that either updates the registry or answers a query.
    """

    def __repr__(self):
        return f"{type(self).__name__}"

    @abstractmethod
    def execute(self):
        pass


class NumeralUpdateCommand(BaseCommand):
    """
    Updates the value of an alien numeral in the registry.
    """

    def __init__(self, alien_numeral: str, roman_numeral: str):
        self.alien_numeral = alien_numeral
        self.roman_numeral = roman_numeral

    def __repr__(self):
        return f"{super().__repr__()}: set {self.alien_numeral} to {self.roman_numeral}"

    def execute(self):
        Registry().update_numeral(self.alien_numeral, self.roman_numeral)


class MineralUpdateCommand(BaseCommand):
    """
    Updates the price of a mineral in the registry.
    """

    def __init__(self, mineral: str, units: [str], price: int):
        self.mineral = mineral
        self.units = units
        self.price = price

    def __repr__(self):
        return f"{super().__repr__()}: set the price of {' '.join(self.units)} {self.mineral} to {self.price}"

    def execute(self):
        try:
            roman = _alien2roman(self.units)
            num_units = roman2int(roman)
        except ValueError as e:
            return str(e)

        Registry().update_mineral(self.mineral, self.price/num_units)


class NumberQueryCommand(BaseCommand):
    """
    Translates alien numbers into decimal.
    """

    def __init__(self, alien_number: [str]):
        self.alien_number = alien_number

    def __repr__(self):
        return f"{super().__repr__()}: calculates the decimal value of {' '.join(self.alien_number)}"

    def execute(self):
        try:
            roman = _alien2roman(self.alien_number)
            value = roman2int(roman)
        except ValueError as e:
            return str(e)

        return f"{' '.join(self.alien_number)} is {value}"


class MineralQueryCommand(BaseCommand):
    """
    Calculates the price of k units of a mineral, where k is an alien number.
    """

    def __init__(self, alien_number: [str], mineral: str):
        self.alien_number = alien_number
        self.mineral = mineral

    def __repr__(self):
        return f"{super().__repr__()}: calculates the price of {' '.join(self.alien_number)} units of {self.mineral}"

    def execute(self):
        try:
            roman = _alien2roman(self.alien_number)
            units = roman2int(roman)
            per_unit = Registry().get_mineral(self.mineral)
        except ValueError as e:
            return str(e)
        price = round(units * per_unit)

        return f"{' '.join(self.alien_number)} {self.mineral} is {price} Credits"


class UnknownCommand(BaseCommand):

    def __repr__(self):
        return f"{super().__repr__()}: displays a generic error message"

    def execute(self):
        return "I have no idea what you are talking about"
