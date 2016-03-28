#! /usr/bin/env python3

import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import operator
from collections import OrderedDict
import datetime

with open(sys.argv[1]+"/flairs.json") as f:
    j = json.load(f)

D = OrderedDict(sorted(j['data'].items(), key=lambda t: t[1]))

rng = range(len(D))
plt.figure(figsize=(40,20), dpi=100)
plt.barh(rng, D.values(), align='center')
plt.yticks(rng, D.keys())
plt.title("Flairs de r/france par nombre de commentaires")

plt.savefig(sys.argv[1]+"/plot.svg")

html_begin = """<!doctype html>

<html lang="en">
	<head>
	<meta charset="utf-8">

	<title>The HTML5 Herald</title>
	<meta name="description" content="Visualisation of r/france comment author's flairs">
	<meta name="author" content="dopsi">

	</head>

	<body>
		<img style="width: 100%;" src="plot.svg" alt="Representation"/>
		<p>Last updated : """
html_end="""</p>
	</body>
</html>"""
comments_sum=sum([ x[1] for x in D.items()])
html = html_begin+str(datetime.datetime.now())+', '+str(comments_sum)+' comments analysed'+html_end

with open(sys.argv[1]+"/index.html", "w") as f:
    f.write(html)
