"""
Roman2Int
=========

Converts Roman numbers < 4000 into integers.
"""
from parsimonious import Grammar, NodeVisitor, ParseError

# The grammar used to parse Roman numbers.
GRAMMAR = Grammar(
    r"""
    number = thousands? hundreds? tens? ones?
    
    ones = sub_ones / ("V"? single_ones?)
    sub_ones = "IX" / "IV"
    single_ones = "I" "I"? "I"?
    
    tens = sub_tens / ("L"? single_tens?)
    sub_tens = "XC" / "XL"
    single_tens = "X" "X"? "X"?
    
    hundreds = sub_hundreds / ("D"? single_hundreds?)
    sub_hundreds = "CM" / "CD"
    single_hundreds = "C" "C"? "C"?
    
    thousands = "M" "M"? "M"?
    """
)

# The value of each individual numeral.
VALUES = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}


class RomanVisitor(NodeVisitor):
    """
    Traverses the parse tree and calculates the integer value.

    Methods with the signature
        visit_*node_type*(self, node, visited_children)
    are called dynamically from the base class.
    """
    @staticmethod
    def _sub(text: str) -> int:
        """
        Auxiliary function that calculates the value of *subtractive pairs* of Roman numerals, i.e. 'IV' or 'XC'.

        :param text:
        :return:
        """
        return VALUES[text[1]] - VALUES[text[0]]

    def visit_sub_ones(self, node, visited_children):
        return self._sub(node.text)

    def visit_sub_tens(self, node, visited_children):
        return self._sub(node.text)

    def visit_sub_hundreds(self, node, visited_children):
        return self._sub(node.text)

    def generic_visit(self, node, visited_children) -> int:
        """
        Recursively defines the value of each node that isn't a *subtractive pair*.

        :param node: the node in question
        :param visited_children: the node's children *after* visiting (i.e. after recursion returns)
        :return: the aggregated value of the node
        """
        # Empty (non-matched) node, i.e. a missing decimal place.
        # Has a value of 0.
        if node.text == "":
            return 0
        # Single numeral.
        # Has the value assigned by VALUES.
        if len(node.text) == 1:
            return VALUES[node.text]
        # Multiple numerals or subtractive pairs.
        # Has a value equal to the sum of all child nodes.
        return sum(visited_children)


VISITOR = RomanVisitor()


def roman2int(s: str) -> int:
    """
    Parse a string of roman numerals representing a number < 4000 and, if successful, calculate its integer value.

    As a quirk, the empty string is interpreted as 0, which is fair enough.

    :param s: a string of roman numerals
    :return: the integer value
    :raise ValueError: if parsing fails
    """
    try:
        tree = GRAMMAR.parse(s)
    except ParseError:
        raise ValueError(f"Could not parse input '{s}' as Roman numerals")

    return VISITOR.visit(tree)
