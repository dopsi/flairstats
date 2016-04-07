import json
import os

import htmlgenerator.generator

from collections import OrderedDict
import datetime
import time

from .tools import display

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
        self._page.header().h1('Subreddit statistics for r/'+self._subreddit)

        section = self._page.section()
        posts_subjects_ranking = OrderedDict(sorted(self._data['posts']['subject-presence'].items(), key=lambda t: t[1], reverse=True))
        del posts_subjects_ranking['None']
        tbl_posts_subjects_ranking = section.article().table()
        tbl_posts_subjects_ranking.tr().td('Flairs de posts les plus utilisés', colspan=2)
        for key, value in posts_subjects_ranking.items():
            tbl_posts_subjects_ranking.tr(value, key)

        posts_flairs_ranking = OrderedDict(sorted(self._data['posts']['flair-presence'].items(), key=lambda t: t[1], reverse=True))
        tbl_posts_flairs_ranking = section.article().table()
        tbl_posts_flairs_ranking.tr().td('Flairs des posts les plus utilisés', colspan=2)
        for key, value in list(posts_flairs_ranking.items())[:10]:
            tbl_posts_flairs_ranking.tr(value, key)

        comments_flairs_ranking = OrderedDict(sorted(self._data['comments']['flair-presence'].items(), key=lambda t: t[1], reverse=True))
        tbl_comments_flairs_ranking = section.article().table()
        tbl_comments_flairs_ranking.tr().td('Flairs des commentaires les plus utilisés', colspan=2)
        for key, value in list(comments_flairs_ranking.items())[:10]:
            tbl_comments_flairs_ranking.tr(value, key)

        duration = time.time() - start_time
        duration_string = ' (took '+display.float(duration, 3)+' seconds). '
        duration_string += str(self._data['comments']['count'])+' comments analysed, '
        duration_string += str(self._data['posts']['count'])+' posts analysed.'
        self._page.footer().p("Generated at "+datetime.datetime.now().strftime('%Y-%m-%d %H:%M %Z')+duration_string.format(duration))

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
