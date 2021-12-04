from singleton_decorator import singleton


@singleton
class Registry:

    def __init__(self):
        self.alien_numerals = {}
        self.mineral_prices = {}

    def update_numeral(self, alien, roman):
        self.alien_numerals[alien] = roman

    def update_mineral(self, mineral, price):
        self.mineral_prices[mineral] = price

    def get_numeral(self, numeral):
        try:
            return self.alien_numerals[numeral]
        except KeyError:
            raise ValueError(f"Unknown alien numeral '{numeral}'")

    def get_mineral(self, mineral):
        try:
            return self.mineral_prices[mineral]
        except KeyError:
            raise ValueError(f"Unknown mineral '{mineral}'")
