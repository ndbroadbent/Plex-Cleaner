#!/usr/bin/python
# -*- coding: utf-8 -*-

# PlexCleaner based on PlexAutoDelete by Steven4x4 with modifications from others
# Rewrite done by ngovil21 to make the script more cohesive and updated for Plex Home
# Version 1.1 - Added option dump and load settings from a config file
# Version 1.7 - Added options for Shared Users
# Version 1.8 - Added Profies
# Version 1.9 - Added options for checking watch status for multiple users in Plex Home
# Version 1.91 - Added ability to select section by title, preparation for new config
# Version 1.92 - Add ignored folders
# Version 1.93 - Add ability to chose log file mode.
# Version 1.94 - Save client id in config file to have use the same device everytime.
# Version 1.95 - Added the ability to cleanup old PlexCleaner devices and reload encoding as commandline arguments
# Version 1.96 - Modified files are printed at the end of the log as well now.
# Version 2.0 - Added ability to email log summary thanks to stevenflesch
# Version 2.01 - Email log only when action completed by default, calculate sizes of files changed
# Version 2.02 - Allow checking shared users by token, allow any user check, bug fixes
# Version 2.03 - Revamp token handling, able to store multiple tokens and check users accordingly

## Config File ###########################################################
# All settings in the config file will overwrite the settings here
Config = ""  # Location of a config file to load options from, can be specified in the commandline with --config [CONFIG_FILE]

## Global Settings #######################################################
Host = ""  # IP Address of the Plex Media Server, by default 127.0.0.1 will be used
Port = ""  # Port of the Plex Media Server, by default 32400 will be used
SectionList = []  # Sections to clean. If empty all sections will be looked at, the section id should be used here which is the number found be in the url on PlexWeb after /section/[ID]
IgnoreSections = []  # Sections to skip cleaning, for use when Settings['SectionList'] is not specified, the same as SectionList, the section id should be used here
LogFile = ""  # Location of log file to save console output
LogFileMode = "overwrite"  # File Mode for logging, overwrite or append, default is overwrite
trigger_rescan = False  # trigger_rescan will rescan a section if changes are made to it
EmailLog = False  # Email the log file contents at conclusion of script
EmailServer = ""  # Email Server (for Gmail, use smtp.gmail.com)
EmailServerPort = 0  # Email Server Port (for Gmail, use 587)
EmailServerUseTLS = False  # Email Server - whether or not to use TLS (for Gmail, use true)
EmailUsername = ""  # Email server username
EmailPassword = ""  # Email server password - if using Gmail, you can use an "app password" so your regular email password isn't in plain text in your config. See: https://myaccount.google.com/apppasswords
EmailRecipient = ""  # Email address to receive the log file contents, if enabled.

# Use Username/Password or Token for servers with PlexHome
# To generate a proper Token, first put your username and password and run the script with the flag --test.
# The Token will be printed in the console or in the logs. Tokens are preferred so that you password is not in
# a readable file.
# Shared is for users that you have invited to the server. This will use their watch information. Be careful with
# what the default show settings are because deleting files will be done by the OS. To help map the server for
# Shared users, you can specify the server friendly name or machine identifier.
Username = ""
Password = ""
# or you may directly give the token. This can be saved in the config file and is preferred after first run.
# You may also give the Token as a dict structure, with 'username' : 'TOKEN' to define Shared/Home User tokens as
# well. The admin token should be defined with the key '*'.
Token = ""
Shared = False
DeviceName = ""
# Remote Mapping ##########################################################
# For use with managing a remote Plex Media Server that is locally mounted
# This will replace the prefix of the remote file path with the local mount point.
RemoteMount = ""  # Path on the remote server to the media files
LocalMount = ""  # Path on the local computer to the media files
##########################################################################

## DEFAULT SETTINGS PER SHOW #############################################
# These are the default actions that are applied to each show.
#
# default_action can be set to 'delete','copy','move', 'keep'
# 'delete' will delete the file from the system
# 'copy' will copy the file to the location given
# 'move' will move the file to the location given
# 'keep' will do nothing to the file
# 'flag' will do nothing to the file, but still keep track of stats
default_action = 'flag'  # 'keep' | 'move' | 'copy' | 'delete' | 'flag'
# plex_delete if set to True will use the Plex API to delete files instead of using system functions
# Useful for remote plex installations
plex_delete = False  # True | False
# similar_files if set to True will try to move/copy/delete files with similar file names to the media file
# Note: delete_similar will not work with plex_delete
similar_files = True  # True | False
# cleanup_movie_folders if set to True will delete folders in movie section path that are less than a certain
# size in megabytes that is set in minimum_folder_size. This is used to cleanup orphaned movie folders when
# a movie file has been deleted by the script or through Plex. Only scanned sections will be affected.
# CAUTION: If you have Plex libraries that are in subdirectories of other libraries, the subdirectory may be deleted!
cleanup_movie_folders = False
# minimum_folder_size is the size in megabytes under which a movie folder will be deleted, set to much less,
# than your smallest movie file. If you keep a large amount of extra feature files, this value may need to be adjusted
minimum_folder_size = 30
# default_episodes will keep a certain number of episodes for a show
# If the number of episodes is greater than the default_episodes, older episodes will be deleted
# unless other criteria such as default_watched, default_onDeck, default_minDays are not met
default_episodes = 0  # Number of episodes to keep
# default_watched if set to False will be disabled. If set to True, only episodes that have been
# watched will be deleted if all other criteria are met
default_watched = True  # True | False
# default_onDeck if set to False will be disabled. If set to True, episodes that are On Deck in Plex
# will not be deleted
default_onDeck = True  # True | False
# default_rated if set to False will be disabled. If set to True, episodes that are rated in Plex
# will not be deleted
default_rated = False # True | False
# default_minDays specifies the minimum number of days to keep an episode. Episodes added more than
# default_minDays ago will be deleted. If default_watched is True, then days from the last watched date
# will be used
default_minDays = 0  # Minimum number of days to keep
# default_maxDays specifies the maximum number of days to keep an episode. Episodes added more than
# default)maxDays ago will be deleted. If default_watched is True, then days from the last watched date
# will be used
default_maxDays = 60  # Maximum number of days to keep an episode
# default_location specifies the location that episodes will be copied or moved to if the action is such
# make sure this is the path to the directory on the local computer
default_location = ''  # /path/to/file
# default_homeUsers specifies the home users that the script will try to check watch status of in Plex Home
# This will check if all users in the list have watched a show. Separate each user with a comma
# You may use 'all' for the home Users and the script will check watch status of all the users in the Plex Home (Including Guest account if enabled)
# You may also use 'any' to check if any of the homeUsers has watched the show and fulfills the requirements
# You may add shared users by using their tokens prepended with a '_' i.e. if the token is TOKEN123, use $TOKEN123
# It is probably better to list the users explicitly
default_homeUsers = ''  # 'Bob,Joe,Will'
# if set to anything > 0, videos with watch progress greater than this will be considered watched
default_progressAsWatched = 0  # Progress percentage to consider video as watched
# list of folders to ignore for processing
default_ignoreFolders = []  # Files that are under any of these folders on the Plex Server will not be processed
##########################################################################

