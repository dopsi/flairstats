import json
import os

import htmlgenerator.generator

class StatsBot:
    def __init__(self, subreddit, data_file, output_dir):
        """Basic constructor"""
        self._subreddit = subreddit
        self._data_file = data_file
        self._output_dir = output_dir
        with open(self._data_file) as df:
            self._data = json.load(df)

        self._page = htmlgenerator.generator.HtmlGenerator()

    def __del__(self):
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
        self._page.write(os.path.join(self._output_dir, 'index.html'))
    
    def generate(self):
        self._page.h1('Subreddit statistics for r/'+self._subreddit)

def StatsBotGenerator(config_file):
    """Generate a list-like container of StatsBot objects"""
    with open(config_file) as cf:
        json_config = json.load(cf)

    for i in json_config['bots']:
        yield StatsBot(i['subreddit'], i['data-file'], i['output-dir'])

def autorun():
    """Autorun function of this module"""
    home = os.getenv('HOME')
    config_file = os.path.join(home, '.config/flairstats/config.json')
    if not os.path.exists(config_file):
        raise FileNotFoundError(config_file)

    statsbots = StatsBotGenerator(config_file)

    for bot in statsbots:
        bot.generate()

if __name__ == '__main__':
    autorun()
