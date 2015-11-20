from __future__ import unicode_literals

import base64
import urllib

import list
import resources.lib.tmdbsimple as tmdbsimple
import utility

tmdbsimple.API_KEY = base64.b64decode('NDc2N2I0YjJiYjk0YjEwNGZhNTUxNWM1ZmY0ZTFmZWM=')
language = utility.get_setting('language').split('-')[0]


def netflix(video_type):
    search_string = utility.keyboard()
    if search_string:
        list.search(search_string, video_type)


def tmdb(video_type, title, year=None):
    search = tmdbsimple.Search()
    if video_type.startswith('tv'):
        content = search.tv(query=utility.encode(title), first_air_date_year=year, language=language,
                            include_adult='true')
        if content['total_results'] == 0:
            content = search.tv(query=utility.encode(title), language=language, include_adult='true')
            if content['total_results'] == 0:
                if '(' in title:
                    title = title[:title.find('(')]
                    content = search.tv(query=utility.encode(title), first_air_date_year=year, language=language,
                                        include_adult='true')
                elif ':' in title:
                    title = title[:title.find(':')]
                    content = search.tv(query=utility.encode(title), first_air_date_year=year, language=language,
                                        include_adult='true')
    else:
        content = search.movie(query=utility.encode(title), year=year, language=language, include_adult='true')
        if content['total_results'] == 0:
            content = search.movie(query=utility.encode(title), language=language, include_adult='true')
            if content['total_results'] == 0:
                if '(' in title:
                    title = title[:title.find('(')]
                    content = search.movie(query=utility.encode(title), year=year, language=language,
                                           include_adult='true')
                elif ':' in title:
                    title = title[:title.find(':')]
                    content = search.movie(query=utility.encode(title), year=year, language=language,
                                           include_adult='true')
    if content['total_results'] == 0:
        content = search.movie(query=utility.encode(title), year=year, language=language, include_adult='true')
    return content


def trailer(video_type, tmdb_id):
    content = None
    if video_type.startswith('tv'):
        try:
            content = tmdbsimple.TV(tmdb_id).videos()
        except Exception:
            pass
    else:
        try:
            content = tmdbsimple.Movies(tmdb_id).videos()
        except Exception:
            pass
    return content