## CUSTOMIZED SHOW SETTINGS ##############################################
# Customized Settings for certain shows. Use this to override default settings.
# Only the settings that are being changed need to be given. The setting will match the default settings above
# You can also specify an id instead of the Show Name. The id is the id assigned by Plex to the show
# Ex: 'Show Name':{'episodes':3,'watched':True/False,'minDays':,'action':'copy','location':'/path/to/folder','homeUsers':'Billy,Bob,Joe'},
# Make sure each show is separated by a comma. Use this for TV shows
ShowPreferences = {
    "Show 1": {"episodes": 3, "watched": True, "minDays": 10, "action": "delete", "location": "/path/to/folder",
               "onDeck": True, "rated": True, "maxDays": 30, "homeUsers": 'Bob,Joe,Will'},
    "Show 2": {"episodes": 0, "watched": False, "minDays": 10, "action": "delete", "location": "/path/to/folder",
               "onDeck": False, "rated": False, "maxDays": 30},
    "Show 3": {"action": "keep"},  # This show will skipped
    "Show Preferences": {}  # Keep this line
}
# Movie specific settings, settings you would like to apply to movie sections only. These settings will override the default
# settings set above. Change the default value here or in the config file. Use this for Movie Libraries.
MoviePreferences = {
    # 'watched': default_watched,  # Delete only watched episodes
    # 'minDays': default_minDays,  # Minimum number of days to keep
    # 'action': default_action,  # Action to perform on movie files (delete/move/copy)
    # 'location': default_location,  # Location to keep movie files
    # 'onDeck': default_onDeck  # Do not delete move if on deck
    # 'rated': default rated # Do not delete move if rated
}

# Profiles allow for customized settings based on Plex Collections. This allows managing of common settings using the Plex Web interface.
# First set the Profile here, then add the TV show to the collection in Plex.
Profiles = {
    "Profile 1": {"episodes": 3, "watched": True, "minDays": 10, "action": "delete", "location": "/path/to/folder",
                  "onDeck": True, "rated": True, "maxDays": 30, 'homeUsers': ''}
}
##########################################################################

## DO NOT EDIT BELOW THIS LINE ###########################################
import os
import xml.dom.minidom
import platform
import re
import shutil
import datetime
import glob
import sys
import logging
import json
import argparse
from collections import OrderedDict
import time
import uuid
import math

from time import sleep
import traceback

try:  # Python2 email imports
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.Utils import formatdate
except:  # Python3 email imports
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import formatdate

import smtplib

try:
    import configparser as ConfigParser
except:
    import ConfigParser

try:
    import urllib.request as urllib2
    from urllib.error import HTTPError
except:
    from urllib2 import HTTPError
    import urllib2

CONFIG_VERSION = 2.0
home_user_tokens = {}
machine_client_identifier = ''


def convert_size(size_bytes):
    if (size_bytes == 0):
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return '%s %s' % (s, size_name[i])


def log(msg, debug=False, error=False):
    if error:
        ErrorLog.append(msg)
    try:
        if LogToFile:
            if debug:
                logging.debug(msg)
            else:
                logging.info(msg)
    except:
        print("[ERROR] Error logging message")
    try:
        print(msg.encode('ascii', 'replace').decode())
    except:
        print("Cannot print message")


def fetchToken(user, passw):
    try:
        from urllib import urlencode  # Python2
    except:
        import urllib
        from urllib.parse import urlencode  # Python3

    data = urlencode({b"user[login]": user, b"user[password]": passw}).encode("utf-8")
    URL = "https://plex.tv/users/sign_in.json"
    headers = {
        'X-Plex-Device-Name': 'PlexCleaner',
        'X-Plex-Username': user,
        'X-Plex-Platform': platform.system(),
        'X-Plex-Device': platform.system(),
        'X-Plex-Platform-Version': platform.release(),
        'X-Plex-Provides': 'Python',
        'X-Plex-Product': 'Python',
        'X-Plex-Client-Identifier': Settings.get('Client_ID', "506c6578436c65616e6572"),
        'X-Plex-Version': str(CONFIG_VERSION)
        # 'Authorization': 'Basic ' + str(encode)
    }
    try:
        if sys.version < '3':
            req = urllib2.Request(URL, data, headers)
            response = urllib2.urlopen(req)
            str_response = response.read()
        else:
            req = urllib.request.Request(URL, data, headers)
            response = urllib.request.urlopen(req)
            str_response = response.read().decode('utf-8')

        loaded = json.loads(str_response)
        return loaded['user']['authentication_token']
    except Exception as e:
        log("[ERROR] Unable to obtain Token: %s" % e, debug=True, error=True)
        if debug_mode:
            log(str(traceback.format_exc()))
        return ""


# For Shared users, get the Access Token for the server, get the https url as well
def getAccessToken(token):
    resources = getURLX("https://plex.tv/api/resources?includeHttps=1", token=token)
    if not resources:
        log("[ERROR] Unable to get access token for token ending with: " + token[-4:], error=True)
        return ""
    devices = resources.getElementsByTagName("Device")
    for device in devices:
        if len(devices) == 1 or machine_client_identifier == device.getAttribute("clientIdentifier") or \
                (Settings['DeviceName'] and (
                                Settings['DeviceName'].lower() in device.getAttribute('name').lower() or Settings[
                            'DeviceName'].lower() in device.getAttribute('clientIdentifier').lower())):
            access_token = device.getAttribute('accessToken')
            if not access_token:
                log("[ERROR] Unable to get access token for token ending with: " + token[-4:], error=True)
                return ""
            return access_token
        connections = device.getElementsByTagName("Connection")
        for connection in connections:
            if connection.getAttribute('address') == Settings['Host']:
                access_token = device.getAttribute("accessToken")
                if not access_token:
                    return ""
                uri = connection.getAttribute('uri')
                match = re.compile("(http[s]?:\/\/.*?):(\d*)").match(uri)
                if match:
                    Settings['Host'] = match.group(1)
                    Settings['Port'] = match.group(2)
                return access_token
    return ""

def getToken(key=None):
    if isinstance(Settings['Token'], dict):
        if key:
            return Settings['Token'].get(key)
        else:
            if len(Settings['Token']) == 1:
                return Settings['Token'].values()[0]
            for k in Settings['Token'].keys():
                if k.endswith('*'):
                    return Settings['Token'][k]
            log("[ERROR] No default key specified!", error=True)
            return None
    return Settings['Token']


def getPlexHomeUserTokens():
    global home_user_tokens
    homeUsers = getURLX("https://plex.tv/api/home/users")
    user_tokens = {}
    if homeUsers:
        # print(homeUsers.toprettyxml())
        user_tokens = {}
        for user in homeUsers.getElementsByTagName("User"):
            user_id = user.getAttribute("id")
            switch_page = getURLX("https://plex.tv/api/home/users/" + user_id + "/switch",
                                  data=b'')  # Empty byte data to send a 'POST'
            if switch_page:
                user_element = switch_page.getElementsByTagName('user')[0]
                username = str(user_element.getAttribute("title")).lower()
                home_token = user_element.getAttribute('authenticationToken')
                if home_token:
                    user_tokens[username] = getAccessToken(home_token)
        home_user_tokens = user_tokens
        if debug_mode:
            print("home user tokens: " + str(user_tokens))
    else:
        print("Cannot load page!")
        home_user_tokens = {}


