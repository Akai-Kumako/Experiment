# coding: utf-8

import os
import codecs
import glob

x = 0

def ngram(text, n):

	results = []
	global x
	if len(text) >= n:
		for i in range(len(text)-n+1):
			results.append(text[i:i+n])
			x+=1
	return results

for files in glob.glob('data/*'):

	f = codecs.open(files, 'r', 'utf-8')
	text = f.read()
	
	print(files.replace('data/', ''))

	files = files.replace('data/', '')

	words = {}
	for word in ngram(text, 3):
		words[word] = words.get(word, 0) + 1

	d = [(v, k) for k , v in words.items()]
	d.sort()
	d.reverse()

	g = codecs.open('results/' + files, 'w', 'utf-8')

	for count, word in d:
		tf = float(count) / float(x)
		g.write(str(count) + word + "%.4f"%(tf) + "\n")

	g.close()
