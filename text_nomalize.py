import pandas as pd

from nltk.tokenize import TweetTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
word_tokenize = TweetTokenizer().tokenize

from converters.Date import DateVietnamese
from converters.Time import Time
from converters.Money import Money
from converters.Fraction import Fraction
from converters.Telephone import TelephoneVietnamese
from converters.Cardinal import CardinalVietnamese
from converters.Decimal import Decimal
from converters.Range import Range
from converters.Meansure import Measure

labels ={
    'DATE': DateVietnamese(),
    'TIME':Time(),
    'MONEY':Money(),
    'FRACTION':Fraction(),
    'TELEPHONE':TelephoneVietnamese(),
    'CARDINAL':CardinalVietnamese(),
    'DECIMAL':Decimal(),
    'RANGE' :Range(),
    'MEANSURE': Measure()
}
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
def has_date(inputString):
    if "/" not in inputString:
        return False
    splt = inputString.split("/")
    for i in splt:
        if not i.isdigit():
            return False
    if len(splt) >3 :
        return False
    if len(splt) == 2:
        month = int(splt[0])
        year = int(splt[1])
        if month >12 or year > 2200 or month <1:
            return False
    if len(splt)==3:
        day =int(splt[0])
        month = int(splt[1])
        year =int(splt[2])
        if day >31 or month > 12 or year >2200 or day < 1 or month <1:
            return False
    return True

def is_time(text):
    if ":" not in text:
        return False
    if "-" in text:
        text = text[:-1]
    splt = text.split(":")
    if len(splt)>3 or '' in splt:
        return False
    elif len(splt)==2:
        HH,MM = int(splt[0]),int(splt[1])
        if HH >24 or MM >60:
            return False
    elif len(splt) ==3:
        HH,MM,SS = int(splt[0]),int(splt[1]),int(splt[2])
        if HH>24 or MM>60 or SS>100:
            return False

    return True
def is_money(inputString):
    return inputString.startswith(('$', '€', '£', '¥'))
def is_fraction(inputString):
    return "/" in inputString
def is_decimal(inputString):
    return "." in inputString
def is_cardinal(inputString):
    return "," in inputString or len(inputString) <= 3
def is_range(inputString) :
    return "-" in inputString
def is_telephone(inputString):
    if inputString.startswith(("19", "18", "0")) and len(inputString)>4:
        return True
def is_meansure(text):
    if text in labels['MEANSURE'].custom_dict:
        return True
def normalize_single(text,previous=""):

    if has_numbers(text):

        if has_date(text):
            text = labels["DATE"].convert_date(text)

        elif is_time(text):
            if text.endswith("-"):
                kq = labels['TIME'].convert(text[:-1])
                kq += " đến"
            else:
                kq = labels['TIME'].convert(text)
            text =kq

        elif is_money(text):
            text = labels['MONEY'].convert(text)

        elif is_decimal(text):
            text = labels['DECIMAL'].convert(text)
        elif is_telephone(text):
            text =labels['TELEPHONE'].convert(text)
        elif is_cardinal(text):
            text = labels['CARDINAL'].convert(text)
        elif is_range(text):
            text = labels['RANGE'].convert(text)

        if is_fraction(text):
            text = labels['FRACTION'].convert(text)
        if has_numbers(text):
            text = labels['CARDINAL'].convert(text)

    text = text.replace("%", " phần trăm")
    text = text.replace("&", " và")
    return text
if __name__ == "__main__":
    v ="5%"
    v =word_tokenize(v)
    print(v)
    for i in v:
        te =normalize_single(i)
        print(i, te)