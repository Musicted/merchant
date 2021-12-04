from sys import stdin

from merchantsguide.parse_input import parse_input


class Merchant:

    @staticmethod
    def single_command(s):
        cmd = parse_input(s)
        return cmd

    @staticmethod
    def repl():
        for cmd in stdin:
            res = Merchant.single_command(cmd)
            if res:
                print(res)
