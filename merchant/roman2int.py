from parsimonious import Grammar, NodeVisitor, ParseError

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

    @staticmethod
    def _sub(text):
        return VALUES[text[1]] - VALUES[text[0]]

    def visit_sub_ones(self, node, visited_children):
        return self._sub(node.text)

    def visit_sub_tens(self, node, visited_children):
        return self._sub(node.text)

    def visit_sub_hundreds(self, node, visited_children):
        return self._sub(node.text)

    def generic_visit(self, node, visited_children):
        if node.text == "":
            return 0
        if len(node.text) == 1:
            return VALUES[node.text]
        return sum(visited_children)


VISITOR = RomanVisitor()


def roman2int(s):
    try:
        tree = GRAMMAR.parse(s)
    except ParseError:
        raise ValueError(f"Could not parse input {s}")

    return VISITOR.visit(tree)
