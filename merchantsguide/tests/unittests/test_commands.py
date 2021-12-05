import pytest

from merchantsguide.commands import MineralQueryCommand, MineralUpdateCommand, NumberQueryCommand, NumeralUpdateCommand
from merchantsguide.commands import UnknownCommand, BaseCommand
from merchantsguide.registry import Registry


def test_update_numeral():
    r = Registry()
    r.reset()

    # add four definitions and assert that nothing is returned
    assert NumeralUpdateCommand('bork', 'I').execute() is None
    assert NumeralUpdateCommand('kmar', 'V').execute() is None
    assert NumeralUpdateCommand('gromp', 'X').execute() is None
    assert NumeralUpdateCommand('urx', 'L').execute() is None

    # check that only these four definitions exist and are correct
    assert len(r.alien_numerals) == 4
    assert r.get_numeral('bork') == 'I'
    assert r.get_numeral('kmar') == 'V'
    assert r.get_numeral('gromp') == 'X'
    assert r.get_numeral('urx') == 'L'

    # update one definition and check for correctness
    assert NumeralUpdateCommand('urx', 'C').execute() is None
    assert len(r.alien_numerals) == 4
    assert r.get_numeral('urx') == 'C'


def test_query_number():
    r = Registry()
    r.reset()

    # define some numerals
    NumeralUpdateCommand('bork', 'I').execute()
    NumeralUpdateCommand('kmar', 'V').execute()
    NumeralUpdateCommand('gromp', 'X').execute()
    NumeralUpdateCommand('urx', 'L').execute()

    # check for correct calculation
    assert NumberQueryCommand(['bork']).execute() == "bork is 1"
    assert NumberQueryCommand(['urx']).execute() == "urx is 50"
    assert NumberQueryCommand(['gromp', 'urx', 'bork', 'bork']).execute()[-2:] == "42"

    # assert that invalid inputs are handled correctly
    assert NumberQueryCommand(['blork']).execute()[:7] == "Unknown"
    assert NumberQueryCommand(['urx', 'urx']).execute()[:9] == "Could not"


def test_update_mineral():
    r = Registry()
    r.reset()

    # define some numerals
    NumeralUpdateCommand('bork', 'I').execute()
    NumeralUpdateCommand('kmar', 'V').execute()
    NumeralUpdateCommand('gromp', 'X').execute()
    NumeralUpdateCommand('urx', 'L').execute()

    # add some minerals
    assert MineralUpdateCommand('Iron', ['bork', 'bork'], 99).execute() is None
    assert MineralUpdateCommand('Gold', ['gromp'], 2500).execute() is None

    # verify the registry status
    assert len(r.mineral_prices) == 2
    assert r.get_mineral('Iron') == 49.5
    assert r.get_mineral('Gold') == 250.0

    # uh-oh! Gold is worthless now!
    MineralUpdateCommand('Gold', ['urx'], 500).execute()
    assert len(r.mineral_prices) == 2
    assert r.get_mineral('Gold') == 10.0

    # check error cases, verify that nothing is changed
    assert MineralUpdateCommand('Iron', ['bork', 'bark'], 99).execute()[:7] == 'Unknown'
    assert MineralUpdateCommand('Iron', ['kmar', 'kmar'], 99).execute()[:5] == 'Could'
    assert r.get_mineral('Iron') == 49.5


def test_query_mineral():
    r = Registry()
    r.reset()

    # define some numerals
    NumeralUpdateCommand('bork', 'I').execute()
    NumeralUpdateCommand('kmar', 'V').execute()
    NumeralUpdateCommand('gromp', 'X').execute()
    NumeralUpdateCommand('urx', 'L').execute()

    # add some minerals
    MineralUpdateCommand('Iron', ['bork', 'bork'], 99).execute()
    MineralUpdateCommand('Gold', ['gromp'], 2500).execute()

    # check that mineral prices are calculated correctly
    assert MineralQueryCommand(['gromp'], 'Iron').execute()[-12:-7] == " 495 "
    assert MineralQueryCommand(['bork'], 'Gold').execute()[-12:-7] == " 250 "

    # check that unknown minerals/numerals and invalid numbers are handled correctly
    assert MineralQueryCommand(['glorp'], 'Iron').execute()[:7] == "Unknown"
    assert MineralQueryCommand(['bork'], 'Unobtainium').execute()[:7] == "Unknown"
    assert MineralQueryCommand(['kmar', 'kmar'], 'Iron').execute()[:9] == "Could not"


def test_reprs_dont_fail():
    assert repr(NumeralUpdateCommand('bork', 'I')) != repr(MineralUpdateCommand('Iron', ['bork'], 23))\
        != repr(NumberQueryCommand(['bork'])) != repr(MineralQueryCommand(['bork'], 'Iron'))\
        != repr(UnknownCommand())


