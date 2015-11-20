from __future__ import unicode_literals

import HTMLParser
import urllib
import xbmc
import xbmcaddon
import xbmcvfs

addon_id = 'plugin.video.netflix'
addon_handle = xbmcaddon.Addon(addon_id)
main_url = 'https://www.netflix.com'
kids_url = 'https://www.netflix.com/Kids'
evaluator_url = 'http://www.netflix.com/api/%s/%s/pathEvaluator?materialize=true&model=harris'
profile_switch_url = 'http://api-global.netflix.com/desktop/account/profiles/switch?switchProfileGuid='
profile_url = 'https://www.netflix.com/ProfilesGate?nextpage=http%3A%2F%2Fwww.netflix.com%2FDefault'
picture_url = 'https://image.tmdb.org/t/p/original'
tmdb_url = 'https://api.themoviedb.org/3/search/%s?api_key=%s&query=%s&language=de'


def data_dir():
    return xbmc.translatePath('special://profile/addon_data/' + addon_id + '/')


def cache_dir():
    return xbmc.translatePath('special://profile/addon_data/' + addon_id + '/cache/')


def cover_cache_dir():
    return xbmc.translatePath('special://profile/addon_data/' + addon_id + '/cache/cover/')


def fanart_cache_dir():
    return xbmc.translatePath('special://profile/addon_data/' + addon_id + '/cache/fanart/')


def session_file():
    return xbmc.translatePath('special://profile/addon_data/' + addon_id + '/session')


def cookie_file():
    return xbmc.translatePath('special://profile/addon_data/' + addon_id + '/cookie')


def addon_dir():
    return addon_handle.getAddonInfo('path')


def addon_icon():
    return addon_handle.getAddonInfo('icon')


def addon_fanart():
    return addon_handle.getAddonInfo('fanart')


def log(message, loglevel=xbmc.LOGNOTICE):
    xbmc.log(encode(addon_id + ': ' + message), level=loglevel)


def notification(message):
    xbmc.executebuiltin(encode('Notification(Netflix: , %s, 5000, %s)' % (message, addon_icon())))


def open_setting():
    return addon_handle.openSettings()


def get_setting(name):
    return addon_handle.getSetting(name)


def set_setting(name, value):
    addon_handle.setSetting(name, value)


def get_string(string_id):
    return addon_handle.getLocalizedString(string_id)


def decode(string):
    return string.decode('utf-8')


def encode(string):
    return string.encode('utf-8')


def clean_content(string):
    string = string.replace('\\t', '')
    string = string.replace('\\n', '')
    string = string.replace('\\u2013', unicode('\u2013'))
    string = string.replace('\\u201c', unicode('\u201C'))
    string = string.replace('\\u201e', unicode('\u201E'))
    string = string.replace('\\', '')
    return string


def clean_filename(n, chars=None):
    if isinstance(n, str):
        return (''.join(c for c in unicode(n, 'utf-8') if c not in '/\\:?"*|<>')).strip(chars)
    elif isinstance(n, unicode):
        return (''.join(c for c in n if c not in '/\\:?"*|<>')).strip(chars)


def unescape(string):
    html_parser = HTMLParser.HTMLParser()
    return html_parser.unescape(string)


def prepare_folders():
    if not xbmcvfs.exists(data_dir()):
        xbmcvfs.mkdir(data_dir())
    if not xbmcvfs.exists(cache_dir()):
        xbmcvfs.mkdir(cache_dir())
    if not xbmcvfs.exists(cover_cache_dir()):
        xbmcvfs.mkdir(cover_cache_dir())
    if not xbmcvfs.exists(fanart_cache_dir()):
        xbmcvfs.mkdir(fanart_cache_dir())


def parameters_to_dictionary(parameters):
    parameter_dictionary = {}
    if parameters:
        parameter_pairs = parameters[1:].split('&')
        for parameter_pair in parameter_pairs:
            parameter_splits = parameter_pair.split('=')
            if (len(parameter_splits)) == 2:
                parameter_dictionary[parameter_splits[0]] = parameter_splits[1]
    return parameter_dictionary


def get_parameter(parameters, parameter):
    return urllib.unquote_plus(parameters.get(parameter, ''))


def progress_window(window_handle, value, message):
    window_handle.update(value, '', message, '')
    if window_handle.iscanceled():
        return False
    else:
        return True


def keyboard():
    keyboard_handle = xbmc.Keyboard('', get_string(30111))
    keyboard_handle.doModal()
    if keyboard_handle.isConfirmed() and keyboard_handle.getText():
        search_string = urllib.quote_plus(keyboard_handle.getText())
    else:
        search_string = None
    return search_string
