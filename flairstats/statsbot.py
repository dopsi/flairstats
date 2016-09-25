import json
import os

import htmlgenerator.generator

from collections import OrderedDict
from itertools import islice
import datetime
import time
import pygal
from pygal.style import Style

from .tools import display

def time_flatten(data, factor=1):
    ret = [0 for _ in range(24)]

    for key, value in data.items():
        ret[int(int(key)/100)] += value/factor

    return ret

class StatsBot:
    def __init__(self, subreddit, data_file, output_dir):
        """Basic constructor"""
        self._subreddit = subreddit
        self._data_file = data_file
        self._output_dir = output_dir
        
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)
        os.chdir(output_dir)
        
        with open(self._data_file) as df:
            self._data = json.load(df)

        self._page = htmlgenerator.generator.HtmlGenerator()
        self._page.title = 'Statistiques de r/'+self._subreddit

    def __del__(self):
        self._page.write('index.html')
    
    def generate(self):
        start_time = time.time()
        self._page.header().h1('Statistiques de r/'+self._subreddit, align='center')

        section = self._page.section()

        line_chart = pygal.Radar()
        line_chart.title = 'Activité en fonction de l\'heure'
        line_chart.x_labels = map(str, range(0, 24))
        line_chart.add('Posts', time_flatten(self._data['posts']['time']['all'], self._data['posts']['count']))
        line_chart.add('Commentaires', time_flatten(self._data['comments']['time']['all'], self._data['comments']['count']))
        with open('activity.svg', 'wb') as act:
            act.write(line_chart.render())

        section.embed(src='activity.svg', id='activity', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')

        # User flairs

        ## Comments

        try:
            posts_flairs_ranking = OrderedDict(sorted(self._data['posts']['flair-presence'].items(),key=lambda t: t[1]),reverse=True)
        except KeyError:
            pass
        else:
            section = self._page.section()
            pie_chart = pygal.HorizontalBar()
            pie_chart.title = 'Distribution des flairs des posteurs'

            posts_flairs_ref_value = max(posts_flairs_ranking.values())/5
            posts_remainder = 0

            data_for_graph = OrderedDict()
            for k, v in posts_flairs_ranking.items():
                if float(v) >= posts_flairs_ref_value:
                    try:
                        data_for_graph[k] =  v
                    except:
                        raise
            
            pie_chart.x_labels = data_for_graph.keys()
            pie_chart.add('Poster flairs', data_for_graph.values())

            with open('posts_flairs.svg', 'wb') as posts_flairs:
                posts_flairs.write(pie_chart.render())
            
            section.embed(src='posts_flairs.svg', id='posts_subjects', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')

        # Post flairs

        try:
            posts_subjects_ranking = OrderedDict(sorted(self._data['posts']['subject-presence'].items(), key=lambda t: t[1]))
        except KeyError:
            pass
        else:
            section = self._page.section()
            try:
                del posts_subjects_ranking['None']
            except KeyError:
                pass
            bar_chart = pygal.HorizontalBar()
            bar_chart.title = 'Distribution des catégories de posts'

            bar_chart.x_labels = posts_subjects_ranking.keys()
            bar_chart.add('Posts', posts_subjects_ranking.values())
            with open('posts_subjects.svg', 'wb') as posts_subjects:
                posts_subjects.write(bar_chart.render())
            
            section.embed(src='posts_subjects.svg', id='posts_subjects', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')

        duration = time.time() - start_time
        duration_string = ' (en '+display.float(duration, 3)+' secondes). '
        duration_string += str(self._data['comments']['count'])+' commentaires analysés, '
        duration_string += str(self._data['posts']['count'])+' posts analysés.'
        foot = self._page.footer().p("Généré le "+datetime.datetime.now().strftime('%Y-%m-%d à %H:%M %Z')+duration_string.format(duration))
        foot.append(' Code source disponible sur ')
        foot.append(htmlgenerator.markup.HtmlAnchor('GitHub', 'http://github.com/dopsi/flairstats'))
        foot.append('.')
        
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
