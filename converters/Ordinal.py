from singleton_decorator import singleton
import re
from Roman import RomanVietnamese
from Cardinal import CardinalVietnamese


@singleton
class OrdinalVietnamese:
    """
    Các bước:
    - 1 Lọc bỏ dấu phẩy và khoảng trắng
    - 2 Kiểm tra số La Mã và chuyển đổi thành chuỗi số nguyên nếu có
    - 3 Nếu là số La Mã, đặt tiền tố là "thứ"
    - 4 Nếu không, kiểm tra xem có phải là số thứ tự tiếng Việt không (ví dụ: "thứ nhất", "thứ 2", "thứ ba")
    - 5 Chuyển đổi chuỗi số còn lại thành Cardinal, và thêm "thứ" vào trước
    - 6 Áp dụng các quy tắc đặc biệt cho số thứ tự tiếng Việt
    """

    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile(r"[, ]")
        self.vietnamese_ordinal_regex = re.compile(r"(?i)(thứ\s*)?(\d+|nhất|nhì|hai|ba|tư|năm|sáu|bảy|tám|chín|mười)")
        self.roman = RomanVietnamese()
        self.cardinal = CardinalVietnamese()

        self.special_cases = {
            "nhất": "thứ nhất",
            "nhì": "thứ nhì",
            "hai": "thứ hai",
            "ba": "thứ ba",
            "tư": "thứ tư",
            "năm": "thứ năm",
            "sáu": "thứ sáu",
            "bảy": "thứ bảy",
            "tám": "thứ tám",
            "chín": "thứ chín",
            "mười": "thứ mười"
        }

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)

        if self.roman.check_if_roman(token):
            number, _ = self.roman.convert(token)

            return f"thứ {number}"

        match = self.vietnamese_ordinal_regex.fullmatch(token)
        if match:
            prefix = match.group(1) or ""
            number = match.group(2)

            if number.lower() in self.special_cases:
                return self.special_cases[number.lower()]

            if number.isdigit():
                cardinal = self.cardinal.convert(number)
                return f"thứ {cardinal}"

            return f"{prefix}{number}"

        return f"thứ {self.cardinal.convert(token)}"


if __name__ == "__main__":
    ordinal_converter = OrdinalVietnamese()

    examples = ["nhất", "thứ nhì", "thứ 3", "thứ tư", "thứ năm", "thứ 10", "21", "100", "1000", "II", "IV"]

    for example in examples:
        result = ordinal_converter.convert(example)
        print(f"Số thứ tự: {example}")
        print(f"Chuyển đổi: {result}")
        print()