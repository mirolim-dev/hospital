from decimal import Decimal
from django.utils.translation import gettext_lazy as _

class MEASURE():
    GRAMM = "g"
    MILLIGRAMM = "mg"
    LITER = "l"
    MILLILITER = 'ml'
    UNIT = 'unit'

    def __init__(self):
        self.types = {
            self.GRAMM: "weight", 
            self.MILLIGRAMM: "weight",
            self.LITER: "liquid",
            self.MILLILITER: "liquid",
            self.UNIT: "unit"
        }

        self.values = {
            self.GRAMM: 1,
            self.MILLIGRAMM: 10**(-3),
            self.LITER: 1, 
            self.MILLILITER: 10**(-3),
            self.UNIT: 1
        }

    
    @property
    def choices(self)->tuple:
        value = (
            (self.GRAMM, "Gramm"), 
            (self.MILLIGRAMM, "MilliGramm"),
            (self.LITER, "Liter"),
            (self.MILLILITER, "MilliLiter"),
            (self.UNIT, "Dona"),
        )
        return tuple(value)

    def is_match_measure_type(self, measure1, measure2):
        return self.types[measure1] == self.types[measure2]
    
    def convert(self, from_measure, to_measure):
        if not self.is_match_measure_type(from_measure, to_measure):
            raise ValueError(_("Ikkala o'lchov turi ham quyidagilarga mos kelishi kerak (vazn, suyuqlik, birlik)"))
        difference_value = self.values[from_measure]/self.values[to_measure]
        return Decimal(difference_value)
