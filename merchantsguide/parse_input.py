from parsimonious import Grammar, ParseError, NodeVisitor

from merchantsguide.commands import MineralQueryCommand, MineralUpdateCommand, NumeralUpdateCommand, NumberQueryCommand

GRAMMAR = Grammar(
    r"""
    input_string = command newline?
    command = (query ws "?") / (update !"?")
    
    update = numeral_update / mineral_update
    numeral_update = alien_numeral ws is ws roman_numeral
    mineral_update = alien_number ws mineral ws is ws decimal ws credits
    
    query = number_query / mineral_query
    number_query = "how much" ws is ws alien_number
    mineral_query = "how many" ws credits ws is ws alien_number ws mineral
    
    alien_number = alien_numeral (ws alien_numeral)*
    mineral = ~"[A-Z][a-z]+"
    
    alien_numeral = ~"[a-z]+"
    roman_numeral = ~"[IVXLCDM]"
    
    ws = ~"\s*"
    is = "is"
    credits = "Credits" / "credits"
    decimal = ~"\d+"
    newline = ws ~"\n"
    """
)


class CommandVisitor(NodeVisitor):

    def visit_input_string(self, node, visited_children):
        return visited_children[0]

    def visit_command(self, node, visited_children):
        return visited_children[0][0]

    def visit_query(self, node, visited_children):
        return visited_children[0]

    def visit_update(self, node, visited_children):
        return visited_children[0]

    def visit_numeral_update(self, node, visited_children):
        alien, _, _, _, roman = visited_children
        return NumeralUpdateCommand(alien, roman)

    def visit_mineral_update(self, node, visited_children):
        units, _, mineral, _, _, _, price, *_ = visited_children
        return MineralUpdateCommand(mineral, units, int(price))

    def visit_number_query(self, node, visited_children):
        number = visited_children[4]
        return NumberQueryCommand(number)

    def visit_mineral_query(self, node, visited_children):
        number, mineral = visited_children[6], visited_children[8]
        return MineralQueryCommand(number, mineral)

    def visit_alien_number(self, node, visited_children):
        return node.text.split(" ")

    def generic_visit(self, node, visited_children):
        return visited_children or node.text


VISITOR = CommandVisitor()


def parse_input(s: str):
    try:
        tree = GRAMMAR.parse(s)
    except ParseError:
        return "I have no idea what you are talking about"

    cmd = VISITOR.visit(tree)
    return cmd.execute()
