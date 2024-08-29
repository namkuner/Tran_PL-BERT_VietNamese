from .Digit import DigitVietnamese
from .Cardinal import CardinalVietnamese
import re
from singleton_decorator import singleton
@singleton
class Decimal:
    def __init__(self):
        super().__init__()
        self.decimal_regex = re.compile(r"(-?\d*)\.(\d+)(.*)")
        self.number_regex = re.compile(r"(-?\d+)(.*)")
        self.filter_regex = re.compile(r"[,]")
        self.cardinal = CardinalVietnamese()
        self.digit = DigitVietnamese()
        self.suffixes = [
            "nghìn",
            "triệu",
            "tỷ",
            "nghìn tỷ",
            "triệu tỷ",
            "tỷ tỷ"
        ]
        self.suffix_regex = re.compile(f" *({'|'.join(self.suffixes)})")
        self.e_suffix_regex = re.compile(r" *E(-?\d+)")

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)

        number = ""
        decimal = ""

        match = self.decimal_regex.match(token)
        if match:
            number = match.group(1)
            decimal = match.group(2)
            token = match.group(3)
        else:
            match = self.number_regex.match(token)
            if match:
                number = match.group(1)
                token = match.group(2)

        match = self.suffix_regex.match(token)
        suffix = ""
        if match:
            suffix = match.group(1)
        else:
            match = self.e_suffix_regex.match(token)
            if match:
                suffix = f"nhân mười mũ {self.cardinal.convert(match.group(1))}"

        result_list = []
        if len(decimal) > 0:
            result_list.append("phẩy")
            result_list.append(self.digit.convert(decimal))

        if number:
            result_list.insert(0, self.cardinal.convert(number))

        if suffix:
            result_list.append(suffix)

        result = " ".join(result_list)

        return result

if __name__ == "__main__":
    decimal = Decimal()

    test_cases = [
        "123,456.789",
        "0.5",
        "1000000",
        "3.14",
        "2.718E3",
        "1.23E-5",
        "9.99999",
        "1234.5678 tỷ",
        "0.000001",
        "1000000.000001",
    ]

    for case in test_cases:
        result = decimal.convert(case)
        print(f"Số: {case}")
        print(f"Chuyển đổi: {result}")
        print()