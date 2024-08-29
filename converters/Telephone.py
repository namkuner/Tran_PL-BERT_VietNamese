from singleton_decorator import singleton
import re


@singleton
class TelephoneVietnamese:
    """
    Các bước:
    - 1 Chuyển đổi thành chữ thường và thay thế dấu ngoặc đơn bằng dấu gạch ngang
    - 2 Chuyển đổi từng ký tự trong token
    - 3 Loại bỏ nhiều "ngat" liên tiếp. Đồng thời loại bỏ "ngat" ở đầu.
    - 4 Thay thế các "khong" liên tiếp bằng "tram" hoặc "nghin" khi thích hợp
    Lưu ý:
    Số điện thoại chứa 0-9, "-", a-z, A-Z, " ", "(", ")"
    """

    def __init__(self):
        super().__init__()
        # Từ điển dịch
        self.tu_dien_dich = {
            " ": "ngat",
            "-": "ngat",
            "x": "may_nhanh",
            "0": "không",
            "1": "môt",
            "2": "hai",
            "3": "ba",
            "4": "bốn",
            "5": "năm",
            "6": "sáu",
            "7": "bảy",
            "8": "tám",
            "9": "chín",
        }
        # Regex để lọc dấu ngoặc đơn
        self.regex_loc = re.compile(r"[()]")

    def convert(self, token: str) -> str:
        # 1 Chuyển đổi thành chữ thường và thay thế dấu ngoặc đơn bằng dấu gạch ngang
        token = self.regex_loc.sub("-", token.lower())

        # 2 Chuyển đổi danh sách các ký tự
        danh_sach_ket_qua = [self.tu_dien_dich[c] if c in self.tu_dien_dich else c for c in token]

        # 3 Loại bỏ nhiều "ngat" liên tiếp. Đồng thời loại bỏ "ngat" ở đầu.
        danh_sach_ket_qua = [phan for i, phan in enumerate(danh_sach_ket_qua) if
                             phan != "ngat" or (i - 1 >= 0 and danh_sach_ket_qua[i - 1] != "ngat")]

        # 4 Lặp qua danh_sach_ket_qua và thay thế nhiều "khong" liên tiếp bằng "tram" hoặc "nghin",
        # nhưng chỉ khi đứng trước là thứ khác ngoài "khong" hoặc "ngat", và đứng sau là "ngat" hoặc kết thúc danh sách.
        i = 0
        while i < len(danh_sach_ket_qua):
            do_lech = 0
            while i + do_lech < len(danh_sach_ket_qua) and danh_sach_ket_qua[i + do_lech] == "khong":
                do_lech += 1
            if (i + do_lech >= len(danh_sach_ket_qua) or danh_sach_ket_qua[i + do_lech] == "ngat") and (
                    i - 1 < 0 or danh_sach_ket_qua[i - 1] not in ("khong", "ngat")) and do_lech in (2, 3):
                danh_sach_ket_qua[i: do_lech + i] = ["tram"] if do_lech == 2 else ["nghin"]
            i += 1

        return " ".join(danh_sach_ket_qua)


def main():
    so_dien_thoai = TelephoneVietnamese()

    # Ví dụ sử dụng
    cac_vi_du = [
        "0123-456-789",
        "(098) 765-4321",
        "0909 333 222",
        "1800 1560",
        "19001560",
        "0336444027",
        "+84-912345678",
    ]

    print("Ví dụ chuyển đổi số điện thoại:")
    for vi_du in cac_vi_du:
        ket_qua = so_dien_thoai.convert(vi_du)
        print(f"Gốc: {vi_du}")
        print(f"Kết quả: {ket_qua}")
        print()


if __name__ == "__main__":
    # main()
    x ="027321"
    if x.startswith(("19", "18", "0")):
        print(1)