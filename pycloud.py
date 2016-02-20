#coding: utf-8

import pandas as pd
import MeCab
import re
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from os import path
from PIL import Image

stop_words = [ u'てる', u'いる', u'なる', u'れる', u'する', u'ある', u'こと', u'これ', u'さん', u'して', \
             u'くれる', u'やる', u'くださる', u'そう', u'せる', u'した',  u'思う',  \
             u'それ', u'ここ', u'ちゃん', u'くん', u'', u'て',u'に',u'を',u'は',u'の', u'が', u'と', u'た', u'し', u'で', \
             u'ない', u'も', u'な', u'い', u'か', u'ので', u'よう', u'']

pattern = re.compile('[!-~]')

fpath = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"

def text_parse(text):
	words = []
	mt = MeCab.Tagger('-Ochasen')
	res = mt.parseToNode(text)

	while res:
		if res.feature.split(",")[0] in ["形容詞", "動詞","名詞", "副詞"]:
			if res.surface != "" and (not pattern.match(res.surface)):
				words.append(res.surface)
		res = res.next
	return words

d = path.dirname(__file__)
tweets = pd.read_csv('tweets.csv')
texts = " ".join(tweets.text.values)
#print texts
word = text_parse(texts)
#print word


okayama = np.array(Image.open(path.join(d, "alice_mask.png")))
wc = WordCloud(background_color="white", font_path=fpath, mask=okayama, 
							stopwords=set(stop_words))
wc.generate(" ".join(word).decode('utf-8'))


wc.to_file(path.join(d, "pycloud.png"))

plt.imshow(wc)
plt.axis("off")
plt.figure()

