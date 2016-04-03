from praw import Reddit

import json
import os

import time

class FetchBot:
    """Bot to fetch the subreddit data."""

    def __init__(self, user_agent, subreddit, data_file):
        """Basic constructor"""
        self._user_agent = user_agent
        self._subreddit = subreddit
        if data_file.startswith('/'):
            self._data_file = data_file
        else:
            self._data_file = os.path.join(os.getenv('HOME'), data_file)
        try:
            with open(self._data_file) as df:
                self._data = json.load(df)
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            self._data = json.loads('{"comments":{},"posts":{}}')

        try:
            if self._data['subreddit'] != self._subreddit:
                raise ValueError('The data file does not correspond the subreddit r/'+self._subreddit)
        except KeyError:
            self._data['subreddit'] = self._subreddit

        self._praw = Reddit(self._user_agent)

    def __del__(self):
        """Destructor"""
        if not os.path.exists(os.path.dirname(self._data_file)):
            os.makedirs(os.path.dirname(self._data_file))
        with open(self._data_file, 'w') as df:
            json.dump(self._data, df)

    def fetch(self):
        """Fetching function"""
        self._fetch(self._praw.get_comments(self._subreddit, limit=500), 'comments')
        self._fetch(self._praw.get_subreddit('france').get_new(limit=500), 'posts')

    def _fetch(self, submissions, key):
        """Generic fetching function"""

        is_first = True

        try:
            self._data[key]['first']
        except:
            self._data[key]['first'] = float(round(time.time()))

        try:
            new_creation_limit = self._data[key]['last']
        except:
            self._data[key]['last'] = new_creation_limit = 0

        for it in submissions:
            if is_first:
                is_first = False
                new_creation_limit = it.created
            if it.created <= self._data[key]['last']:
                break

            try:
                self._data[key]['count'] += 1
            except KeyError:
                self._data[key]['count'] = 1

            if it.author_flair_text:
                try:
                    if str(it.author) not in self._data[key]['unique-users']:
                        self._data[key]['unique-users'][str(it.author)] = it.author_flair_text
                except KeyError:
                    self._data[key]['unique-users'] = dict()
                    if str(it.author) not in self._data[key]['unique-users']:
                        self._data[key]['unique-users'][str(it.author)] = it.author_flair_text

                if 'flair-presence' not in self._data[key]:
                    self._data[key]['flair-presence'] = dict()

                try:
                    self._data[key]['flair-presence'][str(it.author_flair_text)] += 1
                except KeyError:
                    self._data[key]['flair-presence'][str(it.author_flair_text)] = 1

            if key == 'posts':
                if 'subject-presence' not in self._data[key]:
                    self._data[key]['subject-presence'] = dict()

                try:
                    self._data[key]['subject-presence'][str(it.link_flair_text)] += 1
                except KeyError:
                    self._data[key]['subject-presence'][str(it.link_flair_text)] = 1
        
        self._data[key]['last'] = new_creation_limit


def FetchBotGenerator(config_file):
    """Generate a list-like container of FetchBot objects"""
    with open(config_file) as cf:
        json_config = json.load(cf)

    user_agent = json_config['user-agent']
    for i in json_config['bots']:
        yield FetchBot(user_agent, i['subreddit'], i['data-file'])

def autorun():
    """Autorun function of this module"""
    home = os.getenv('HOME')
    config_file = os.path.join(home, '.config/flairstats/config.json')
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)

    fetchbots = FetchBotGenerator(config_file)

    for bot in fetchbots:
        bot.fetch()

if __name__ == "__main__":
    autorun()
