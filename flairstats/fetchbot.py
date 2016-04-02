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
        self._data_file = data_file
        try:
            with open(self._data_file) as df:
                self._data = json.load(df)
        except (FileNotFoundError,json.decoder.JSONDecodeError):
            self._data = json.loads('{"comments":{},"posts":{}}')

        self._praw = Reddit(self._user_agent)

    def __del__(self):
        with open(self._data_file, 'w') as df:
            json.dump(self._data, df)

    def fetch(self):
        """Fetching function"""
        submissions = self._praw.get_comments(self._subreddit, limit=500)

        is_first = True

        try:
            self._data['comments']['first']
        except:
            self._data['comments']['first'] = float(round(time.time()))

        try:
            new_comment_creation_limit = self._data['comments']['last']
        except:
            self._data['comments']['last'] = new_comment_creation_limit = 0

        for comment in submissions:
            if is_first:
                is_first = False
                new_comment_creation_limit = comment.created
            if comment.created <= self._data['comments']['last']:
                break

            try:
                self._data['comments']['count'] += 1
            except KeyError:
                self._data['comments']['count'] = 1

            if comment.author_flair_text:
                try:
                    if str(comment.author) not in self._data['comments']['unique-users']:
                        self._data['comments']['unique-users'][str(comment.author)] = comment.author_flair_text
                except KeyError:
                    self._data['comments']['unique-users'] = dict()
                    if str(comment.author) not in self._data['comments']['unique-users']:
                        self._data['comments']['unique-users'][str(comment.author)] = comment.author_flair_text

                if 'flair-presence' not in self._data['comments']:
                    self._data['comments']['flair-presence'] = dict()

                try:
                    self._data['comments']['flair-presence'][str(comment.author_flair_text)] += 1
                except KeyError:
                    self._data['comments']['flair-presence'][str(comment.author_flair_text)] = 1
        
        self._data['comments']['last'] = new_comment_creation_limit


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
