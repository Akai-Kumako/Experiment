import sys
import MeCab
import codecs

m = MeCab.Tagger ("-Ochasen”")
f = codecs.open("../data/001.txt", 'r', 'utf-8')
text = f.read()

w = m.parse (text)
words = []

words = w.split("\n")

for e in words:
	print(e)
