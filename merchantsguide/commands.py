"""
Commands
========

These commands update the mineral and numeral repository and answer queries.
"""
from abc import ABC, abstractmethod

from merchantsguide.roman2int import roman2int
from merchantsguide.registry import Registry


def _alien2roman(alien: [str]):
    """
    Auxiliary function that translates alien to Roman numerals.

    :param alien: a list of alien numerals
    :return: the corresponding string of Roman numerals
    """
    return "".join(map(Registry().get_numeral, alien))


class BaseCommand(ABC):  # pragma: no cover
    """
    Abstract command that either updates the registry or answers a query.
    """

    def __repr__(self):
        return f"{type(self).__name__}"

    @abstractmethod
    def execute(self):
        """
        Execute a command and return its output, if any.

        :raise NotImplementedError
        """
        raise NotImplementedError()


class NumeralUpdateCommand(BaseCommand):
    """
    Updates the Roman numeral value of an alien numeral in the registry.
    """

    def __init__(self, alien_numeral: str, roman_numeral: str):
        """
        Initialize a NumeralUpdateCommand with an alien and a corresponding Roman numeral.

        On execution, the repository is updated with this key-value pair.

        :param alien_numeral: An alien numeral, e.g. 'bork'
        :param roman_numeral: A Roman numeral, e.g. 'I'
        """
        self.alien_numeral = alien_numeral
        self.roman_numeral = roman_numeral

    def __repr__(self):
        return f"{super().__repr__()}: set {self.alien_numeral} to {self.roman_numeral}"

    def execute(self):
        """
        Update the repository with the key-value pair provided on init.

        :return: None
        """
        Registry().update_numeral(self.alien_numeral, self.roman_numeral)


class MineralUpdateCommand(BaseCommand):
    """
    Updates the price of a mineral in the registry.
    """

    def __init__(self, mineral: str, units: [str], price: int):
        """
        Initialize a MineralUpdateCommand with information on the price of a mineral.

        On execution, the per-unit price is calculated and the registry is updated with it.

        :param mineral: The name of a mineral
        :param units: An alien number representation as a list of numerals
        :param price: The price of the given number of units of the given mineral
        """
        self.mineral = mineral
        self.units = units
        self.price = price

    def __repr__(self):
        return f"{super().__repr__()}: set the price of {' '.join(self.units)} {self.mineral} to {self.price}"

    def execute(self):
        """
        Update the repository with the calculated price per unit.

        Price per unit is calculated by dividing the price by the number of units.

        :return: None
        """
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
        """
        Initializes the NumberQueryCommand with a number given in alien number format.

        :param alien_number: An alien number representation as a list of numerals
        """
        self.alien_number = alien_number

    def __repr__(self):
        return f"{super().__repr__()}: calculates the decimal value of {' '.join(self.alien_number)}"

    def execute(self):
        """
        Calculate the decimal value of the alien number.

        :return: The query answer string
        """
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
        """
        Initialize the MineralQueryCommand with an alien number and a mineral name.

        :param alien_number: An alien number representation as a list of numerals
        :param mineral: The name of the mineral in question
        """
        self.alien_number = alien_number
        self.mineral = mineral

    def __repr__(self):
        return f"{super().__repr__()}: calculates the price of {' '.join(self.alien_number)} units of {self.mineral}"

    def execute(self):
        """
        Calculate the price of the given number of units of the given mineral.

        :return: The query answer string
        """
        try:
            roman = _alien2roman(self.alien_number)
            units = roman2int(roman)
            per_unit = Registry().get_mineral(self.mineral)
        except ValueError as e:
            return str(e)
        price = round(units * per_unit)

        return f"{' '.join(self.alien_number)} {self.mineral} is {price} Credits"


class UnknownCommand(BaseCommand):
    """
    Displays a generic error message, i.e. in case of a parsing error.
    """
    def __repr__(self):
        return f"{super().__repr__()}: displays a generic error message"

    def execute(self):
        """
        Does nothing and returns an error string.

        :return: the error string
        """
        return "I have no idea what you are talking about"
