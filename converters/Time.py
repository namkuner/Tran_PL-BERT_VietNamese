from singleton_decorator import singleton
import re
from .Cardinal import CardinalVietnamese


@singleton
class Time:
    def __init__(self):
        super().__init__()

        self.filter_regex = re.compile(r"[. ]")
        self.time_regex = re.compile(r"^(?P<hour>\d{1,2}) *((?::|.) *(?P<minute>\d{1,2}))? *(?P<suffix>[a-zA-Z\. ]*)$",
                                     flags=re.I)
        self.full_time_regex = re.compile(
            r"^(?:(?P<hour>\d{1,2}) *:)? *(?P<minute>\d{1,2})(?: *: *(?P<seconds>\d{1,2})(?: *. *(?P<milliseconds>\d{1,3}))?)? *(?P<suffix>[a-zA-Z\. ]*)$",
            flags=re.I)
        self.ampm_time_regex = re.compile(r"^(?P<suffix>[a-zA-Z\. ]*)(?P<hour>\d{1,2})", flags=re.I)

        self.cardinal = CardinalVietnamese()

    def convert(self, token: str) -> str:
        token = token.strip()
        result_list = []

        match = self.time_regex.match(token)
        if match:
            hour, minute, suffix = match.group("hour"), match.group("minute"), match.group("suffix")

            result_list.append(self.cardinal.convert(hour))
            result_list.append("giờ")

            if minute and minute != "00":
                result_list.append(self.cardinal.convert(minute))
                result_list.append("phút")

            if suffix:
                suffix = self.filter_regex.sub("", suffix).lower()
                if suffix == "sa":
                    result_list.append("sáng")
                elif suffix == "ch":
                    result_list.append("chiều")

            return " ".join(result_list)

        match = self.full_time_regex.match(token)
        if match:
            hour, minute, seconds, milliseconds, suffix = match.group("hour"), match.group("minute"), match.group(
                "seconds"), match.group("milliseconds"), match.group("suffix")

            if hour:
                result_list.append(self.cardinal.convert(hour))
                result_list.append("giờ")
            if minute:
                result_list.append(self.cardinal.convert(minute))
                result_list.append("phút")
            if seconds:
                result_list.append(self.cardinal.convert(seconds))
                result_list.append("giây")
            if milliseconds:
                result_list.append(self.cardinal.convert(milliseconds))
                result_list.append("phần nghìn giây")

            if suffix:
                suffix = self.filter_regex.sub("", suffix).lower()
                if suffix == "sa":
                    result_list.append("sáng")
                elif suffix == "ch":
                    result_list.append("chiều")

            return " ".join(result_list)

        match = self.ampm_time_regex.match(token)
        if match:
            hour, suffix = match.group("hour"), match.group("suffix")

            result_list.append(self.cardinal.convert(hour))
            result_list.append("giờ")

            suffix = self.filter_regex.sub("", suffix).lower()
            if suffix == "sa":
                result_list.append("sáng")
            elif suffix == "ch":
                result_list.append("chiều")

            return " ".join(result_list)

        return token


if __name__ == "__main__":
    time = Time()

    print(time.convert("7:30"))  # Kết quả mong đợi: bảy giờ ba mươi phút
    print(time.convert("8:00 SA"))  # Kết quả mong đợi: tám giờ sáng
    print(time.convert("3:00 CH"))  # Kết quả mong đợi: ba giờ chiều
    print(time.convert(
        "11:59:59.999"))  # Kết quả mong đợi: mười một giờ năm mươi chín phút năm mươi chín giây chín trăm chín mươi chín phần nghìn giây
    print(time.convert("SA7"))  # Kết quả mong đợi: bảy giờ sáng
    print(time.convert("CH5"))  # Kết quả mong đợi: năm giờ chiều
    print(time.convert("9:30:21"))  # Kết quả mong đợi: năm giờ chiều