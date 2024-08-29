from singleton_decorator import singleton
import re


@singleton
class RomanVietnamese:
    """
    Các bước:
    - 1 Lấy phần lớn nhất
    - 2 Kiểm tra hậu tố 's'
    - 3 Áp dụng lọc nghiêm ngặt
    - 4 Tính tổng giá trị của chữ số La Mã bằng số nguyên
    - 5 Trả về biểu diễn chuỗi của tổng, cùng với hậu tố
    Trường hợp đặc biệt:
    II I -> hai
    IIs  -> hai's
    II.  -> hai
    """

    def __init__(self):
        super().__init__()
        # Regex để lọc bỏ các ký tự không phải chữ số La Mã
        self.roman_filter_strict_regex = re.compile("[^IVXLCDM]")
        # Regex để phát hiện chữ số La Mã
        self.roman_filter_regex = re.compile(r"[.IVXLCDM]+(th|nd|st|rd|'s|s)?")

        # Từ điển giá trị chữ số La Mã
        self.roman_numerals = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }



    def convert(self, token: str) -> (str, str):
        # 1 Tách token thành các phần và làm việc với phần lớn nhất, trong trường hợp đầu vào là "I II"
        token = max(token.split(" "), key=len)
        # 2 Kiểm tra xem có cần sử dụng hậu tố "'s" không
        suffix = ""
        if token[-1:] == "s":
            suffix = "'s"

        # 3 Áp dụng lọc nghiêm ngặt để loại bỏ ".", "'" và "s"
        token = self.roman_filter_strict_regex.sub("", token)
        # 4 Chúng ta lặp qua token theo chiều ngược lại, liên tục cộng hoặc trừ giá trị được biểu diễn
        # bởi ký tự, dựa trên các token trước đó.
        total = 0
        prev = 0
        for c in reversed(token):
            cur = self.roman_numerals[c]
            total += cur if cur >= prev else -cur
            prev = cur

        return (str(total), suffix)


    def check_if_roman(self, token: str) -> bool:
        # Kiểm tra xem phần lớn nhất của token có được coi là chữ số La Mã hay không
        return self.roman_filter_regex.fullmatch(max(token.split(" "), key=len)) != None


if __name__ == "__main__":
    roman_converter = RomanVietnamese()

    # Ví dụ 1
    example1 = "XIV"
    result1, suffix1 = roman_converter.convert(example1)
    print(f"Chữ số La Mã: {example1}")
    print(f"Chuyển đổi: {result1}{suffix1}")
    print()

    # Ví dụ 2
    example2 = "MCMLIV"
    result2, suffix2 = roman_converter.convert(example2)
    print(f"Chữ số La Mã: {example2}")
    print(f"Chuyển đổi: {result2}{suffix2}")
    print()

    # Ví dụ 3
    example3 = "IIs"
    result3, suffix3 = roman_converter.convert(example3)
    print(f"Chữ số La Mã: {example3}")
    print(f"Chuyển đổi: {result3}{suffix3}")