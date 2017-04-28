# coding: utf-8

import os.path
import codecs

x = 1

def ngram(text, n):
	results = []
	global x
	if len(text) >= n:
		for i in range(len(text)-n+1):
			results.append(text[i:i+n])
			x+=1
	return results

f = codecs.open('data/001.txt', 'r', 'utf-8')
text = f.read()

words = {}
for word in ngram(text, 3):
	words[word] = words.get(word, 0) + 1

d = [(v, k) for k , v in words.items()]
d.sort()
d.reverse()
for count, word in d:
	print count, word 

print(x)
