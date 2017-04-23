#!/user/bin/env python
# coding: utf-8

import os.path
import codecs

def ngram(text, n):
	results = []
	x = 0
	if len(text) >= n:
		for i in range(len(text)-n+1):
			results.append(text[i:i+n])
			x+=1
	print(x)
	return results

f = codecs.open('data/001.txt', 'r', 'utf-8')
text = f.read()

for e in ngram(text, 3):
	print(e)
