import html
import os
from phonemize import phonemize

import phonemizer
global_phonemizer = phonemizer.backend.EspeakBackend(language='vi', preserve_punctuation=True,  with_stress=True)
import json

with open("vocal.json", 'r', encoding='utf-8') as file:
  tokenizer = json.load(file)
all = []

for idx, txt_book in enumerate(os.listdir("data")):
  file_path = f"data/{txt_book}"
  with open(file_path, 'r',encoding="utf8") as file:
    lines = file.readlines()
  for line in lines:
    html_line = html.unescape(line.replace('\n', '').replace('\t', ''))
    if "http:" in html_line or len(html_line)<200:
      continue
    all.append(html_line)
  if idx%10==0:
    print(idx)

for i in all:
  x = phonemize(i,global_phonemizer,tokenizer)
  print(x)