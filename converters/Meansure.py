from singleton_decorator import singleton

import re

from .Decimal import Decimal
from .Fraction import Fraction


@singleton
class Measure:
    def __init__(self):
        super().__init__()
        # Regex để phát hiện phân số
        self.fraction_regex = re.compile(
            r"(((?:-?\d* )?-?\d+ *\/ *-? *\d+)|(-?\d* *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒)))")
        # Regex để phát hiện xem có nên sử dụng "của một" hay không
        self.of_a_regex = re.compile(r"(-?\d+ -?\d+ *\/ *-? *\d+)|(-?\d+ *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒))")
        # Regex để phát hiện đầu vào để chuyển đổi số, bao gồm cả hậu tố triệu/tỷ tiềm năng
        self.value_regex = re.compile(r"(-?(?: |\d)*\.?\d+ *(?:nghìn|triệu|tỷ|nghìn tỷ|triệu tỷ|tỷ tỷ)?)")
        # Regex để lọc bỏ dấu phẩy
        self.filter_regex = re.compile(r"[,]")
        # Regex để lọc bỏ khoảng trắng
        self.filter_space_regex = re.compile(r"[ ]")
        # Regex để lọc bỏ chữ cái
        self.letter_filter_regex = re.compile(r"[^0-9\-\.]")

        # Từ điển tiền tố cho 10^i với i > 0
        self.prefix_dict = {
            "Y": "yotta",
            "Z": "zetta",
            "E": "exa",
            "P": "peta",
            "T": "tera",
            "G": "giga",
            "M": "mega",
            "k": "kilo",
            "h": "hecto",
            "da": "deca",
            "d": "deci",
            "c": "centi",
            "m": "milli",
            "μ": "micro",
            "µ": "micro",
            "n": "nano",
            "p": "pico",
            "f": "femto",
            "a": "atto",
            "z": "zepto",
            "y": "yocto"
        }

        # Từ điển dịch cho các loại đơn vị có thể thêm tiền tố
        self.prefixable_trans_dict = {
            "m": {
                "singular": "mét",
                "plural": "mét"
            },
            "b": {
                "singular": "bit",
                "plural": "bit"
            },
            "B": {
                "singular": "byte",
                "plural": "byte"
            },
            "bps": {
                "singular": "bit trên giây",
                "plural": "bit trên giây"
            },
            "Bps": {
                "singular": "byte trên giây",
                "plural": "byte trên giây"
            },
            "g": {
                "singular": "gram",
                "plural": "gram"
            },
            "gf": {
                "singular": "gram lực",
                "plural": "gram lực"
            },
            "W": {
                "singular": "oát",
                "plural": "oát"
            },
            "Wh": {
                "singular": "oát giờ",
                "plural": "oát giờ"
            },
            "Hz": {
                "singular": "héc",
                "plural": "héc"
            },
            "J": {
                "singular": "jun",
                "plural": "jun"
            },
            "L": {
                "singular": "lít",
                "plural": "lít"
            },
            "V": {
                "singular": "vôn",
                "plural": "vôn"
            },
            "f": {
                "singular": "fara",
                "plural": "fara"
            },
            "s": {
                "singular": "giây",
                "plural": "giây"
            },
            "A": {
                "singular": "ampe",
                "plural": "ampe"
            },
            "Ah": {
                "singular": "ampe giờ",
                "plural": "ampe giờ"
            },
            "Pa": {
                "singular": "pascal",
                "plural": "pascal"
            },
            "C": {
                "singular": "culông",
                "plural": "culông"
            },
            "Bq": {
                "singular": "becquerel",
                "plural": "becquerel"
            },
            "N": {
                "singular": "niutơn",
                "plural": "niutơn"
            },
            "bar": {
                "singular": "bar",
                "plural": "bar"
            },
            "lm": {
                "singular": "lumen",
                "plural": "lumen"
            },
            "cal": {
                "singular": "calo",
                "plural": "calo"
            },
        }

        # Từ điển đã được biến đổi sử dụng self.prefixable_trans_dict và từ điển tiền tố
        self.prefixed_dict = {
            prefix + prefixed: {"singular": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["singular"],
                                "plural": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["plural"]} for
            prefixed in self.prefixable_trans_dict for prefix in self.prefix_dict}
        self.prefixed_dict = {**self.prefixed_dict, **self.prefixable_trans_dict}

        # Từ điển dịch cho các loại đơn vị không có tiền tố
        self.custom_dict = {
            "%": {
                "singular": "phần trăm",
                "plural": "phần trăm"
            },
            "pc": {
                "singular": "phần trăm",
                "plural": "phần trăm"
            },
            "ft": {
                "singular": "foot",
                "plural": "foot"
            },
            "mi": {
                "singular": "dặm",
                "plural": "dặm"
            },
            "mb": {
                "singular": "megabyte",
                "plural": "megabyte"
            },
            "ha": {
                "singular": "hecta",
                "plural": "hecta"
            },
            "\"": {
                "singular": "inch",
                "plural": "inch"
            },
            "in": {
                "singular": "inch",
                "plural": "inch"
            },
            "\'": {
                "singular": "foot",
                "plural": "foot"
            },
            "rpm": {
                "singular": "vòng trên phút",
                "plural": "vòng trên phút"
            },
            "hp": {
                "singular": "mã lực",
                "plural": "mã lực"
            },
            "cc": {
                "singular": "xăng-ti-mét khối",
                "plural": "xăng-ti-mét khối"
            },
            "oz": {
                "singular": "aoxơ",
                "plural": "aoxơ",
            },
            "mph": {
                "singular": "dặm trên giờ",
                "plural": "dặm trên giờ"
            },
            "lb": {
                "singular": "pao",
                "plural": "pao"
            },
            "lbs": {
                "singular": "pao",
                "plural": "pao"
            },
            "kt": {
                "singular": "nút",
                "plural": "nút"
            },
            "dB": {
                "singular": "đề-xi-ben",
                "plural": "đề-xi-ben"
            },
            "AU": {
                "singular": "đơn vị thiên văn",
                "plural": "đơn vị thiên văn"
            },
            "st": {
                "singular": "stone",
                "plural": "stone"
            },
            "yd": {
                "singular": "yard",
                "plural": "yard"
            },
            "yr": {
                "singular": "năm",
                "plural": "năm"
            },
            "yrs": {
                "singular": "năm",
                "plural": "năm"
            },
            "eV": {
                "singular": "electron vôn",
                "plural": "electron vôn"
            },
            "/": {
                "singular": "trên",
                "plural": "trên"
            },
            "sq": {
                "singular": "vuông",
                "plural": "vuông"
            },
            "2": {
                "singular": "vuông",
                "plural": "vuông"
            },
            "²": {
                "singular": "vuông",
                "plural": "vuông"
            },
            "3": {
                "singular": "khối",
                "plural": "khối"
            },
            "³": {
                "singular": "khối",
                "plural": "khối"
            },
            "h": {
                "singular": "giờ",
                "plural": "giờ"
            },
            "hr": {
                "singular": "giờ",
                "plural": "giờ"
            },
            "hrs": {
                "singular": "giờ",
                "plural": "giờ"
            },
            "ch": {
                "singular": "chain",
                "plural": "chain"
            },
            "KiB": {
                "singular": "kibibyte",
                "plural": "kibibyte"
            },
            "MiB": {
                "singular": "mebibyte",
                "plural": "mebibyte"
            },
            "GiB": {
                "singular": "gibibyte",
                "plural": "gibibyte"
            },
            "pH": {
                "singular": "pH",
                "plural": "pH"
            },
            "kph": {
                "singular": "kilômét trên giờ",
                "plural": "kilômét trên giờ"
            },
            "Da": {
                "singular": "đalton",
                "plural": "đalton"
            },
            "cwt": {
                "singular": "hundredweight",
                "plural": "hundredweight"
            },
            "Sv": {
                "singular": "sievert",
                "plural": "sievert",
            },
            "C": {
                "singular": "độ xen-xi-út",
                "plural": "độ xen-xi-út"
            },
            "degrees": {
                "singular": "độ",
                "plural": "độ"
            },
            "degree": {
                "singular": "độ",
                "plural": "độ"
            },
            "atm": {
                "singular": "át-mốt-phê",
                "plural": "át-mốt-phê"
            },
            "min": {
                "singular": "phút",
                "plural": "phút"
            },
            "cd": {
                "singular": "can-đê-la",
                "plural": "can-đê-la"
            },
            "ly": {
                "singular": "năm ánh sáng",
                "plural": "năm ánh sáng"
            },
            "kts": {
                "singular": "nút",
                "plural": "nút"
            },
            "mol": {
                "singular": "mol",
                "plural": "mol"
            },
            "Nm": {
                "singular": "niutơn mét",
                "plural": "niutơn mét"
            },
            "Ω": {
                "singular": "ôm",
                "plural": "ôm"
            },
            "bbl": {
                "singular": "thùng",
                "plural": "thùng"
            },
            "gal": {
                "singular": "gallon",
                "plural": "gallon"
            },
            "cal": {
                "singular": "cỡ nòng",
                "plural": "cỡ nòng"
            }
        }

        # Ghi đè và thêm giá trị từ custom_dict vào prefixed_dict
        self.prefixed_dict = {**self.prefixed_dict, **self.custom_dict}

        # Phiên bản viết thường của self.prefixed_dict
        self.lower_prefixed_dict = {key.lower(): self.prefixed_dict[key] for key in self.prefixed_dict}

        # Hậu tố đặc biệt mà tổng hậu tố nên được tách ra
        self.special_suffixes = re.compile(r"(\/|trên(?!trăm)|vuông|2|²|3|³)")

        # Chuyển đổi Decimal và Fraction
        self.decimal = Decimal()
        self.fraction = Fraction()


    def convert(self, token: str) -> str:
        # 1 Lọc bỏ dấu phẩy
        token = self.filter_regex.sub("", token)

        result_list = []

        # Số nhiều mặc định là false, vì "/s" nên là "trên giây"
        plural = False

        # 2 Thử khớp với một phân số
        match = self.fraction_regex.match(token)
        if match:
            # 2.1 Nếu tồn tại, chuyển đổi thành văn bản sử dụng bộ chuyển đổi Fraction
            result_list.append(self.fraction.convert(match.group(0)))
            # Chuyển token thành phần còn lại. Vì sử dụng match thay vì search,
            # phần đầu của dòng tiếp theo có thể không cần thiết
            token = token[:match.span()[0]] + token[match.span()[1]:]

            # Lọc bỏ khoảng trắng
            token = self.filter_space_regex.sub("", token)

            # Nếu có một số trước phân số, ví dụ "8 1/2" hoặc "8 ½", thì chúng ta thêm "của một", và giữ nguyên số ít
            # Ngược lại, chúng ta chuyển sang số nhiều
            if self.of_a_regex.match(match.group(0)):
                plural = True
            else:
                result_list.append("của một")

        else:
            # 3 Thử khớp với "x,y" hoặc "x"
            match = self.value_regex.match(token)
            if match:
                # 3.1 Chuyển không có khoảng trắng cho bộ chuyển đổi decimal
                result_list.append(self.decimal.convert(self.filter_space_regex.sub("", match.group(1))))
                token = token[:match.span()[0]] + token[match.span()[1]:]
                # Số nhiều là False khi giá trị tuyệt đối của số thập phân là 1, và giá trị thập phân không có dạng "1,x"
                # Ngược lại là True
                if abs(float(self.letter_filter_regex.sub("", match.group(1)))) != 1 or "," in match.group(1):
                    plural = True

        # Biến chỉ ra liệu từ "trên" vừa được sử dụng
        # Điều này được sử dụng để phát hiện số nhiều
        per = False
        # 4 Lặp qua phần còn lại của token
        for split_token in token.split(" "):
            for i, token in enumerate(self.split_token(split_token)):
                # Thêm tên thích hợp của hậu tố nếu tồn tại
                # Thử không phân biệt chữ hoa chữ thường nếu lần trước thất bại
                if token in self.prefixed_dict:
                    result_list.append(self.prefixed_dict[token]["plural" if plural and not per else "singular"])
                elif token.lower() in self.lower_prefixed_dict:
                    result_list.append(
                        self.lower_prefixed_dict[token.lower()]["plural" if plural and not per else "singular"])
                else:
                    result_list.append(token)

                # Nếu kết quả trước đó là "trên", đặt per thành True để sử dụng "singular" cho từ tiếp theo.
                # Nhưng chỉ khi "trên" không phải là hậu tố đầu tiên. Ví dụ: "5/km2" là "năm trên kilômét vuông"
                if result_list[-1] == "trên" and i != 0:
                    per = True

                # Nếu từ cuối cùng không phải là "trên", và không phải "vuông" hoặc "khối", đặt lại per thành False.
                # Nếu "trên" được sử dụng, tiếp theo là "vuông" hoặc "khối", chúng ta muốn giữ "singular" cho
                # từ sắp tới
                elif result_list[-1] not in ("vuông", "khối"):
                    per = False

        result = " ".join(result_list)

        # 5 Xử lý trường hợp đặc biệt: xentimét khối -> xăng-ti-mét khối
        result = re.sub(r"xentimét khối", "xăng-ti-mét khối", result)

        return result