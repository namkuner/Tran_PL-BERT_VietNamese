from .Cardinal import CardinalVietnamese
import re
from singleton_decorator import  singleton

@singleton
class Fraction:
    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(",")
        self.space_filter_regex = re.compile(" ")
        self.trans_dict = {
            "½": {"prepended": "một", "single": "một", "text": "phần hai"},
            "⅓": {"prepended": "một", "single": "một", "text": "phần ba"},
            "⅔": {"prepended": "hai", "single": "hai", "text": "phần ba"},
            "¼": {"prepended": "một", "single": "một", "text": "phần tư"},
            "¾": {"prepended": "ba", "single": "ba", "text": "phần tư"},
            "⅕": {"prepended": "một", "single": "một", "text": "phần năm"},
            "⅖": {"prepended": "hai", "single": "hai", "text": "phần năm"},
            "⅗": {"prepended": "ba", "single": "ba", "text": "phần năm"},
            "⅘": {"prepended": "bốn", "single": "bốn", "text": "phần năm"},
            "⅙": {"prepended": "một", "single": "một", "text": "phần sáu"},
            "⅚": {"prepended": "năm", "single": "năm", "text": "phần sáu"},
            "⅐": {"prepended": "một", "single": "một", "text": "phần bảy"},
            "⅛": {"prepended": "một", "single": "một", "text": "phần tám"},
            "⅜": {"prepended": "ba", "single": "ba", "text": "phần tám"},
            "⅝": {"prepended": "năm", "single": "năm", "text": "phần tám"},
            "⅞": {"prepended": "bảy", "single": "bảy", "text": "phần tám"},
            "⅑": {"prepended": "một", "single": "một", "text": "phần chín"},
            "⅒": {"prepended": "một", "single": "một", "text": "phần mười"}
        }
        self.special_regex = re.compile(f"({'|'.join(self.trans_dict.keys())})")
        self.cardinal = CardinalVietnamese()
        self.slash_regex = re.compile(r"(-?\d{1,3}( \d{3})+|-?\d+) *\/ *(-?\d{1,3}( \d{3})+|-?\d+)")

        # Không cần chuyển đổi từ Cardinal sang Ordinal trong tiếng Việt
        self.trans_denominator = {}

        self.edge_dict = {
            "1": {"singular": "trên một", "plural": "trên một"},
            "2": {"singular": "phần hai", "plural": "phần hai"},
            "4": {"singular": "phần tư", "plural": "phần tư"}
        }

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)
        match = self.special_regex.search(token)
        if match:
            frac = match.group(1)
            frac_dict = self.trans_dict[frac]

            remainder = self.special_regex.sub("", token)
            if remainder:
                prefix = self.cardinal.convert(remainder)
                result = f"{prefix} và {frac_dict['prepended']} {frac_dict['text']}"
            else:
                result = f"{frac_dict['single']} {frac_dict['text']}"

        else:
            match = self.slash_regex.search(token)
            if match:
                numerator = match.group(1)
                denominator = match.group(3)

                numerator = self.space_filter_regex.sub("", numerator)
                denominator = self.space_filter_regex.sub("", denominator)

                numerator_text = self.cardinal.convert(numerator)

                if denominator in self.edge_dict:
                    result = f"{numerator_text} {self.edge_dict[denominator]['singular']}"

                else:
                    denominator_text = self.cardinal.convert(denominator)
                    result = f"{numerator_text} phần {denominator_text}"

                remainder = self.slash_regex.sub("", token)
                if remainder:
                    remainder_text = self.cardinal.convert(remainder)
                    result = f"{remainder_text} và {result}"

            else:
                result = token

        return result

if __name__ == "__main__":
    fraction = Fraction()

    test_cases = [
        "½",
        "1½",
        "2¼",
        "3⅔",
        "1/4",
        "3/4",
        "5/8",
        "10/3",
        "100/25",
        "1000/999",
        "2 1/2",
        "3 3/4",
        "5 2/3",
        "100 1/100",
    ]

    for case in test_cases:
        result = fraction.convert(case)
        print(f"Phân số: {case}")
        print(f"Chuyển đổi: {result}")
        print()