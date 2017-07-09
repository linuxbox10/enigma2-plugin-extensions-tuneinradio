# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TSmedia/resources/syspath.py
import os
import sys
import sys
from os import listdir as os_listdir
TSmedia_error_file = '/tmp/TSmedia_error'
print 'TSxpath:adding TSmedia directories to system path......'
scripts = '/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/scripts'
if os.path.exists(scripts):
    for name in os_listdir(scripts):
        if 'script.' in name:
            fold = scripts + '/' + name + '/lib'
            sys.path.append(fold)

TSmediaaddons = '/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/addons'
sys.path.append(TSmediaaddons)
TSmediaresources = '/usr/lib/enigma2/python/Plugins/Extensions/TSmedia/resources'
sys.path.append(TSmediaresources)
print 'TSxpath:Finished adding  TSmedia directories to system path......'