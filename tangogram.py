# coding: utf-8

import os
import codecs
import glob
import math
import sys
import MeCab

#単語ngramの関数
def tango(text):

	m = MeCab.Tagger("mecabrc")
	analysis = m.parse(text)
	q = []
	q = analysis.split("\n")
	txt = []
	for info in q:
		if not(info == 'EOS' or info == ''):
			info_elems = info.split(',')
		if(info_elems[6] == '*'):
			txt.append(info_elems[0].replace('	名詞', ''))
		else:
			txt.append(info_elems[6])
	return txt

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
k = int(args[1])
IDF = {}

#IDFの値を求める

for files in glob.glob('data/*'):

	y+=1	

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	text = tango(text)
	
	words = {}
	for word in ngram(text, k):
		words[word] = words.get(word, 0) + 1

	for word in words.keys():
		Ngram[word] = words.get(word, 0) + 1

e = [(v, k) for k , v in Ngram.items()]
e.sort()
e.reverse()		

for count, word in e:
	idf = math.log2(float(y) / float(count))
	IDF[word] = idf

#TFの値を求める
#TF-IDEの値をファイルに出力する

for files in glob.glob('data/*'):

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	text = tango(text)

	files = files.replace('data/', '')

	words = {}
	for word in ngram(text, k):
		words[word] = words.get(word, 0) + 1

	d = [(v, k) for k, v in words.items()]
	d.sort()
	d.reverse()

	g = codecs.open('tango-results/' + str(k) + "_" + files, 'w', 'utf-8')

	for count, word in d:
		tf = float(count) / float(x)
		g.write(word + " " + "%.4f"%(tf * IDF[word]) + "\n")

	print(files)	

	g.close()
