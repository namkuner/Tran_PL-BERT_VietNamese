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


def phonemize(text, global_phonemizer, tokenizer):

    words = word_tokenize(text)

    phonemes_bad = [global_phonemizer.phonemize([word], strip=True)[0] if word not in string.punctuation else word for
                    word in words]
    input_ids = []
    phonemes = []

    for i in range(len(words)):
        word = words[i]
        phoneme = phonemes_bad[i]


        # process special cases (NOT COMPLETE)
        try :
            token = tokenizer[word]
        except:
            continue
        input_ids.append(token)
        phonemes.append(phoneme)

    assert len(input_ids) == len(phonemes)
    return {'input_ids': input_ids, 'phonemes': phonemes}