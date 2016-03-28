#! /usr/bin/env python3

import json
import sys
from praw import Reddit

my_user_agent = 'subreddit flair statistics - by u/dopsi'

r = Reddit(user_agent=my_user_agent)

flair='none'

with open(sys.argv[2]+'/flairs.json') as f:
    j = json.load(f)

sub_comments = r.get_comments(sys.argv[1])

first = True
new_lastcomment = j['lastcomment']

for i in sub_comments:
    if (i.created <= j['lastcomment']):
        print("Ignored comment (reason: too old)")
        continue

    if (first):
        first = False
        new_lastcomment = i.created
    
    if (i.author_flair_text == None):
        try:
            j['data']['none'] += 1
            print("Increased 'none' comments by 1 for user "+str(i.author))
        except KeyError:
            j['data']['none'] = 1
            print("Added 'none' key for user "+str(i.author))
    else:
        try:
            j['data'][i.author_flair_text] += 1
            print("Increased '"+i.author_flair_text+"' comments by 1 for user "+str(i.author))
        except KeyError:
            j['data'][i.author_flair_text] = 1
            print("Added '"+i.author_flair_text+"' key for user "+str(i.author))

j['lastcomment'] = new_lastcomment

with open(sys.argv[2]+'flairs.json', mode='w') as f:
    json.dump(j, f)
