import json
import os

import htmlgenerator.generator

from collections import OrderedDict
import datetime
import time
import pygal
from pygal.style import Style

from .tools import display

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

# Subject flairs
        try:
            section = self._page.section()
            posts_subjects_ranking = OrderedDict(sorted(self._data['posts']['subject-presence'].items(), key=lambda t: t[1]))
            del posts_subjects_ranking['None']
            posts_subjects_line_chart = pygal.HorizontalBar()
            posts_subjects_line_chart.title = 'Distribution des catégories de posts'
            posts_subjects_line_chart.x_labels = posts_subjects_ranking.keys()
            posts_subjects_line_chart.add('Posts', posts_subjects_ranking.values())
            with open('posts_subjects_ranking.svg', 'wb') as svgfile:
                svgfile.write(posts_subjects_line_chart.render())
    
            section.embed(src='posts_subjects_ranking.svg', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')
        except KeyError:
            section.p('No subject flairs available')

# User comments flairs
        try:
            section = self._page.section()
            posts_flairs_ranking = OrderedDict(sorted(self._data['posts']['flair-presence'].items(), key=lambda t: t[1]))
            comments_flairs_ranking = OrderedDict(sorted(self._data['comments']['flair-presence'].items(), key=lambda t: t[1]))
            
            user_comment_flairs_line_chart = pygal.HorizontalBar(height=12*len(comments_flairs_ranking))
            user_comment_flairs_line_chart.title = 'Distribution des flairs utilisateurs (en % du total des commentaires)'
            user_comment_flairs_line_chart.x_labels = comments_flairs_ranking.keys()
            user_comment_flairs_line_chart.add('Commentaires', comments_flairs_ranking.values())
            with open('user_comments_flairs_ranking.svg', 'wb') as svgfile:
                svgfile.write(user_comment_flairs_line_chart.render())
    
            user_comment_flairs_line_chart = pygal.HorizontalBar(height=12*len(posts_flairs_ranking))
            user_comment_flairs_line_chart.title = 'Distribution des flairs utilisateurs (en % du total des posts)'
            user_comment_flairs_line_chart.x_labels = posts_flairs_ranking.keys()
            user_comment_flairs_line_chart.add('Commentaires', posts_flairs_ranking.values())
            with open('user_posts_flairs_ranking.svg', 'wb') as svgfile:
                svgfile.write(user_comment_flairs_line_chart.render())
    
            section.embed(src='user_comments_flairs_ranking.svg', tipe='image/svg+xml')
            section.embed(src='user_posts_flairs_ranking.svg', tipe='image/svg+xml')
        except KeyError:
            section.p('No user comment flair')

# Footer
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
