import pytest

from merchantsguide.parse_input import parse_input
from merchantsguide.commands import *


def test_numeral_update_valid():
    cmd = parse_input("bork is I")
    assert isinstance(cmd, NumeralUpdateCommand)
    assert cmd.alien_numeral == 'bork'
    assert cmd.roman_numeral == 'I'


def test_numeral_update_two_alien_numerals():
    cmd = parse_input("bork bork is I")
    assert isinstance(cmd, UnknownCommand)


def test_numeral_update_uppercase_alien_numeral():
    cmd = parse_input("Bork is I")
    assert isinstance(cmd, UnknownCommand)


def test_numeral_update_two_is():
    cmd = parse_input("bork is is I")
    assert isinstance(cmd, UnknownCommand)


def test_numeral_update_two_roman_numerals():
    cmd = parse_input("bork is II")
    assert isinstance(cmd, UnknownCommand)


def test_numeral_update_invalid_roman_numeral():
    cmd = parse_input("bork is Y")
    assert isinstance(cmd, UnknownCommand)


def test_mineral_update_valid():
    cmd = parse_input("bork bork Silver is 34 credits")
    assert isinstance(cmd, MineralUpdateCommand)
    assert cmd.mineral == 'Silver'
    assert cmd.units == ['bork', 'bork']
    assert cmd.price == 34


def test_mineral_update_invalid_units():
    cmd = parse_input("bork Bork Silver is 34 credits")
    assert isinstance(cmd, UnknownCommand)


def test_mineral_update_invalid_mineral():
    cmd = parse_input("bork bork silver is 34 credits")
    assert isinstance(cmd, UnknownCommand)


def test_mineral_update_invalid_price():
    cmd = parse_input("bork bork silver is many credits")
    assert isinstance(cmd, UnknownCommand)


def test_number_query_valid():
    cmd = parse_input("how much is the fish?")
    assert isinstance(cmd, NumberQueryCommand)
    assert cmd.alien_number == ['the', 'fish']


def test_number_query_invalid():
    cmd = parse_input("how much is the Iron?")
    assert isinstance(cmd, UnknownCommand)


def test_mineral_query_valid():
    cmd = parse_input("how many credits is bork bork Silver?")
    assert isinstance(cmd, MineralQueryCommand)
    assert cmd.mineral == 'Silver'
    assert cmd.alien_number == ['bork', 'bork']


def test_mineral_query_invalid_mineral():
    cmd = parse_input("how many credits is bork bork fish?")
    assert isinstance(cmd, UnknownCommand)


def test_mineral_query_invalid_alien_numeral():
    cmd = parse_input("how many credits is bork Bork Silver?")
    assert isinstance(cmd, UnknownCommand)


def test_mineral_query_malformed_query():
    cmd = parse_input("how much is bork Bork Silver?")
    assert isinstance(cmd, UnknownCommand)
