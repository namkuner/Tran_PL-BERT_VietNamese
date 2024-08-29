from singleton_decorator import singleton
import re, os
from .Cardinal import CardinalVietnamese
from .Digit import DigitVietnamese


@singleton
class Money:
    def __init__(self):
        super().__init__()
        self.decimal_regex = re.compile(r"(.*?)(-?\d*)\.(\d+)(.*)")
        self.number_regex = re.compile(r"(.*?)(-?\d+)(.*)")
        self.filter_regex = re.compile(r"[, ]")

        self.currencies = {
            "đ": {
                "number": {
                    "singular": "đồng",
                    "plural": "đồng"
                },
                "decimal": {
                    "singular": "xu",
                    "plural": "xu"
                }
            },
            "vnd": {
                "number": {
                    "singular": "đồng Việt Nam",
                    "plural": "đồng Việt Nam"
                },
                "decimal": {
                    "singular": "xu",
                    "plural": "xu"
                }
            }
        }

        self.suffixes = [
            "nghìn",
            "triệu",
            "tỷ",
            "nghìn tỷ",
            "triệu tỷ",
            "tỷ tỷ"
        ]

        self.abbr_suffixes = {
            "k": "nghìn",
            "tr": "triệu",
            "t": "tỷ"
        }

        self.suffix_regex = re.compile(
            f"({'|'.join(sorted(self.suffixes + list(self.abbr_suffixes.keys()), key=len, reverse=True))})(.*)",
            flags=re.I)

        self.currency_regex = re.compile(r"(.*?)(đồng|vnd|đ)(.*?)", flags=re.I)

        self.cardinal = CardinalVietnamese()  # Giả sử đã có lớp Cardinal cho tiếng Việt
        self.digit = DigitVietnamese()  # Giả sử đã có lớp Digit cho tiếng Việt

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)

        before = ""
        after = ""
        currency = None
        number = ""
        decimal = ""
        scale = ""

        match = self.decimal_regex.search(token[::-1])
        if match:
            before = match.group(4)[::-1]
            number = match.group(3)[::-1]
            decimal = match.group(2)[::-1]
            after = match.group(1)[::-1]
        else:
            match = self.number_regex.search(token)
            if match:
                before = match.group(1)
                number = match.group(2)
                after = match.group(3)

        if before:
            before = before.lower()
            if before in self.currencies:
                currency = self.currencies[before]
            elif before[-1] in self.currencies:
                currency = self.currencies[before[-1]]

        if after:
            match = self.suffix_regex.match(after)
            if match:
                scale = match.group(1).lower()
                scale = self.abbr_suffixes[scale] if scale in self.abbr_suffixes else scale
                after = match.group(2)

            if after.lower() in self.currencies:
                currency = self.currencies[after.lower()]
                after = ""

        decimal_support = currency and "number" in currency

        result_list = []
        if decimal_support and not scale:
            if number and (number != "0" or not decimal):
                result_list.append(self.cardinal.convert(number))
                result_list.append(currency["number"]["singular"])
                if decimal and decimal != "0" * len(decimal):
                    result_list.append("và")
            if decimal and decimal != "0" * len(decimal):
                decimal = f"{decimal:0<2}"
                result_list.append(self.cardinal.convert(decimal))
                result_list.append(currency["decimal"]["singular"])
        else:
            if number:
                result_list.append(self.cardinal.convert(number))
            if decimal and decimal != "0" * len(decimal):
                result_list.append("phẩy")
                result_list.append(self.digit.convert(decimal))
            if scale:
                result_list.append(scale)
            if currency:
                if decimal_support:
                    currency = currency["number"]
                result_list.append(currency["singular"])

        if after:
            result_list.append(after.lower())

        result = " ".join(result_list)
        return result


if __name__ == "__main__":
    money = Money()

    # Ví dụ 1: Số tiền đơn giản
    print(money.convert("15000đ"))  # Kết quả mong đợi: mười lăm nghìn đồng

    # Ví dụ 2: Số tiền có phần thập phân
    print(money.convert("1500.50đ"))  # Kết quả mong đợi: một nghìn năm trăm đồng và năm mươi xu

    # Ví dụ 3: Số tiền lớn
    print(money.convert("1000000000đ"))  # Kết quả mong đợi: một tỷ đồng

    # Ví dụ 4: Sử dụng VND
    print(money.convert("5000000VND"))  # Kết quả mong đợi: năm triệu đồng Việt Nam

    # Ví dụ 5: Sử dụng hậu tố
    print(money.convert("2tr đồng"))  # Kết quả mong đợi: hai triệu đồng

    # Ví dụ 6: Số tiền rất lớn
    print(money.convert("1000000000000đ"))  # Kết quả mong đợi: một nghìn tỷ đồng