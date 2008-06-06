# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla Corporation Code.
#
# The Initial Developer of the Original Code is
# Mikeal Rogers.
# Portions created by the Initial Developer are Copyright (C) 2008
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#  Mikeal Rogers <mikeal.rogers@gmail.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

# This global settings files is for use with the simplesettings library

import os, sys

def findInPath(fileName, path=os.environ['PATH']):
    dirs = path.split(os.pathsep)
    for dir in dirs:
        if os.path.isfile(os.path.join(dir, fileName)):
            return os.path.join(dir, fileName)
        if os.name == 'nt' or sys.platform == 'cygwin':
            if os.path.isfile(os.path.join(dir, fileName + ".exe")):
                return os.path.join(dir, fileName + ".exe")
    return None

# Mozilla prefs

MOZILLA_DEFAULT_PREFS = {'extensions.update.enabled'    : False,
                         'extensions.update.notifyUser' : False,
                         'browser.shell.checkDefaultBrowser' : False,
                         'browser.tabs.warnOnClose' : False,
                         'browser.warnOnQuit': False,
                         'browser.sessionstore.resume_from_crash': False,
                        } 
                        
MOZILLA_PREFERENCES = {} # For user config file to set additional prefs
MOZILLA_CMD_ARGS = []

MOZILLA_CREATE_NEW_PROFILE = True

if sys.platform == 'darwin':
    NETWORK_INTERFACE_NAME = None
    firefoxApp = os.path.join('Applications', 'Firefox.app')
    firefoxDir = os.path.join(os.path.expanduser('~/'), firefoxApp)

    if not os.path.isdir(firefoxDir):
        firefoxDir = os.path.join('/', firefoxApp)

    MOZILLA_DEFAULT_PROFILE = os.path.join(firefoxDir, 'Contents', 'MacOS', 'defaults', 'profile')
    MOZILLA_BINARY          = os.path.join(firefoxDir, 'Contents', 'MacOS', 'firefox-bin')


elif sys.platform == 'linux2':
    firefoxBin = findInPath('firefox')
    
    if firefoxBin is not None and os.path.isfile(firefoxBin):
        MOZILLA_BINARY = firefoxBin
    
    MOZILLA_DEFAULT_PROFILE = None

    for path in ('/usr/lib/iceweasel/defaults/profile',
                 '/usr/share/firefox/defaults/profile',
                 '/usr/lib/mozilla-firefox/defaults/profile',
                 '/usr/lib/firefox-3.0/defaults/profile'):
        if os.path.isdir(path):
            MOZILLA_DEFAULT_PROFILE = path


elif os.name == 'nt' or sys.platform == 'cygwin':
    firefoxBin = findInPath('firefox')
    
    bin_locations = [os.path.join(os.environ['ProgramFiles'], 'Mozilla Firefox', 'firefox.exe'),
                     os.path.join(os.environ['ProgramFiles'], 'Mozilla Firefox 3 Beta 5', 'firefox.exe'),
                    ]
    
    if firefoxBin is None:
        for loc in bin_locations:
            if os.path.isfile(loc):
                firefoxBin = loc

    if firefoxBin is not None and os.path.isfile(firefoxBin):
        firefoxDir = os.path.dirname(firefoxBin)

        MOZILLA_BINARY          = firefoxBin
        MOZILLA_DEFAULT_PROFILE = os.path.join(firefoxDir, 'defaults', 'profile')
        
        