# Load Settings from json into an OrderedDict, with defaults
def LoadSettings(opts):
    s = OrderedDict()
    s['test'] = opts.get('test', False)
    s['Host'] = opts.get('Host', Host)
    s['Port'] = opts.get('Port', Port)
    s['SectionList'] = opts.get('SectionList', SectionList)
    s['IgnoreSections'] = opts.get('IgnoreSections', IgnoreSections)
    s['LogFile'] = opts.get('LogFile', LogFile)
    s['LogFileMode'] = opts.get('LogFileMode', LogFileMode)
    s['trigger_rescan'] = opts.get('trigger_rescan', trigger_rescan)
    s['EmailLog'] = opts.get('EmailLog', EmailLog)
    s['EmailServer'] = opts.get('EmailServer', EmailServer)
    s['EmailServerPort'] = opts.get('EmailServerPort', EmailServerPort)
    s['EmailServerUseTLS'] = opts.get('EmailServerUseTLS', EmailServerUseTLS)
    s['EmailUsername'] = opts.get('EmailUsername', EmailUsername)
    s['EmailPassword'] = opts.get('EmailPassword', EmailPassword)
    s['EmailRecipient'] = opts.get('EmailRecipient', EmailRecipient)
    s['Token'] = opts.get('Token', Token)
    s['Username'] = opts.get('Username', Username)
    s['Password'] = opts.get('Password', Password)
    s['Shared'] = opts.get('Shared', Shared)
    s['DeviceName'] = opts.get('DeviceName', DeviceName)
    s['RemoteMount'] = opts.get('RemoteMount', RemoteMount)
    s['LocalMount'] = opts.get('LocalMount', LocalMount)
    s['plex_delete'] = opts.get('plex_delete', plex_delete)
    s['similar_files'] = opts.get('similar_files', similar_files)
    s['cleanup_movie_folders'] = opts.get('cleanup_movie_folders', cleanup_movie_folders)
    s['minimum_folder_size'] = opts.get('minimum_folder_size', minimum_folder_size)
    s['default_episodes'] = opts.get('default_episodes', default_episodes)
    s['default_minDays'] = opts.get('default_minDays', default_minDays)
    s['default_maxDays'] = opts.get('default_maxDays', default_maxDays)
    s['default_action'] = opts.get('default_action', default_action)
    s['default_watched'] = opts.get('default_watched', default_watched)
    s['default_progressAsWatched'] = opts.get('default_progressAsWatched', default_progressAsWatched)
    s['default_location'] = opts.get('default_location', default_location)
    s['default_onDeck'] = opts.get('default_onDeck', default_onDeck)
    s['default_rated'] = opts.get('default_rated', default_rated)
    s['default_homeUsers'] = opts.get('default_homeUsers', default_homeUsers)
    s['default_ignoreFolders'] = opts.get('default_ignoreFolders', default_ignoreFolders)
    s['ShowPreferences'] = OrderedDict(sorted(opts.get('ShowPreferences', ShowPreferences).items()))
    s['MoviePreferences'] = OrderedDict(sorted(opts.get('MoviePreferences', MoviePreferences).items()))
    s['Profiles'] = OrderedDict(sorted(opts.get('Profiles', Profiles).items()))
    s['Version'] = opts.get('Version', CONFIG_VERSION)
    s['Client_ID'] = opts.get('Client_ID', None)
    return s


def dumpSettings(output):
    # Remove old settings
    if 'End Preferences' in Settings['ShowPreferences']:
        Settings['ShowPreferences'].pop('End Preferences')
    if 'Movie Preferences' in Settings['MoviePreferences']:
        Settings['MoviePreferences'].pop('Movie Preferences')
    Settings['ShowPreferences'] = OrderedDict(sorted(Settings['ShowPreferences'].items()))
    Settings['MoviePreferences'] = OrderedDict(sorted(Settings['MoviePreferences'].items()))
    Settings['Profiles'] = OrderedDict(sorted(Settings['Profiles'].items()))
    Settings['Version'] = CONFIG_VERSION
    with open(output, 'w') as outfile:
        json.dump(Settings, outfile, indent=2)


def getURLX(URL, data=None, parseXML=True, max_tries=1, timeout=0.5, referer=None, token=None, method=None):
    if not token:
        token = getToken()
    if not URL.startswith('http'):
        URL = 'http://' + URL
    for x in range(0, max_tries):
        if x > 0:
            sleep(timeout*x)
        try:
            headers = {
                "X-Plex-Token": token,
                'X-Plex-Platform': platform.system(),
                'X-Plex-Device': platform.system(),
                'X-Plex-Device-Name': 'PlexCleaner',
                'X-Plex-Platform-Version': platform.release(),
                'X-Plex-Provides': 'controller',
                'X-Plex-Product': 'Python',
                'X-Plex-Version': str(CONFIG_VERSION),
                'X-Plex-Client-Identifier': Settings['Client_ID'],
                'Accept': 'application/xml'
            }
            if Settings['Username']:
                headers['X-Plex-Username'] = Settings['Username']
            if referer:
                headers['Referer'] = referer
            req = urllib2.Request(url=URL, data=data, headers=headers)
            if method:
                req.get_method = lambda: method
            page = urllib2.urlopen(req)
            if page:
                if parseXML:
                    return xml.dom.minidom.parse(page)
                else:
                    return page
        except HTTPError as e:
            if e.code == 401:
                if debug_mode:
                    log("Unauthorized to access url with token.")
                return None                # Do not retry on unauthorized error, won't be fixed
            else:
                log("Error requesting page: %s" % e, debug=True)
                if debug_mode:
                    log(str(traceback.format_exc()))
                continue
        except Exception as e:
            log("Error requesting page: %s" % e, debug=True)
            if debug_mode:
                log(str(traceback.format_exc()))
            continue
    return None


