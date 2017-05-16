# coding: utf-8

import os
import codecs
import glob
import math
import sys
import MeCab
import re


#単語に分割する関数
def tango(text):

	m = MeCab.Tagger("mecabrc")
	analysis = m.parse(text)
	q = []
	q = analysis.split("\n")
	txt = []
	for info in q:
		if not(info == 'EOS' or info == ''):
			info_elems = info.split(',')
		if(info_elems[0].find("\t助詞") == -1 and info_elems[0].find("\t助動詞") == -1 and info_elems[0].find("\t接続詞") == -1 and info_elems[0].find("\t記号") == -1):
			if(info_elems[6] == '*'):
				txt.append(info_elems[0].replace('	名詞', ''))
			else:
				txt.append(info_elems[6])
		else:
			txt.append('')
	return txt

#Ngramを求める関数
def ngram(text, n):

	results = []
	global x
	x = 0
	if len(text) >= n:
		for i in range (len(text)-n+1):
			results.append("".join(text[i:i+n]))
			x+=1
	return results

args = sys.argv
y = 0
Ngram = {}
k = 1
IDF = {}
IDFfiles = {}

#IDFの値を求める

for files in glob.glob('data/*'):

	y+=1	

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	text = re.sub(re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+"), ' ', text)
	text = re.sub(re.compile("[!-/:-@[-`{-~]"), ' ', text)
	text = tango(text)
	
	words = {}
	for word in ngram(text, k):
		words[word] = words.get(word, 0) + 1

	files = files.replace("data/", "")

	for word in words.keys():
		Ngram[word] = words.get(word, 0) + 1
		IDFfiles[word] = IDFfiles.get(word, "") + "\t" + files

e = [(v, k) for k, v in Ngram.items()]
e.sort()
e.reverse()		

for count, word in e:
	idf = math.log2(float(y) / float(count))
	IDF[word] = idf

#転置インデックスを作成してファイルに出力する

h = codecs.open('tango-index/tangolist.txt', 'w', 'utf-8')
b = [(v, k) for k, v in IDFfiles.items()]
for files, word in b:
	h.write(word + files + "\n")
h.close()

#TFの値を求める
#TF-IDEの値をファイルに出力する

for files in glob.glob('data/*'):

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	text = re.sub(re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+"), ' ', text)
	text = re.sub(re.compile("[!-/:-@[-`{-~]"), ' ', text)
	text = tango(text)

	files = files.replace('data/', '')

	words = {}
	for word in ngram(text, k):
		words[word] = words.get(word, 0) + 1

	d = [(v, k) for k, v in words.items()]
	d.sort()
	d.reverse()

	g = codecs.open('tango-index/' + files, 'w', 'utf-8')

	results = {}
	for count, word in d:
		tf = float(count) / float(x)
		tfidf = "%.4f"%(tf * IDF[word])
		results[word] = tfidf
	c = [(v, k) for k, v in sorted(results.items())]
	#c.sort()
	#c.reverse()

	for count, word in c:
		g.write(word + "\t" + count + "\n")

	g.close()

argvs = sys.argv
#検索結果を表示する
res = {}
out = []
for argument in range(1, len(argvs)):
	texts = []
	texts = IDFfiles.get(args[argument], "").split("\t")
	res[args[argument]] = texts		
	if(argument == 1):
		out = set(res.get(args[argument], ""))
	else:
		out = out.update(set(res.get(args[argument], "")))
print(out, "検索結果はありません")
