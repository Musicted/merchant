"""
Merchant
========

Reads and executes commands and provides a REPL.
"""
from sys import stdin

from merchantsguide.parse_input import parse_input


class Merchant:
    """
    Merchant's Guide to the Galaxy.

    Reads and executes commands and provides a REPL.
    """
    @staticmethod
    def single_command(s):
        """
        Read and execute a single command.

        :param s: the input string
        :return: the command's return value (either a string or None)
        """
        cmd = parse_input(s)
        return cmd.execute()

    @staticmethod
    def repl():  # pragma: no cover
        """
        Initiate a read-execute-print loop (REPL).

        Read inputs from stdin, execute them, and (if applicable) print a response for each until an EOF is received.

        :return: None
        """
        for line in stdin:
            res = Merchant.single_command(line.strip())
            if res:
                print(res)