# Returns if a file action was performed (move, copy, delete)
def performAction(file, action, media_id=0, location="", parentFolder=None):
    global DeleteCount, DeleteSize, MoveCount, MoveSize, CopyCount, CopySize, FlaggedCount, FlaggedSize

    try:
        if sys.version < '3':
            file = file.decode('utf-8')
    except:
        if debug_mode:
            log(str(traceback.format_exc()))

    file = getLocalPath(file)
    action = action.lower()
    if action.startswith('k'):  # Keep file
        log("[KEEPING] " + file)
        return False
    for path in Settings['default_ignoreFolders']:
        if file.startswith(path):
            log("File is in " + path)
            log("[IGNORED] " + file)
            return False
    is_file = False
    try:
        is_file = os.path.isfile(file)
    except UnicodeDecodeError:
        try:
            is_file = os.path.isfile(file.decode('utf-8'))
        except:
            if not args.reload_encoding:
                log("Unable to decode filename, try running script with --reload_encoding.")
            log("[NOT FOUND] " + file)
            return False
    except:
        log("[NOT FOUND] " + file)
        return False

    if test or action.startswith('f'):  # Test file or Flag file
        if not is_file:
            log("[NOT FOUND] " + file)
            return False
        if show_size:
            FlaggedSize += os.stat(file).st_size
        log("**[FLAGGED] " + file)
        ActionHistory.append("[FLAGGED] " + file)
        FlaggedCount += 1
        return False
    elif action.startswith('d') and Settings['plex_delete']:  # Delete using Plex Web API
        try:
            if show_size and is_file:  # If using plex_delete, check if we can access file
                DeleteSize += os.stat(file).st_size
            URL = (Settings['Host'] + ":" + Settings['Port'] + "/library/metadata/" + str(media_id))
            req = getURLX(URL, max_tries=1, method='DELETE', parseXML=False)
            if not req:
                log("Unable to plex delete file: %s" % file)
                return False
            DeleteCount += 1
            log("**[DELETED] " + file)
            ActionHistory.append("[DELETED] " + file)
            return True
        except Exception as e:
            log("[ERROR] Cannot delete file: %s" % e, debug=True, error=True)
            if debug_mode:
                log(str(traceback.format_exc()))
            return False
    if not is_file:
        log("[NOT FOUND] " + file)
        return False
    if Settings['similar_files']:
        regex = re.sub("\[", "[[]", os.path.splitext(file)[0]) + "*"
        log("[INFO] Finding files similar to: " + regex)
        filelist = glob.glob(regex)
    else:
        filelist = (file,)
    if action.startswith('c'):
        try:
            for f in filelist:
                if show_size:
                    CopySize += os.stat(f).st_size
                shutil.copy(os.path.realpath(f), location)
                log("**[COPIED] " + file)
            ActionHistory.append("[COPIED] " + filelist[0])
            CopyCount += 1
            return True
        except Exception as e:
            log("[ERROR] Error copying file: %s" % e, debug=True, error=True)
            return False
    elif action.startswith('m'):
        for f in filelist:
            try:
                if show_size:
                    MoveSize += os.stat(f).st_size
                os.utime(os.path.realpath(f), None)
                shutil.move(os.path.realpath(f), location)
                log("**[MOVED] " + f)
            except Exception as e:
                log("[ERROR] Error moving file: %s" % e, debug=True, error=True)
                return False
            if os.path.islink(f):
                os.unlink(f)
        ActionHistory.append("[MOVED] " + filelist[0])
        MoveCount += 1
        return True
    elif action.startswith('d'):
        for f in filelist:
            try:
                if show_size:
                    DeleteSize += os.stat(f).st_size
                os.remove(f)
                log("**[DELETED] " + f)
            except Exception as e:
                log("[ERROR] Error deleting file: %s" % e, debug=True, error=True)
                continue
        ActionHistory.append("[DELETED] " + filelist[0])
        DeleteCount += 1
        return True
    else:
        log("[FLAGGED] " + file)
        ActionHistory.append("[FLAGGED] " + file)
        FlaggedCount += 1
        if show_size and os.path.isfile(file):
            FlaggedSize += os.stat(file).st_size
        return False


def get_input(prompt=""):
    if sys.version < 3:
        return raw_input(prompt)
    else:
        return input(prompt)

def CheckIsRated(media_id):
    global RatedCount
    for VideoNode in doc.getElementsByTagName("Video"):
        if VideoNode.getAttribute("ratingKey") == str(media_id):
            if VideoNode.hasAttribute("userRating"):
                RatedCount += 1
                return True
    return False

def CheckOnDeck(media_id):
    global OnDeckCount
    if not deck:
        return False
    for DeckVideoNode in deck.getElementsByTagName("Video"):
        if DeckVideoNode.getAttribute("ratingKey") == str(media_id):
            OnDeckCount += 1
            return True
    return False


# Crude method to replace a remote path with a local path. Hopefully python properly takes care of file separators.
def getLocalPath(file):
    if Settings['RemoteMount'] and Settings['LocalMount']:
        if file.startswith(Settings['RemoteMount']):
            file = os.path.normpath(file.replace(Settings['RemoteMount'], Settings['LocalMount'], 1))
    return file


# gets the total size of a file in bytes, recursively searches through folders
def getTotalSize(file):
    total_size = os.path.getsize(file)
    if os.path.isdir(file):
        for item in os.listdir(file):
            itempath = os.path.join(file, item)
            if os.path.isfile(itempath):
                total_size += os.path.getsize(itempath)
            elif os.path.isdir(itempath):
                total_size += getTotalSize(itempath)
    return total_size


def getMediaInfo(VideoNode):
    view = VideoNode.getAttribute("viewCount")
    if view == '':
        view = 0
    view = int(view)
    ################################################################
    ###Find number of days between date video was viewed and today
    lastViewedAt = VideoNode.getAttribute("lastViewedAt")
    if lastViewedAt == '':
        DaysSinceVideoLastViewed = 0
    else:
        d1 = datetime.datetime.today()
        d2 = datetime.datetime.fromtimestamp(float(lastViewedAt))
        DaysSinceVideoLastViewed = (d1 - d2).days
    ################################################################
    ################################################################
    ###Find number of days between date video was added and today
    addedAt = VideoNode.getAttribute("addedAt")
    if addedAt == '':
        DaysSinceVideoAdded = 0
    else:
        d1 = datetime.datetime.today()
        da2 = datetime.datetime.fromtimestamp(float(addedAt))
        DaysSinceVideoAdded = (d1 - da2).days
    if VideoNode.hasAttribute('viewOffset') and VideoNode.hasAttribute('duration'):
        progress = int(VideoNode.getAttribute('viewOffset')) * 100 / int(VideoNode.getAttribute('duration'))
    else:
        progress = 0
    ################################################################
    MediaNode = VideoNode.getElementsByTagName("Media")
    media_id = VideoNode.getAttribute("ratingKey")
    for Media in MediaNode:
        PartNode = Media.getElementsByTagName("Part")
        for Part in PartNode:
            file = Part.getAttribute("file")
            if sys.version < '3':  # remove HTML quoted characters, only works in python < 3
                file = urllib2.unquote(file.encode('utf-8'))
            else:
                file = urllib2.unquote(file)
            return {'view': view, 'DaysSinceVideoAdded': DaysSinceVideoAdded,
                    'DaysSinceVideoLastViewed': DaysSinceVideoLastViewed, 'file': file, 'media_id': media_id,
                    'progress': progress}


def checkUsersWatched(users, media_id, progress_as_watched):
    compareDay = -1
    any_user = users == ['any'] or users == 'any'
    if users == 'all' or any_user:
        if isinstance(Settings['Token'], dict):
            users = Settings['Token'].keys()
        else:
            if not home_user_tokens:
                getPlexHomeUserTokens()
            users = home_user_tokens.keys()
    for u in users:
        toke = None
        if u in Settings['Token']:
            toke = Settings['Token'].get(u, 0)
        else:
            if u.startswith("_"):
                toke = u[1:]
            elif not home_user_tokens:
                getPlexHomeUserTokens()
            if u in home_user_tokens:
                toke = home_user_tokens[u]
        if toke:
            DaysSinceVideoLastViewed = checkUserWatched(toke, media_id, progress_as_watched)
        else:
            log("[ERROR] Do not have the token for " + u + ". Please check spelling or token.", error=True)
            return -1
        if any_user:
            if compareDay == -1 or DaysSinceVideoLastViewed > compareDay:  # Find the user who has seen the episode first for ANY user
                compareDay = DaysSinceVideoLastViewed
        elif DaysSinceVideoLastViewed == -1:
            log("[INFO] " + u + " has not seen video " + media_id)
            return -1                                                    #Shortcut out, user in list has not seen video
        elif compareDay == -1 or DaysSinceVideoLastViewed < compareDay:  # Find the user who has seen the episode last, minimum DSVLW
            compareDay = DaysSinceVideoLastViewed
    return compareDay


