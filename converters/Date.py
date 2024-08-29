import re
from singleton_decorator import singleton
import re
from .Cardinal import CardinalVietnamese
import re

@singleton
class DateVietnamese:
    """
    Chuyển đổi ngày tháng từ dạng số sang dạng chữ tiếng Việt.
    Hỗ trợ các định dạng: "DD/MM/YYYY", "DD-MM-YYYY", "DD.MM.YYYY".
    Ví dụ: "25/12/2023", "01-01-2024", "10.05.2023"
    """

    def __init__(self):
        self.day_trans_dict = {
            "1": "một",
            "2": "hai",
            "3": "ba",
            "4": "bốn",
            "5": "năm",
            "6": "sáu",
            "7": "bảy",
            "8": "tám",
            "9": "chín",
            "10": "mười",
            "11": "mười một",
            "12": "mười hai",
            "13": "mười ba",
            "14": "mười bốn",
            "15": "mười lăm",
            "16": "mười sáu",
            "17": "mười bảy",
            "18": "mười tám",
            "19": "mười chín",
            "20": "hai mươi",
            "21": "hai mươi mốt",
            "22": "hai mươi hai",
            "23": "hai mươi ba",
            "24": "hai mươi bốn",
            "25": "hai mươi lăm",
            "26": "hai mươi sáu",
            "27": "hai mươi bảy",
            "28": "hai mươi tám",
            "29": "hai mươi chín",
            "30": "ba mươi",
            "31": "ba mươi mốt"
        }

        self.month_trans_dict = {
            "1": "một",
            "2": "hai",
            "3": "ba",
            "4": "tư",
            "5": "năm",
            "6": "sáu",
            "7": "bảy",
            "8": "tám",
            "9": "chín",
            "10": "mười",
            "11": "mười một",
            "12": "mười hai"
        }

    def convert_year(self, year: str) -> str:
        cardinal_converter = CardinalVietnamese()
        return cardinal_converter.convert(year)

    def convert_date(self, date: str) -> str:
        # Tìm và tách ngày, tháng, năm dựa trên dấu phân cách
        date_parts = re.split(r"[\/\-\.\s]", date)

        day, month, year = date_parts[0], date_parts[1], date_parts[2]

        day_text = f"ngày {self.day_trans_dict[day.lstrip('0')]}"
        month_text = f"tháng {self.month_trans_dict[month.lstrip('0')]}"
        year_text = f"năm {self.convert_year(year)}"

        return f"{day_text} {month_text} {year_text}"

if __name__ == "__main__":
    date_converter = DateVietnamese()

    # Ví dụ 1
    example1 = "25/12/1990"
    result1 = date_converter.convert_date(example1)
    print(f"Ngày tháng: {example1}")
    print(f"Chuyển đổi: {result1}")
    print()

    # Ví dụ 2
    example2 = "01-01-1991"
    result2 = date_converter.convert_date(example2)
    print(f"Ngày tháng: {example2}")
    print(f"Chuyển đổi: {result2}")
    print()

    # Ví dụ 3
    example3 = "10.05.2023"
    result3 = date_converter.convert_date(example3)
    print(f"Ngày tháng: {example3}")
    print(f"Chuyển đổi: {result3}")

