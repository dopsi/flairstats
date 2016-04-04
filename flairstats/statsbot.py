import json
import os

import htmlgenerator.generator

from collections import OrderedDict
import datetime
import time
import math

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
        start_time = time.time()
        self._page.h1('Subreddit statistics for r/'+self._subreddit)
        posts_subjects_ranking = OrderedDict(sorted(self._data['posts']['subject-presence'].items(), key=lambda t: t[1], reverse=True))
        del posts_subjects_ranking['None']
        tbl_posts_subjects_ranking = self._page.table()
        tbl_posts_subjects_ranking.tr('Flairs de posts les plus utilisés')
        for i in posts_subjects_ranking.keys():
            tbl_posts_subjects_ranking.tr(i)
        duration = time.time() - start_time
        duration_string = ' (took {0:.'+'{:.0f}'.format(max(math.fabs(math.floor(math.log10(duration))),3))+'f} seconds).'
        self._page.p("Generated at "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M %Z')+duration_string.format(duration))

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