def checkUserWatched(token, media_id, progress_as_watched):
    user_media_page = getURLX(Settings['Host'] + ":" + Settings['Port'] + '/library/metadata/' + media_id,
                              token=token)
    if user_media_page:
        video = user_media_page.getElementsByTagName("Video")[0]
        videoProgress = 0
        if video.hasAttribute('viewOffset') and video.hasAttribute('duration'):
            videoProgress = int(video.getAttribute('viewOffset')) * 100 / int(video.getAttribute('duration'))
        if (video.hasAttribute('viewCount') and int(video.getAttribute('viewCount')) > 0) or (
                        progress_as_watched > 0 and videoProgress > progress_as_watched):
            lastViewedAt = video.getAttribute('lastViewedAt')
            if not lastViewedAt or lastViewedAt == '' or lastViewedAt == '0':
                return 0
            else:
                d1 = datetime.datetime.today()
                d2 = datetime.datetime.fromtimestamp(float(lastViewedAt))
                return (d1 - d2).days
    # Video has not been seen by this user or not accessible, return -1 for unseen
    return -1


# Movies are all listed on one page
def checkMovies(document, section):
    global FileCount
    global KeptCount
    global KeptSize

    changes = 0
    for VideoNode in document.getElementsByTagName("Video"):
        movie_settings = default_settings.copy()
        movie_settings.update(Settings['MoviePreferences'])
        title = VideoNode.getAttribute("title")
        movie_id = VideoNode.getAttribute("ratingKey")
        m = getMediaInfo(VideoNode)
        onDeck = CheckOnDeck(movie_id)
        isRated = CheckIsRated(movie_id)
        collections = VideoNode.getElementsByTagName("Collection")
        for collection in collections:
            collection_tag = collection.getAttribute('tag')
            if collection_tag and collection_tag in Settings['Profiles']:
                movie_settings.update(Settings['Profiles'][collection_tag])
                print("Using profile: " + collection_tag)
        if debug_mode:
            log(str(movie_settings), True)
        check_users = []
        if movie_settings['homeUsers']:
            check_users = movie_settings['homeUsers'].strip(" ,").lower().split(",")
            for j in range(0, len(check_users)):  # Remove extra spaces and commas
                check_users[j] = check_users[j].strip(", ")
        if movie_settings['watched']:
            if check_users:
                movie_settings['onDeck'] = False
                watchedDays = checkUsersWatched(check_users, m['media_id'], movie_settings['progressAsWatched'])
                if watchedDays == -1:
                    m['view'] = 0
                    compareDay = 0
                else:
                    m['view'] = 1
                    if watchedDays > m['DaysSinceVideoAdded']:
                        compareDay = m['DaysSinceVideoAdded']
                    else:
                        compareDay = watchedDays
            elif m['DaysSinceVideoLastViewed'] > m['DaysSinceVideoAdded']:
                compareDay = m['DaysSinceVideoAdded']
            else:
                compareDay = m['DaysSinceVideoLastViewed']
            log("%s | Viewed: %d | Days Since Viewed: %d | On Deck: %s | Rated: %s" % (
                title, m['view'], compareDay, onDeck, isRated))
            checkedWatched = (m['view'] > 0 or (0 < movie_settings['progressAsWatched'] < m['progress']))
        else:
            compareDay = m['DaysSinceVideoAdded']
            log("%s | Viewed: %d | Days Since Viewed: %d | On Deck: %s | Rated: %s" % (
                title, m['view'], compareDay, onDeck, isRated))
            checkedWatched = True
        FileCount += 1
        checkDeck = False
        if movie_settings['onDeck']:
            checkDeck = onDeck
        checkRated = False
        if movie_settings['rated']:
            checkRated = isRated
        check = (not movie_settings['action'].startswith('k')) and checkedWatched and (
            compareDay >= movie_settings['minDays']) and (not checkDeck) and (not checkRated)
        if check:
            if performAction(file=m['file'], action=movie_settings['action'], media_id=movie_id,
                             location=movie_settings['location']):
                changes += 1
        else:
            log('[KEEPING] ' + m['file'])
            KeptCount += 1
            if show_size and os.path.isfile(m['file']):
                KeptSize += os.stat(m['file']).st_size
        log("")
    if Settings.get('cleanup_movie_folders', False):
        log("Cleaning up orphaned folders less than " + str(Settings['minimum_folder_size']) + "MB in Section " + section)
        cleanUpFolders(section, Settings['minimum_folder_size'])
    return changes


# Cleans up orphaned folders in a section that are less than the max_size (in megabytes)
def cleanUpFolders(section, max_size):
    for directory in doc_sections.getElementsByTagName("Directory"):
        if directory.getAttribute("key") == section:
            for location in directory.getElementsByTagName("Location"):
                ignore_folder = False
                for f in Settings['default_ignoreFolders']:
                    if location.getAttribute("path").startswith(f):
                        ignore_folder = True
                        break
                if ignore_folder:
                    continue
                path = getLocalPath(location.getAttribute("path"))
                if os.path.isdir(path):
                    for folder in os.listdir(path):
                        dir_path = os.path.join(path, folder)
                        if os.path.isdir(dir_path):
                            if len(
                                    folder) == 1:  # If folder name length is one assume videos are categorized alphabetically, search subdirectories
                                subfolders = os.listdir(dir_path)
                            else:
                                subfolders = (" ",)
                            for subfolder in subfolders:
                                subfolder_path = os.path.join(path, folder, subfolder).strip()
                                if os.path.exists(os.path.join(subfolder_path,
                                                               '.nodelete')):  # Do not delete folders that have .nodelete in them
                                    continue
                                size = getTotalSize(subfolder_path)
                                ignore_folder = False
                                for f in Settings['default_ignoreFolders']:
                                    if subfolder_path.startswith(f):
                                        ignore_folder = True
                                if ignore_folder:
                                    continue
                                if os.path.isdir(subfolder_path) and size < max_size * 1024 * 1024:
                                    try:
                                        if test:  # or default_action.startswith("f"):
                                            log("**[Flagged]: " + subfolder_path)
                                            log("Size " + str(size) + " bytes")
                                            continue
                                        shutil.rmtree(subfolder_path)
                                        log("**[DELETED] " + subfolder_path)
                                    except Exception as e:
                                        log("Unable to delete folder: %s" % e, True)
                                        continue


