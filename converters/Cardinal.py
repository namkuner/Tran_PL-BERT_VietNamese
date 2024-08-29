from typing import List

from singleton_decorator import singleton
import re
from .Roman import RomanVietnamese


@singleton
class CardinalVietnamese:
    """
    Các bước:
    - 1 Loại bỏ dấu chấm
    - 2 Kiểm tra xem có phải là số La Mã không
    - 3 Nếu đúng, chuyển đổi số La Mã lớn nhất tìm thấy thành số nguyên, sau đó thành chuỗi đại diện cho số nguyên đó
    - 4 Nếu đúng, kiểm tra xem có nên thêm hậu tố "'s" không (xem trường hợp đặc biệt)
    - 5 Lọc bỏ các ký tự không phải số, trừ "-"
    - 6 Kiểm tra xem có nên sử dụng tiền tố "âm" không
    - 7 Loại bỏ tất cả các ký tự "-" còn lại
    - 8 Nếu là "0", thêm "không" vào danh sách đầu ra
    - 9 Nếu không phải "0", chia chuỗi thành các phần tối đa 3 chữ số, sao cho phần nhỏ nhất bao gồm các ký tự ngoài cùng bên trái
    -   10 Chia mỗi phần thành `trăm` và `phần còn lại`
    -   11 Thêm "x trăm" nếu `trăm` > 0
    -   12 Thêm giá trị văn bản đại diện cho `phần còn lại`
    -   13 Thêm hậu tố cho phần, ví dụ: triệu, tỷ, v.v.
    -   14 Thêm đầu ra cho phần vào tổng đầu ra
    - 15 Kết hợp danh sách đầu ra tổng thành một chuỗi
    - 16 Thêm tiền tố và/hoặc hậu tố

    Trường hợp đặc biệt:
    II -> hai
    -2 -> âm hai
    I. -> một
    IV's -> bốn's

    Ghi chú:
    - Không có "và" hoặc dấu gạch ngang trong kết quả, ví dụ: không có "hai mươi mốt" hoặc "một trăm lẻ một"
    """

    def __init__(self):
        super().__init__()
        self.filter_regex = re.compile("[^0-9\-]")
        self.filter_strict_regex = re.compile("[^0-9]")
        self.dot_filter_regex = re.compile("[.]")

        self.scale_suffixes = [
            "nghìn",
            "triệu",
            "tỷ",
            "nghìn tỷ",
            "triệu tỷ",
            "tỷ tỷ"
        ]

        self.small_trans_dict = {
            "1": "một",
            "2": "hai",
            "3": "ba",
            "4": "bốn",
            "5": "năm",
            "6": "sáu",
            "7": "bảy",
            "8": "tám",
            "9": "chín",
        }

        self.tens_trans_dict = {
            "1": "mười",
            "2": "hai mươi",
            "3": "ba mươi",
            "4": "bốn mươi",
            "5": "năm mươi",
            "6": "sáu mươi",
            "7": "bảy mươi",
            "8": "tám mươi",
            "9": "chín mươi",
        }

        self.special_trans_dict = {
            11: "mười một",
            12: "mười hai",
            13: "mười ba",
            14: "mười bốn",
            15: "mười lăm",
            16: "mười sáu",
            17: "mười bảy",
            18: "mười tám",
            19: "mười chín"
        }

        self.roman = RomanVietnamese()

    def _give_chunk(self, num_str: str, size: int = 3) -> str:
        while num_str:
            yield num_str[-size:]
            num_str = num_str[:-size]

    def convert(self, token: str) -> str:
        token = self.dot_filter_regex.sub("", token)

        suffix = ""
        if self.roman.check_if_roman(token):
            token, suffix = self.roman.convert(token)

        token = self.filter_regex.sub("", token)

        prefix = ""
        while len(token) > 0 and token[0] == "-":
            token = token[1:]
            prefix = "âm" if prefix == "" else ""

        token = self.filter_strict_regex.sub("", token)

        if token == len(token) * "0":
            return "không"

        chunks = list(self._give_chunk(token))
        text_list = []

        for depth, chunk in enumerate(chunks):
            chunk_text = self._convert_chunk(chunk, depth == len(chunks) - 1)
            if chunk_text:
                if depth > 0:
                    chunk_text.append(self.scale_suffixes[depth - 1])
                text_list = chunk_text + text_list

        result = " ".join(text_list)

        if prefix:
            result = f"{prefix} {result}"
        if suffix:
            result = f"{result}{suffix}"

        return result

    def _convert_chunk(self, chunk: str, is_last_chunk: bool) -> List[str]:
        chunk_text = []
        length = len(chunk)

        # Xử lý hàng trăm
        if length == 3:
            if chunk[0] != '0':
                chunk_text.append(self.small_trans_dict[chunk[0]])
                chunk_text.append("trăm")
            elif not is_last_chunk and (chunk[1] != '0' or chunk[2] != '0'):
                chunk_text.append("không trăm")

        # Xử lý hàng chục và đơn vị
        if length >= 2:
            if chunk[-2:] in self.special_trans_dict:
                chunk_text.append(self.special_trans_dict[chunk[-2:]])
            else:
                if chunk[-2] != '0':
                    chunk_text.append(self.tens_trans_dict[chunk[-2]])
                    if chunk[-1] != '0':
                        if chunk[-1] == '1' and chunk[-2] != '1':
                            chunk_text.append("mốt")
                        else:
                            chunk_text.append(self.small_trans_dict[chunk[-1]])
                elif chunk[-1] != '0':
                    if len(chunk_text) > 0 or not is_last_chunk:
                        chunk_text.append("lẻ")
                    chunk_text.append(self.small_trans_dict[chunk[-1]])
        elif length == 1 and chunk != '0':
            chunk_text.append(self.small_trans_dict[chunk])

        return chunk_text

if __name__ == "__main__":
    cardinal_converter = CardinalVietnamese()

    # Ví dụ 1
    example1 = "20211231"
    result1 = cardinal_converter.convert(example1)
    print(f"Số: {example1}")
    print(f"Chuyển đổi: {result1}")
    print()

    # Ví dụ 2
    example2 = "-5678213"
    result2 = cardinal_converter.convert(example2)
    print(f"Số: {example2}")
    print(f"Chuyển đổi: {result2}")
    print()

    # Ví dụ 3
    example3 = "1000000"
    result3 = cardinal_converter.convert(example3)
    print(f"Số: {example3}")
    print(f"Chuyển đổi: {result3}")