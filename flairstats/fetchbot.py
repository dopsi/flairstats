from praw import Reddit

import json
import os

class FetchBot:
    """Bot to fetch the subreddit data."""

    def __init__(self, user_agent, subreddit, data_file):
        """Basic constructor"""
        self._user_agent = user_agent
        self._subreddit = subreddit
        self._data_file = data_file

    def fetch(self):
        """Fetching function"""
        print('FetchBot called for r/'+self._subreddit)

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
