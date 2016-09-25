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
        
        with open(self._data_file) as df:
            self._data = json.load(df)

        self._page = htmlgenerator.generator.HtmlGenerator()
        self._page.title = 'Statistiques de r/'+self._subreddit

    def __del__(self):
        self._page.write(os.path.join(self._output_dir,'index.html'))
    
    def generate(self):
        start_time = time.time()
        self._page.header().h1('Statistiques de r/'+self._subreddit, align='center')

        section = self._page.section()

        # Daily activity

        day_activity = pygal.Radar()
        day_activity.title = 'Activité en fonction de l\'heure'
        day_activity.x_labels = map(str, range(0, 24))
        day_activity.add('Posts', time_flatten(self._data['posts']['time']['all'], self._data['posts']['count']))
        day_activity.add('Commentaires', time_flatten(self._data['comments']['time']['all'], self._data['comments']['count']))
        with open(os.path.join(self._output_dir,'activity.svg'), 'wb') as act:
            act.write(day_activity.render())

        section.embed(src='activity.svg', id='activity', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')

        # Weekly activity

        week_activity = pygal.Radar()
        week_activity.title = 'Activité en fonction du jour'

        weekdays = OrderedDict([(0, "Monday"), (1, "Tuesday"), (2, "Wednesday"), (3, "Thursday"), (4, "Friday"), (5, "Saturday"),(6, "Sunday")])

        week_activity.x_labels = weekdays.values()

        posts_week_activity = OrderedDict()
        comments_week_activity = OrderedDict()
        for n,day in weekdays.items():
            posts_week_activity[day] = sum(self._data['posts']['time'][str(n)].values())
            comments_week_activity[day] = sum(self._data['comments']['time'][str(n)].values())

        week_activity.add('Posts', posts_week_activity.values())
        week_activity.add('Comments', comments_week_activity.values())
        with open(os.path.join(self._output_dir,'week_activity.svg'), 'wb') as week_act:
            week_act.write(week_activity.render())

        section.embed(src='week_activity.svg', id='activity', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')

        # User flairs

        ## Comments

        try:
            user_flairs_ranking = OrderedDict(sorted(self._data['comments']['flair-presence'].items(),key=lambda t: t[1],reverse=True))
        except KeyError:
            pass
        else:
            section = self._page.section()
            user_flairs_graph =  pygal.HorizontalBar()
            user_flairs_graph.title = 'Distribution des flairs des utilisateurs'

            user_flairs_ref_value = max(user_flairs_ranking.values())/5

            data_for_graph_user_flairs = OrderedDict()
            with open(os.path.join(self._output_dir, 'user_flairs.txt'), 'w') as user_flairs:
                for k, v in user_flairs_ranking.items():
                    if float(v) >= user_flairs_ref_value:
                        try:
                            data_for_graph_user_flairs[k] =  v
                        except:
                            raise
                    user_flairs.write("{flair} {hits}\n".format(flair=k, hits=v))

            data_for_graph_user_flairs = OrderedDict(sorted(data_for_graph_user_flairs.items(), key=lambda t: t[1]))

            user_flairs_graph.x_labels = data_for_graph_user_flairs.keys()
            user_flairs_graph.add('Poster flairs', data_for_graph_user_flairs.values())

            with open(os.path.join(self._output_dir,'user_flairs.svg'), 'wb') as user_flairs_file:
                user_flairs_file.write(user_flairs_graph.render())
            
            section.embed(src='user_flairs.svg', id='posts_subjects', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')
            section.p('<a href="url">{link}</a>'.format(url='user_flairs.txt', link='All data here'), klass="raw-link")

        ## Posts

        try:
            posts_user_flairs_ranking = OrderedDict(sorted(self._data['posts']['flair-presence'].items(),key=lambda t: t[1],reverse=True))
        except KeyError:
            pass
        else:
            section = self._page.section()
            posts_user_flairs_graph =  pygal.HorizontalBar()
            posts_user_flairs_graph.title = 'Distribution des flairs des posteurs'

            posts_user_flairs_ref_value = max(posts_user_flairs_ranking.values())/5

            data_for_graph_posts_user_flairs = OrderedDict()
            with open(os.path.join(self._output_dir, 'posts_user_flairs.txt'), 'w') as posts_user_flairs:
                for k, v in posts_user_flairs_ranking.items():
                    if float(v) >= posts_user_flairs_ref_value:
                        try:
                            data_for_graph_posts_user_flairs[k] =  v
                        except:
                            raise
                    posts_user_flairs.write("{flair} {hits}\n".format(flair=k, hits=v))

            data_for_graph_posts_user_flairs = OrderedDict(sorted(data_for_graph_posts_user_flairs.items(), key=lambda t: t[1]))

            posts_user_flairs_graph.x_labels = data_for_graph_posts_user_flairs.keys()
            posts_user_flairs_graph.add('Poster flairs', data_for_graph_posts_user_flairs.values())

            with open(os.path.join(self._output_dir,'posts_user_flairs.svg'), 'wb') as posts_user_flairs_file:
                posts_user_flairs_file.write(posts_user_flairs_graph.render())
            
            section.embed(src='posts_user_flairs.svg', id='posts_subjects', tipe='image/svg+xml', style='margin-left: 25%;', width='50%')
            section.p('<a href="url">{link}</a>'.format(url='posts_user_flairs.txt', link='All data here'), klass="raw-link")

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
            with open(os.path.join(self._output_dir,'posts_subjects.svg'), 'wb') as posts_subjects:
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
