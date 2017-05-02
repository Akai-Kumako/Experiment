# coding: utf-8

import os
import codecs
import glob
import math
import sys

args = sys.argv

def ngram(text, n):

	results = []
	global x
	x = 0
	if len(text) >= n:
		for i in range(len(text)-n+1):
			results.append(text[i:i+n])
			x+=1
	return results

gram = [{}, {}, {}, {}, {}]

y = 0

for files in glob.glob('data/*'):

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()

	y+=1

	#print(files.replace('data/', ''))

	files = files.replace('data/', '')

<<<<<<< HEAD
	for i in range(1, 6, 1):

		words = {}
		for word in ngram(text, i):
			words[word] = words.get(word, 0) + 1

		if(i == 1):
			for word in words.keys():
				gram[0][word] = gram[0].get(word, 0) + 1
		elif(i == 2):
			for word in words.keys():
				gram[1][word] = gram[1].get(word, 0) + 1
		elif(i == 3):
			for word in words.keys():
				gram[2][word] = gram[2].get(word, 0) + 1
		elif(i == 4):
			for word in words.keys():
				gram[3][word] = gram[3].get(word, 0) + 1
		elif(i == 5):
			for word in words.keys():
				gram[4][word] = gram[4].get(word, 0) + 1

		d = [(v, k) for k , v in words.items()]
		d.sort()
		d.reverse()

		g = codecs.open('results/' + str(i) + '_' + files, 'w', 'utf-8')

		for count, word in d:
			tf = float(count) / float(x)
			g.write(str(count) + word + "%.4f"%(tf) + "\n")

		g.close()

#unigramを求める
h = codecs.open('results/unigram.txt', 'w', 'utf-8')

e = [(r, t) for t, r in gram[0].items()]
e.sort()
e.reverse()

for cnt, w in e:
	idf = math.log2(float(y) / float(cnt))
	h.write(w + " " + "%.4f"%(idf) + "\n")

h.close()

#baigramを求める
h = codecs.open('results/baigram.txt', 'w', 'utf-8')

e = [(r, t) for t, r in gram[1].items()]
e.sort()
e.reverse()

for cnt, w in e:
	idf = math.log2(float(y) / float(cnt))
	h.write(w + " " + "%.4f"%(idf) + "\n")

h.close()

#trigramを求める
h = codecs.open('results/trigram.txt', 'w', 'utf-8')

e = [(r, t) for t, r in gram[2].items()]
e.sort()
e.reverse()

for cnt, w in e:
	idf = math.log2(float(y) / float(cnt))
	h.write(w + " " + "%.4f"%(idf) + "\n")

h.close()

#fourgramを求める
h = codecs.open('results/fourgram.txt', 'w', 'utf-8')

e = [(r, t) for t, r in gram[3].items()]
e.sort()
e.reverse()

for cnt, w in e:
	idf = math.log2(float(y) / float(cnt))
	h.write(w + " " + "%.4f"%(idf) + "\n")

h.close()

#fivegramを求める
h = codecs.open('results/fivegram.txt', 'w', 'utf-8')

e = [(r, t) for t, r in gram[4].items()]
e.sort()
e.reverse()

for cnt, w in e:
	idf = math.log2(float(y) / float(cnt))
	h.write(w + " " + "%.4f"%(idf) + "\n")

h.close()   	