# Shows have a season pages that need to be navigated
def checkShow(showDirectory):
    global KeptCount
    global KeptSize
    global FileCount
    # Parse all of the episode information from the season pages
    show_settings = default_settings.copy()
    show_metadata = getURLX(
        Settings['Host'] + ":" + Settings['Port'] + '/library/metadata/' + showDirectory.getAttribute('ratingKey'))
    collections = show_metadata.getElementsByTagName("Collection")
    for collection in collections:
        collection_tag = collection.getAttribute('tag')
        if collection_tag and collection_tag in Settings['Profiles']:
            show_settings.update(Settings['Profiles'][collection_tag])
            print("Using profile: " + collection_tag)
    if debug_mode:
        log(str(show_settings), True)
    show = getURLX(Settings['Host'] + ":" + Settings['Port'] + showDirectory.getAttribute('key'))
    if not show:  # Check if show page is None or empty
        log("Failed to load show page. Skipping...")
        return 0
    media_container = show.getElementsByTagName("MediaContainer")[0]
    show_id = media_container.getAttribute('key')
    show_name = media_container.getAttribute('parentTitle')
    for key in Settings['ShowPreferences']:
        if (key.lower() in show_name.lower()) or (key == show_id):
            show_settings.update(Settings['ShowPreferences'][key])
            break
    # if action is keep then skip checking
    if show_settings['action'].startswith('k'):  # If keeping on show just skip checking
        log("[KEEPING] " + show_name)
        log("")
        return 0
    check_users = []
    if show_settings['homeUsers']:
        check_users = show_settings['homeUsers'].strip(" ,").lower().split(",")
        for k in range(0, len(check_users)):  # Remove extra spaces and commas
            check_users[k] = check_users[k].strip(", ")
    episodes = []
    for SeasonDirectoryNode in show.getElementsByTagName("Directory"):  # Each directory is a season
        if not SeasonDirectoryNode.getAttribute('type') == "season":  # Only process Seasons (skips Specials)
            continue
        season_key = SeasonDirectoryNode.getAttribute('key')
        season_num = str(SeasonDirectoryNode.getAttribute('index'))  # Directory index refers to the season number
        if season_num.isdigit():
            season_num = ("%02d" % int(season_num))
        season = getURLX(Settings['Host'] + ":" + Settings['Port'] + season_key)
        if not season:
            continue
        for VideoNode in season.getElementsByTagName("Video"):
            episode_num = str(VideoNode.getAttribute('index'))  # Video index refers to the episode number
            if episode_num.isdigit():  # Check if numeric index
                episode_num = ("%03d" % int(episode_num))
            if episode_num == "":  # if episode_num blank here, then use something else to get order
                episode_num = VideoNode.getAttribute('originallyAvailableAt')
                if episode_num == "":
                    episode_num = VideoNode.getAttribute('title')
                    if episode_num == "":
                        episode_num = VideoNode.getAttribute('addedAt')
            title = VideoNode.getAttribute('title')
            m = getMediaInfo(VideoNode)
            if show_settings['watched']:
                if check_users:
                    show_settings['onDeck'] = False
                    watchedDays = checkUsersWatched(check_users, m['media_id'], show_settings['progressAsWatched'])
                    if watchedDays == -1:
                        m['view'] = 0
                        compareDay = 0
                    else:
                        m['view'] = 1
                        if watchedDays > m['DaysSinceVideoAdded']:
                            compareDay = m['DaysSinceVideoAdded']
                        else:
                            compareDay = watchedDays
                elif m['DaysSinceVideoLastViewed'] > m['DaysSinceVideoAdded']:
                    compareDay = m['DaysSinceVideoAdded']
                else:
                    compareDay = m['DaysSinceVideoLastViewed']
            else:
                compareDay = m['DaysSinceVideoAdded']
            # key = '%sx%s' % (season_num, episode_num)  # store episode with key based on season number and episode number for sorting
            episodes.append({'season': season_num, 'episode': episode_num, 'title': title, 'view': m['view'],
                             'compareDay': compareDay, 'file': m['file'], 'media_id': m['media_id'],
                             'progress': m['progress']})
            FileCount += 1
    count = 0
    changes = 0
    # Sort episodes by season and episode
    episodes = sorted(episodes, key=lambda z: (z['season'], z['episode']))
    for k in range(0, len(episodes)):
        ep = episodes[k]
        onDeck = CheckOnDeck(ep['media_id'])
        isRated = CheckIsRated(ep['media_id'])
        if show_settings['watched']:
            log("%s - S%sxE%s - %s | Viewed: %d | Days Since Last Viewed: %d | On Deck: %s | Rated: %s" % (
                show_name, ep['season'], ep['episode'], ep['title'], ep['view'], ep['compareDay'], onDeck, isRated))
            checkWatched = (ep['view'] > 0 or (0 < show_settings['progressAsWatched'] < ep['progress']))
        else:
            log("%s - S%sxE%s - %s | Viewed: %d | Days Since Added: %d | On Deck: %s | Rated: %s" % (
                show_name, ep['season'], ep['episode'], ep['title'], ep['view'], ep['compareDay'], onDeck, isRated))
            checkWatched = True
        # if we have more episodes or it's been longer than the max days, then check if we can delete the file
        if ((len(episodes) - k) > show_settings['episodes']) or (ep['compareDay'] > show_settings['maxDays'] > 0):
            checkDeck = False
            if show_settings['onDeck']:
                checkDeck = onDeck or (k + 1 < len(episodes) and CheckOnDeck(episodes[k + 1]['media_id']))
                if debug_mode and checkDeck:
                    print("File is on deck, not deleting")
            checkRated = False
            if show_settings['rated']:
                checkRated = isRated or (k + 1 < len(episodes) and CheckIsRated(episodes[k + 1]['media_id']))   
                if debug_mode and checkRated:
                    print("File is rated, not deleting")
            check = (not show_settings['action'].startswith('k')) and checkWatched and (
                ep['compareDay'] >= show_settings['minDays']) and (not checkDeck) and (not checkRated)
            if check:
                if performAction(file=ep['file'], action=show_settings['action'], media_id=ep['media_id'],
                                 location=show_settings['location']):
                    changes += 1
            else:
                if debug_mode:
                    print("Watched status is %s, compare day is %d, checkDeck is %s, checkRated is %s" % (
                    str(checkWatched), ep['compareDay'], str(checkDeck), str(checkRated)))
                log('[KEEPING] ' + getLocalPath(ep['file']))
                KeptCount += 1
                if show_size and os.path.isfile(ep['file']):
                    KeptSize += os.stat(getLocalPath(ep['file'])).st_size
        else:
            if debug_mode:
                print("Episode is %d and max days is %s" % (
                len(episodes) - k, str(ep['compareDay'] > show_settings['maxDays'] > 0)))
                print(str(k))
            log('[KEEPING] ' + getLocalPath(ep['file']))
            KeptCount += 1
            if show_size and os.path.isfile(ep['file']):
                KeptSize += os.stat(getLocalPath(ep['file'])).st_size
        log("")
        count += 1
    return changes


def sendEmail(email_from, email_to, subject, body, server, port, username="", password="", secure=False,
              email_type='html'):
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(body, email_type))
    try:
        server = smtplib.SMTP(server, port)
        if secure:  # use TLS for secure connection
            server.ehlo()
            server.starttls()
            server.ehlo()
        if username:
            server.login(username, password)
        text = msg.as_string()
        senders = server.sendmail(email_from, email_to, text)
        server.quit()
    except Exception as e:
        log("Error in sending Email: " + e.message)
        if debug_mode:
            log(str(traceback.format_exc()))
        raise e
    return senders is None


## Main Script ############################################

