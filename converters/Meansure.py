import re
from typing import List, Dict
from singleton_decorator import singleton
from .Decimal import Decimal
from .Fraction import Fraction
@singleton
class NormalizedMeasure:
    def __init__(self):
        self._init_regexes()
        self._init_dictionaries()
        self._init_converters()

    def _init_regexes(self):
        self.fraction_regex = re.compile(
            r"(((?:-?\d* )?-?\d+ *\/ *-? *\d+)|(-?\d* *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒)))")
        self.of_a_regex = re.compile(r"(-?\d+ -?\d+ *\/ *-? *\d+)|(-?\d+ *(?:½|⅓|⅔|¼|¾|⅕|⅖|⅗|⅘|⅙|⅚|⅐|⅛|⅜|⅝|⅞|⅑|⅒))")
        self.value_regex = re.compile(r"(-?(?: |\d)*\.?\d+ *(?:nghìn|triệu|tỷ|nghìn tỷ|triệu tỷ|tỷ tỷ)?)")
        self.filter_regex = re.compile(r"[,]")
        self.filter_space_regex = re.compile(r"[ ]")
        self.letter_filter_regex = re.compile(r"[^0-9\-\.]")
        self.special_suffixes = re.compile(r"(\/|trên(?!trăm)|vuông|2|²|3|³)")

    def _init_dictionaries(self):
        self.prefix_dict = {
            "Y": "yotta", "Z": "zetta", "E": "exa", "P": "peta", "T": "tera",
            "G": "giga", "M": "mega", "k": "kilo", "h": "hecto", "da": "deca",
            "d": "deci", "c": "centi", "m": "milli", "μ": "micro", "µ": "micro",
            "n": "nano", "p": "pico", "f": "femto", "a": "atto", "z": "zepto", "y": "yocto"
        }

        self.prefixable_trans_dict = {
            "m": {"singular": "mét", "plural": "mét"},
            "b": {"singular": "bit", "plural": "bit"},
            "B": {"singular": "byte", "plural": "byte"},
            "bps": {"singular": "bit trên giây", "plural": "bit trên giây"},
            "Bps": {"singular": "byte trên giây", "plural": "byte trên giây"},
            "g": {"singular": "gram", "plural": "gram"},
            "gf": {"singular": "gram lực", "plural": "gram lực"},
            "W": {"singular": "oát", "plural": "oát"},
            "Wh": {"singular": "oát giờ", "plural": "oát giờ"},
            "Hz": {"singular": "héc", "plural": "héc"},
            "J": {"singular": "jun", "plural": "jun"},
            "L": {"singular": "lít", "plural": "lít"},
            "V": {"singular": "vôn", "plural": "vôn"},
            "f": {"singular": "fara", "plural": "fara"},
            "s": {"singular": "giây", "plural": "giây"},
            "A": {"singular": "ampe", "plural": "ampe"},
            "Ah": {"singular": "ampe giờ", "plural": "ampe giờ"},
            "Pa": {"singular": "pascal", "plural": "pascal"},
            "C": {"singular": "culông", "plural": "culông"},
            "Bq": {"singular": "becquerel", "plural": "becquerel"},
            "N": {"singular": "niutơn", "plural": "niutơn"},
            "bar": {"singular": "bar", "plural": "bar"},
            "lm": {"singular": "lumen", "plural": "lumen"},
            "cal": {"singular": "calo", "plural": "calo"},
        }

        self.custom_dict = {
            "%": {"singular": "phần trăm", "plural": "phần trăm"},
            "pc": {"singular": "phần trăm", "plural": "phần trăm"},
            "ft": {"singular": "foot", "plural": "foot"},
            "mi": {"singular": "dặm", "plural": "dặm"},
            "mb": {"singular": "megabyte", "plural": "megabyte"},
            "ha": {"singular": "hecta", "plural": "hecta"},
            "\"": {"singular": "inch", "plural": "inch"},
            "in": {"singular": "inch", "plural": "inch"},
            "\'": {"singular": "foot", "plural": "foot"},
            "rpm": {"singular": "vòng trên phút", "plural": "vòng trên phút"},
            "hp": {"singular": "mã lực", "plural": "mã lực"},
            "cc": {"singular": "xăng-ti-mét khối", "plural": "xăng-ti-mét khối"},
            "oz": {"singular": "aoxơ", "plural": "aoxơ"},
            "mph": {"singular": "dặm trên giờ", "plural": "dặm trên giờ"},
            "lb": {"singular": "pao", "plural": "pao"},
            "lbs": {"singular": "pao", "plural": "pao"},
            "kt": {"singular": "nút", "plural": "nút"},
            "dB": {"singular": "đề-xi-ben", "plural": "đề-xi-ben"},
            "AU": {"singular": "đơn vị thiên văn", "plural": "đơn vị thiên văn"},
            "st": {"singular": "stone", "plural": "stone"},
            "yd": {"singular": "yard", "plural": "yard"},
            "yr": {"singular": "năm", "plural": "năm"},
            "yrs": {"singular": "năm", "plural": "năm"},
            "eV": {"singular": "electron vôn", "plural": "electron vôn"},
            "/": {"singular": "trên", "plural": "trên"},
            "sq": {"singular": "vuông", "plural": "vuông"},
            "2": {"singular": "vuông", "plural": "vuông"},
            "²": {"singular": "vuông", "plural": "vuông"},
            "3": {"singular": "khối", "plural": "khối"},
            "³": {"singular": "khối", "plural": "khối"},
            "h": {"singular": "giờ", "plural": "giờ"},
            "hr": {"singular": "giờ", "plural": "giờ"},
            "hrs": {"singular": "giờ", "plural": "giờ"},
            "ch": {"singular": "chain", "plural": "chain"},
            "KiB": {"singular": "kibibyte", "plural": "kibibyte"},
            "MiB": {"singular": "mebibyte", "plural": "mebibyte"},
            "GiB": {"singular": "gibibyte", "plural": "gibibyte"},
            "pH": {"singular": "pH", "plural": "pH"},
            "kph": {"singular": "kilômét trên giờ", "plural": "kilômét trên giờ"},
            "Da": {"singular": "đalton", "plural": "đalton"},
            "cwt": {"singular": "hundredweight", "plural": "hundredweight"},
            "Sv": {"singular": "sievert", "plural": "sievert"},
            "C": {"singular": "độ xen-xi-út", "plural": "độ xen-xi-út"},
            "degrees": {"singular": "độ", "plural": "độ"},
            "degree": {"singular": "độ", "plural": "độ"},
            "atm": {"singular": "át-mốt-phê", "plural": "át-mốt-phê"},
            "min": {"singular": "phút", "plural": "phút"},
            "cd": {"singular": "can-đê-la", "plural": "can-đê-la"},
            "ly": {"singular": "năm ánh sáng", "plural": "năm ánh sáng"},
            "kts": {"singular": "nút", "plural": "nút"},
            "mol": {"singular": "mol", "plural": "mol"},
            "Nm": {"singular": "niutơn mét", "plural": "niutơn mét"},
            "Ω": {"singular": "ôm", "plural": "ôm"},
            "bbl": {"singular": "thùng", "plural": "thùng"},
            "gal": {"singular": "gallon", "plural": "gallon"},
            "cal": {"singular": "cỡ nòng", "plural": "cỡ nòng"}
        }

        self.prefixed_dict = {
            prefix + prefixed: {
                "singular": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["singular"],
                "plural": self.prefix_dict[prefix] + self.prefixable_trans_dict[prefixed]["plural"]
            } for prefixed in self.prefixable_trans_dict for prefix in self.prefix_dict
        }
        self.prefixed_dict.update(self.prefixable_trans_dict)
        self.prefixed_dict.update(self.custom_dict)

        self.lower_prefixed_dict = {key.lower(): value for key, value in self.prefixed_dict.items()}

    def _init_converters(self):

        self.decimal = Decimal()
        self.fraction = Fraction()

    def split_token(self, token: str) -> List[str]:
        parts = re.findall(r'\d+|\D+', token)
        result = []
        for part in parts:
            if part.isdigit():
                result.append(part)
            else:
                result.extend(self.split_non_numeric(part))
        return result

    def split_non_numeric(self, token: str) -> List[str]:
        special_cases = ["km2", "m2", "km3", "m3"]
        for case in special_cases:
            if token.lower().startswith(case):
                return [token[:len(case)], token[len(case):]]
        return list(token)

    def convert(self, token: str) -> str:
        token = self.filter_regex.sub("", token)
        result_list = []
        plural = False

        fraction_match = self.fraction_regex.match(token)
        if fraction_match:
            result_list.append(self.fraction.convert(fraction_match.group(0)))
            token = token[:fraction_match.span()[0]] + token[fraction_match.span()[1]:]
            token = self.filter_space_regex.sub("", token)
            if self.of_a_regex.match(fraction_match.group(0)):
                plural = True
            else:
                result_list.append("của một")
        else:
            value_match = self.value_regex.match(token)
            if value_match:
                result_list.append(self.decimal.convert(self.filter_space_regex.sub("", value_match.group(1))))
                token = token[:value_match.span()[0]] + token[value_match.span()[1]:]
                if abs(float(self.letter_filter_regex.sub("", value_match.group(1)))) != 1 or "," in value_match.group(1):
                    plural = True

        per = False
        for split_token in token.split(" "):
            for i, token in enumerate(self.split_token(split_token)):
                if token in self.prefixed_dict:
                    result_list.append(self.prefixed_dict[token]["plural" if plural and not per else "singular"])
                elif token.lower() in self.lower_prefixed_dict:
                    result_list.append(self.lower_prefixed_dict[token.lower()]["plural" if plural and not per else "singular"])
                else:
                    result_list.append(token)

                if result_list[-1] == "trên" and i != 0:
                    per = True
                elif result_list[-1] not in ("vuông", "khối"):
                    per = False

        result = " ".join(result_list)
        result = re.sub(r"xentimét khối", "xăng-ti-mét khối", result)
        return result

# Sử dụng
# normalized_measure = NormalizedMeasure()
# print(normalized_measure.convert("5km2"))  # Ví dụ sử dụng