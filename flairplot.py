#! /usr/bin/env python3

import json
import sys

import matplotlib.pyplot as plt
import operator
from collections import OrderedDict

with open(sys.argv[1]) as f:
    j = json.load(f)

D = OrderedDict(sorted(j['data'].items(), key=lambda t: t[1]))

rng = range(len(D))
plt.figure(figsize=(40,20), dpi=100)
plt.barh(rng, D.values(), align='center')
plt.yticks(rng, D.keys())
plt.title("Flairs de r/france par nombre de commentaires")

plt.savefig(sys.argv[2])