if __name__ == "__main__":

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", "-test", help="Run the script in test mode", action="store_true", default=False)
    parser.add_argument("--dump", "-dump", help="Dump the settings to a configuration file and exit", nargs='?',
                        const="Cleaner.conf", default=None)
    parser.add_argument("--config", "-config", "--load", "-load",
                        help="Load settings from a configuration file and run with settings")
    parser.add_argument("--update_config", "-update_config", action="store_true",
                        help="Update the config file with new settings from the script and exit")
    parser.add_argument("--debug", "-debug", action="store_true", default=False,
                        help="Run script in debug mode to log more error information")
    parser.add_argument("--reload_encoding", "-reload_encoding", "--reload", "-reload", action="store_true", default=False,
                        help="Reload system with default encoding set to utf-8")
    parser.add_argument("--clean_devices", "-clean_devices", "--clean", "-clean",
                        help="Cleanup old PlexCleaner devices ids", action="store_true", default=False)
    parser.add_argument("--show_size", "-show_size", "--size", "-size", help="Show total size of files changed",
                        action="store_true", default=False)
    parser.add_argument("--always_email", "-always_email", "--email", "-email", help="Always email log, even if empty",
                        action="store_true", default=False)
    # parser.add_argument("--config_edit", "-config_edit", action="store_true",
    #                     help="Prompts for editing the config from the commandline")

    args = parser.parse_args()

    debug_mode = args.debug
    email_empty_log = args.always_email
    show_size = args.show_size

    if args.reload_encoding:
        # reload sys to set default encoding to utf-8
        try:
            reload(sys)
            sys.setdefaultencoding("utf-8")
        except:
            pass

    if args.config:
        Config = args.config
    # If no config file is provided, check if there is a config file in first the user directory, or the current directory.
    if Config == "":
        if os.path.isfile(os.path.join(os.path.expanduser("~"), ".plexcleaner")):
            Config = os.path.join(os.path.expanduser("~"), ".plexcleaner")
        elif os.path.isfile(os.path.join(sys.path[0], "Cleaner.conf")):
            Config = os.path.join(sys.path[0], "Cleaner.conf")
        elif os.path.isfile(os.path.join(sys.path[0], "Settings.cfg")):
            Config = os.path.join(sys.path[0], "Settings.cfg")
        elif os.path.isfile(".plexcleaner"):
            Config = ".plexcleaner"
        elif os.path.isfile("Cleaner.conf"):
            Config = "Cleaner.conf"

    Settings = OrderedDict()

    if Config and os.path.isfile(Config):
        print("Loading config file: " + Config)
        with open(Config, 'r') as infile:
            opt_string = infile.read().replace('\n', '')  # read in file removing breaks
            # Escape odd number of backslashes (Windows paths are a problem)
            opt_string = re.sub(r'(?x)(?<!\\)\\(?=(?:\\\\)*(?!\\))', r'\\\\', opt_string)
            options = json.loads(opt_string)
            Settings = LoadSettings(options)
        if ('Version' not in options) or not options['Version'] or (options['Version'] < CONFIG_VERSION):
            print("Old version of config file! Updating...")
            dumpSettings(Config)
    else:
        Settings = LoadSettings(Settings)

    test = args.test or Settings.get('test', False)

    if args.dump:
        # Output settings to a json config file and exit
        print("Saving settings to " + args.dump)
        dumpSettings(args.dump)
        print("Settings saved. Exiting...")
        exit()

    if test:
        print(json.dumps(Settings, indent=2, sort_keys=False))  # if testing print out the loaded settings in the console

    if args.update_config:
        if Config:
            # resp = get_input("Edit Settings in console? (y/n)")
            # if resp.lower().startswith("y"):
            #     while True:
            print("Updating Config file with current settings")
            dumpSettings(Config)
            exit()
        else:
            print("No config file found! Exiting!")
            exit()

    ErrorLog = []

    if Settings['Host'] == "":
        Settings['Host'] = "127.0.0.1"
    if Settings['Port'] == "":
        Settings['Port'] = "32400"

    LogToFile = False
    if not Settings['LogFile'] == "":
        LogToFile = True
        filemode = "w"
        if Settings.get("LogFileMode").startswith("a"):
            filemode = "a"
        logging.basicConfig(filename=Settings['LogFile'], filemode=filemode, level=logging.DEBUG)
        logging.captureWarnings(True)

    log("** Script started " + time.strftime("%m-%d-%Y %I:%M:%S%p"))
    log("")

    # If we don't have a client_id, generate a unique UID for machine and save in config
    if not Settings['Client_ID']:
        if Config:
            Settings['Client_ID'] = str(uuid.uuid1().hex)
            dumpSettings(Config)
        else:
            Settings['Client_ID'] = "506c6578436c65616e6572"  # PlexCleaner in Hexadecimal

    if not Settings['Token']:
        if Settings['Username']:
            Settings['Token'] = fetchToken(Settings['Username'], Settings['Password'])
            if not Settings['Token']:
                log("Error getting token, trying without...", True)
            elif test:
                print("Token: " + Settings['Token'])  # print token, do not save in log file
                login = True

    # Process Token keys, ensure we have lowercase usernames and get access token for shared users.
    if isinstance(Settings['Token'], dict):
        for k in Settings['Token'].keys():
            if k.endswith('$'):
                Settings['Token'][k] = getAccessToken(Settings['Token'][k])
                Settings['Token'][k[:-1].lower()] = Settings['Token'][k]    #add shared user without trailing '$'
            if k.endswith('*'):
                Settings['Token'][k[:-1].lower()] = Settings['Token'][k]    #add default user without trailing '*'
            Settings['Token'][k.lower()] = Settings['Token'][k]

    if args.clean_devices:
        log("Cleaning up devices on plex.tv")
        try:
            x = getURLX("https://plex.tv/devices", parseXML=True, token=getToken())
        except:
            if debug_mode:
                log(str(traceback.format_exc()))
            log("Unable to load devices from http://plex.tv!")
            exit()
        if debug_mode:
            print(x.toprettyxml())
        deviceCount = 0
        log("There are %d client devices." % len(x.getElementsByTagName("Device")))
        for device in x.getElementsByTagName("Device"):
            name = device.getAttribute("name")
            if device.getAttribute("token") == getToken():  # Don't delete the current device token
                continue
            if device.getAttribute("name") == "PlexCleaner" or device.getAttribute("product") == "PlexCleaner":
                deviceCount += 1
                id = device.getAttribute("id")
                try:
                    getURLX("https://plex.tv/devices" + "/" + id + ".xml", token=getToken(), method='DELETE',
                            parseXML=False)
                    log("Deleted device: " + device.getAttribute("clientIdentifier"))
                    sleep(0.1)  # sleep for 100ms to rate limit requests to plex.tv
                except:
                    if debug_mode:
                        log(str(traceback.format_exc()))
                    log("Unable to delete device!")
                if deviceCount > 100:
                    log("Device limit reached! Please run again.")
                    break
        log("Exiting now, verify changes on PlexWeb. \n")
        exit()

    if not Settings['Host'].startswith("http"):
        Settings['Host'] = "http://" + Settings['Host']

    server_check = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/")
    if server_check:
        media_container = server_check.getElementsByTagName("MediaContainer")[0]
        if not Settings['DeviceName']:
            Settings['DeviceName'] = media_container.getAttribute("friendlyName")
        if not machine_client_identifier:
            machine_client_identifier = media_container.getAttribute("machineIdentifier")
    else:
        log("[ERROR] Cannot reach server!", error=True)

    if Settings['Shared'] and getToken():
        accessToken = getAccessToken(getToken())
        if accessToken:
            Settings['Token'] = accessToken
            if test:
                log("Access Token: " + Settings['Token'], True)
        else:
            log("[ERROR] Access Token not found or not a shared account", error=True)

    default_settings = {'episodes': Settings['default_episodes'],
                        'minDays': Settings['default_minDays'],
                        'maxDays': Settings['default_maxDays'],
                        'action': Settings['default_action'],
                        'watched': Settings['default_watched'],
                        'progressAsWatched': Settings['default_progressAsWatched'],
                        'location': Settings['default_location'],
                        'onDeck': Settings['default_onDeck'],
                        'rated': Settings['default_rated'],
                        'homeUsers': Settings['default_homeUsers']
                        }

    log("----------------------------------------------------------------------------")
    log("                           Detected Settings")
    log("----------------------------------------------------------------------------")
    log("Host: " + Settings['Host'])
    log("Port: " + Settings['Port'])

    FileCount = 0
    DeleteCount = 0
    DeleteSize = 0
    MoveCount = 0
    MoveSize = 0
    CopyCount = 0
    CopySize = 0
    OnDeckCount = 0
    RatedCount = 0
    FlaggedCount = 0
    FlaggedSize = 0
    KeptCount = 0
    KeptSize = 0
    ActionHistory = []

    doc_sections = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/")

    if (not Settings['SectionList']) and doc_sections:
        for Section in doc_sections.getElementsByTagName("Directory"):
            if Section.getAttribute("key") not in Settings['IgnoreSections'] and Section.getAttribute("title") not in \
                    Settings['IgnoreSections']:
                Settings['SectionList'].append(Section.getAttribute("key"))
    elif doc_sections and Settings['SectionList']:  # Replace section names with the proper id(/key)
        for i in range(0, len(Settings['SectionList'])):
            if isinstance(Settings['SectionList'][i], int):  # Skip checking name of integers (these are keys)
                continue
            for Section in doc_sections.getElementsByTagName("Directory"):
                if Section.getAttribute("title") == str(Settings['SectionList'][i]):
                    Settings['SectionList'][i] = int(Section.getAttribute("key"))

        Settings['SectionList'].sort()
        # log("Section List Mode: Auto")
        log("Operating on sections: " + ','.join(str(x) for x in Settings['SectionList']))
        log("Skipping Sections: " + ','.join(str(x) for x in Settings['IgnoreSections']))

    else:
        log("Section List Mode: User-defined")
        log("Operating on user-defined sections: " + ','.join(str(x) for x in Settings['SectionList']))

    RescannedSections = []

    for Section in Settings['SectionList']:
        Section = str(Section)

        doc = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/" + Section + "/all")
        deck = getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/" + Section + "/onDeck")

        if not doc:
            log("[ERROR] Failed to load Section %s. Skipping..." % Section, error=True)
            continue
        SectionName = doc.getElementsByTagName("MediaContainer")[0].getAttribute("title1")
        log("")
        log("--------- Section " + Section + ": " + SectionName + " -----------------------------------")

        group = doc.getElementsByTagName("MediaContainer")[0].getAttribute("viewGroup")
        changed = 0
        if group == "movie":
            changed = checkMovies(doc, Section)
        elif group == "show":
            for DirectoryNode in doc.getElementsByTagName("Directory"):
                changed += checkShow(DirectoryNode)
        if changed > 0 and Settings['trigger_rescan']:
            log("Triggering rescan...")
            if getURLX(Settings['Host'] + ":" + Settings['Port'] + "/library/sections/" + Section + "/refresh?deep=1",
                       parseXML=False):
                RescannedSections.append(Section)

    log("")
    log("----------------------------------------------------------------------------")
    log("----------------------------------------------------------------------------")
    log("                Summary -- Script Completed")
    log("----------------------------------------------------------------------------")
    log("")
    if test:
        log("** Currently in testing mode. Please review the changes below. **")
        log("   Remove test from the configuration if everything looks okay.")
        log("")
    log("  Config file: " + Config)
    log("  Total File Count      " + str(FileCount) + (
    " (" + convert_size(KeptSize + FlaggedSize) + ")" if show_size and KeptSize + FlaggedSize > 0 else ""))
    log("  Kept Show Files       " + str(KeptCount) + (
    " (" + convert_size(KeptSize) + ")" if show_size and KeptSize > 0 else ""))
    log("  On Deck Files         " + str(OnDeckCount))
    log("  Rated Files           " + str(RatedCount))
    log("  Deleted Files         " + str(DeleteCount) + (
    " (" + convert_size(DeleteSize) + ")" if show_size and DeleteSize > 0 else ""))
    log("  Moved Files           " + str(MoveCount) + (
    " (" + convert_size(MoveSize) + ")" if show_size and MoveSize > 0 else ""))
    log("  Copied Files          " + str(CopyCount) + (
    " (" + convert_size(CopySize) + ")" if show_size and CopySize > 0 else ""))
    log("  Flagged Files         " + str(FlaggedCount) + (
    " (" + convert_size(FlaggedSize) + ")" if show_size and FlaggedSize > 0 else ""))
    log("  Rescanned Sections    " + ', '.join(str(x) for x in RescannedSections))
    if len(ActionHistory) > 0:
        log("")
        log("  Changed Files:")
        for item in ActionHistory:
            log("  " + item)
    if len(ErrorLog) > 0:
        log("")
        log("  Errors:")
        for item in ErrorLog:
            log("  " + item)
    log("")
    log("----------------------------------------------------------------------------")
    log("----------------------------------------------------------------------------")

    # Email Log
    if Settings['EmailLog'] and (len(ActionHistory) > 0 or len(
            ErrorLog) > 0 or email_empty_log):  # Email log, but by default do not email log if no actions performed
        try:
            EmailContents = []  # Text of email.
            EmailContents.append("<pre>")
            EmailContents.append("----------------------------------------------------------------------------")
            EmailContents.append("                Summary -- Script Completed")
            EmailContents.append("----------------------------------------------------------------------------")
            EmailContents.append("\n")
            EmailContents.append("  Config file: " + Config)
            EmailContents.append("  Total File Count      " + str(FileCount) + (
                " (" + convert_size(KeptSize + FlaggedSize) + ")" if show_size and KeptSize + FlaggedSize > 0 else ""))
            EmailContents.append("  Kept Show Files       " + str(KeptCount) + (
                " (" + convert_size(KeptSize) + ")" if show_size and KeptSize > 0 else ""))
            EmailContents.append("  On Deck Files         " + str(OnDeckCount))
            EmailContents.append("  Rated Files           " + str(RatedCount))
            EmailContents.append("  Deleted Files         " + str(DeleteCount) + (
                " (" + convert_size(DeleteSize) + ")" if show_size and DeleteSize > 0 else ""))
            EmailContents.append("  Moved Files           " + str(MoveCount) + (
                " (" + convert_size(MoveSize) + ")" if show_size and MoveSize > 0 else ""))
            EmailContents.append("  Copied Files          " + str(CopyCount) + (
                " (" + convert_size(CopySize) + ")" if show_size and CopySize > 0 else ""))
            EmailContents.append("  Flagged Files         " + str(FlaggedCount) + (
                " (" + convert_size(FlaggedSize) + ")" if show_size and FlaggedSize > 0 else ""))
            EmailContents.append("  Rescanned Sections    " + ', '.join(str(x) for x in RescannedSections))
            if len(ActionHistory) > 0:
                EmailContents.append("\n")
                EmailContents.append("  Changed Files:")
                for item in ActionHistory:
                    EmailContents.append("  " + item.encode('ascii', 'replace').decode('utf-8'))
            if len(ErrorLog) > 0:
                EmailContents.append("\n")
                EmailContents.append(" Errors:")
                for item in ErrorLog:
                    EmailContents.append("  " + item.encode('ascii', 'replace').decode('utf-8'))
            EmailContents.append("\n")
            EmailContents.append("----------------------------------------------------------------------------")
            EmailContents.append("</pre>")
            if sendEmail(Settings["EmailUsername"], Settings["EmailRecipient"], "Plex-Cleaner Log", "\n".join(EmailContents),
                      Settings["EmailServer"], Settings["EmailServerPort"], Settings["EmailUsername"],
                      Settings["EmailPassword"], Settings["EmailServerUseTLS"]):
                log("")
                log("Email of script summary sent successfully.")
        except Exception as e:
            log(e, True)
            log("Could not send email.  Please ensure a valid server, port, username, password, and recipient are specified in your Config file.")
            if debug_mode:
                log(str(traceback.format_exc()))

    log("")
