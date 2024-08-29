from singleton_decorator import singleton
import re

@singleton
class DigitVietnamese:
    """
    Các bước:
    - 1 Lọc bỏ tất cả các ký tự không phải số
    - 2 Kiểm tra trường hợp đặc biệt
    - 3 Chuyển đổi mỗi chữ số thành văn bản tiếng Việt
    - 4 Thêm khoảng trắng giữa các từ
    Trường hợp đặc biệt:
    007 -> không không bảy
    trong khi 003 -> không không ba
    """
    def __init__(self):
        super().__init__()
        # Regex để lọc bỏ các ký tự không phải số
        self.filter_regex = re.compile("[^0-9]")
        # Từ điển chuyển đổi chữ số sang chữ tiếng Việt
        self.trans_dict = {
            "0": "không",
            "1": "một",
            "2": "hai",
            "3": "ba",
            "4": "bốn",
            "5": "năm",
            "6": "sáu",
            "7": "bảy",
            "8": "tám",
            "9": "chín"
        }

    def convert(self, token: str) -> str:
        # 1 Lọc bỏ tất cả các ký tự không phải số
        token = self.filter_regex.sub("", token)
        # 2 Kiểm tra trường hợp đặc biệt
        if token == "007":
            return "không không bảy"
        # 3 & 4 Chuyển đổi mỗi chữ số thành văn bản và thêm khoảng trắng
        token = " ".join([self.trans_dict[c] for c in token])
        return token
if __name__ == "__main__":
    # Tạo một thể hiện của lớp DigitVietnamese
    digit_converter = DigitVietnamese()

    # Ví dụ 1: Số điện thoại
    phone_number = "0912345678"
    print(f"Số điện thoại: {phone_number}")
    print(f"Chuyển đổi: {digit_converter.convert(phone_number)}")
    print()

    # Ví dụ 2: Mã số sinh viên
    student_id = "SV20210001"
    print(f"Mã số sinh viên: {student_id}")
    print(f"Chuyển đổi: {digit_converter.convert(student_id)}")
    print()

    # Ví dụ 3: Trường hợp đặc biệt
    special_case = "007"
    print(f"Số đặc biệt: {special_case}")
    print(f"Chuyển đổi: {digit_converter.convert(special_case)}")
