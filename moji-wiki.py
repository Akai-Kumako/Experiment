# coding: utf-8

import os
import codecs
import glob
import math
import sys
import MeCab
import re
import numpy as np

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
k = int(args[1])
IDF = {}
IDFfiles = {}

#IDFの値を求める

for files in glob.glob('Wikipedia/*'):

	y+=1	

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	text = re.sub(re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+"), ' ', text)
	text = re.sub(re.compile("[!-/:-@[-`{-~]"), ' ', text)
	#text = tango(text)
	
	words = {}
	for word in ngram(text, k):
		words[word] = words.get(word, 0) + 1

	files = files.replace("Wikipedia/", "")

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

h = codecs.open('moji-wiki/tangolist.txt', 'w', 'utf-8')
b = [(v, k) for k, v in IDFfiles.items()]
for files, word in b:
	h.write(word + files + "\n")
h.close()

#TFの値を求める
#TF-IDFの値をファイルに出力する

brains = {} #全ファイルの全単語に対するTF-IDF値が格納された辞書 
for files in glob.glob('Wikipedia/*'):

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	text = re.sub(re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+"), ' ', text)
	text = re.sub(re.compile("[!-/:-@[-`{-~]"), ' ', text)
	#text = tango(text)

	files = files.replace('Wikipedia/', '')

	words = {}
	for word in ngram(text, k):
		words[word] = words.get(word, 0) + 1

	if(args[1] == 2): words.pop("  ")

	d = [(v, k) for k, v in words.items()]
	d.sort()
	d.reverse()

	g = codecs.open('moji-wiki/' + files, 'w', 'utf-8')

	results = {}
	for count, word in d:
		tf = float(count) / float(x)
		tfidf = "%.4f"%(tf * IDF[word])
		results[word] = tfidf
	c = [(v, k) for k, v in sorted(results.items())]

	brains[files] = results

	for count, word in c:
		g.write("'" + word + "'" + "\t" + count + "\n")

	g.close()

argvs = sys.argv

#検索結果を表示する
res = {}
out = []
if(len(argvs) == 2):
	print("検索条件を引数に入力してください")
	sys.exit()
for argument in range(2, len(argvs)):
	texts = []
	texts = IDFfiles.get(args[argument], "").split("\t")
	res[args[argument]] = texts		
	if(argument == 2):
		out = res.get(args[argument], "")
	else:
		out = list(set(out) & set(res.get(args[argument], "")))
out.remove("")

#検索結果をランキング形式で表示する

if(len(out) == 0):
	print("該当するファイルはありません。")
else:
	standard = "0";
	standardfile = "";
	for here in range(len(out)):
		if standard < brains[out[here]][args[2]]:
			standard = brains[out[here]][args[2]]
			standardfile = out[here]
	
	##絶対値を計算
	standardvalues = brains[standardfile].values()
	standardvalues = [float(n) for n in standardvalues] #文字列リストを浮動小数点型リストに変換
	standardvalues = [x ** 2 for x in standardvalues] #リストの各要素を二乗する

	subfiles = list(out)
	subfiles.remove(standardfile)

	absolute = {}
	for f in subfiles:
		values = brains[f].values()
		values = [float(n) for n in values]
		values = [x ** 2 for x in values]
		absolute[f] = sum(values)

	##内積を計算
	inner = {}
	for f in subfiles:
		keys = list(set(brains[f].keys()) & set(brains[standardfile].keys()))
		inn = 0
		for k in keys:
			inn += float(brains[f].get(k, 0)) * float(brains[standardfile].get(k, 0))
		inner[f] = inn

	##類似度を計算
	similarity = {}
	for f in subfiles:
		degree = inner.get(f, 0) / (math.sqrt(absolute.get(f, 0)) * math.sqrt((sum(standardvalues))))
		similarity[f] = degree

	print("検索結果:" + str(len(out)) + "件")
	print(standardfile)
	for k, v in sorted(similarity.items(), key = lambda x:x[1], reverse=True):
		print(k + " :	" + str(v))
