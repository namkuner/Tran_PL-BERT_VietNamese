import string
from nltk.tokenize import TweetTokenizer
word_tokenize = TweetTokenizer().tokenize
special_mappings = {
    "a": "ɐ",
    "'t": 't',
    "'ve": "v",
    "'m": "m",
    "'re": "ɹ",
    "d": "d",
    'll': "l",
    "n't": "nt",
    "'ll": "l",
    "'d": "d",
    "'": "ʔ",
    "wasn": "wˈɒzən",
    "hasn": "hˈæzn",
    "doesn": "dˈʌzən",
}

def clean_word(word):
    special_chars = "{<[)}>(]"
    for char in special_chars:
        input_string = word.replace(char, '"')
    return word
def check_phonemes(phonem):
    special_chars_to_ignore = "̪̃/^"
    for char in special_chars_to_ignore:
        if char in phonem:
            return False
    return True
def replace_special_chars(word):
    x = "t̪"
    return word.replace(x, 't0')
def phonemize(text, global_phonemizer, tokenizer):

    words = word_tokenize(text)
    words = [clean_word(word) for word in words]
    phonemes_bad = [global_phonemizer.phonemize([word], strip=True)[0] if word not in string.punctuation else word for
                    word in words]
    phonemes_bad = [replace_special_chars(phoneme) for phoneme in phonemes_bad]

    input_ids = []
    phonemes = []

    for i in range(len(words)):
        word = words[i]
        phoneme = phonemes_bad[i]
        if not check_phonemes(phoneme):
            continue

        # process special cases (NOT COMPLETE)
        try :
            token = tokenizer[word]
        except:
            continue
        input_ids.append(token)
        phonemes.append(phoneme)

    assert len(input_ids) == len(phonemes)
    return {'input_ids': input_ids, 'phonemes': phonemes}