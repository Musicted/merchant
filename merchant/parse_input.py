from parsimonious import Grammar

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
