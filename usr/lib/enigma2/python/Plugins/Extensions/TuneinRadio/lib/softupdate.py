# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/lib/softupdate.py
from os import popen, system, path, listdir, remove
import os
from Components.Label import Label
from Screens.Standby import TryQuitMainloop
from Screens.Screen import Screen
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap, NumberActionMap
from enigma import getDesktop, eConsoleAppContainer
sz_w = getDesktop(0).size().width()
from Screens.MessageBox import MessageBox
gLogFile = None
from .pltools import getversioninfo, gethostname, log as dlog
currversion, enigmaos, currpackage, currbuild = getversioninfo('TuneinRadio')
server_updatesfile = 'http://www.tunisia-dreambox.info/TSplugins/TuneinRadio/TuneinRadio_updates.txt'
server_updatespath = 'http://tunisia-dreambox.info/TSplugins/TuneinRadio'

def dataupdates():
    version = None
    link = None
    updates = None
    builddate = ''
    try:
        import urllib2
        fp = urllib2.urlopen(server_updatesfile)
        count = 0
        lines = fp.readlines()
        link16 = ''
        link20 = ''
        builddate = ''
        for line in lines:
            if line.startswith('software_version'):
                version = line.split('=')[1].strip()
            if line.startswith('software_fixupdate'):
                builddate = line.split('=')[1].strip()
            if line.startswith('software_link2.0'):
                link20 = line.split('=')[1].strip()
            if line.startswith('software_updates'):
                updates = line.split('=')[1].strip()
            link = link20
            if not enigmaos == 'oe2.0':
                link = link.replace('.ipk', '.deb')

        return ('none',
         version,
         link,
         updates,
         builddate)
    except:
        return ('error',
         version,
         link,
         updates,
         builddate)

    return


class updatesscreen(Screen):
    if sz_w == 1280:
        skin = '<screen\n    name = "updatesscreen"\n    position = "center,center"\n    size = "790,570"\n    backgroundColor = "#080000">\n    <ePixmap\n        position = "300,540"\n        size = "25,25"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"\n        zPosition = "3"\n        transparent = "1"\n        alphatest = "blend"/>\n    <widget\n        name = "key_green"\n        position = "280,537"\n        zPosition = "4"\n        size = "200,24"\n        halign = "center"\n        font = "Regular;20"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"/>\n    <ePixmap\n        position = "280,530"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "204,37"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n\n    <ePixmap\n        position = "100,540"\n        size = "25,25"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"\n        zPosition = "3"\n        transparent = "1"\n        alphatest = "blend"/>\n        \n        \n    <widget\n        name = "key_yellow"\n        position = "130,537"\n        zPosition = "4"\n        size = "200,24"\n        halign = "center"\n        font = "Regular;20"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"/>\n    <ePixmap\n        position = "130,530"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "204,37"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n\n\n        \n    <widget\n        name = "info"\n        position = "20,50"\n        zPosition = "2"\n        size = "760,485"\n        font = "Regular;22"\n        foregroundColor = "#ffffff"\n        transparent = "1"\n        halign = "center"\n        valign = "center"/>\n</screen>\n'
    else:
        skin = '<screen\n    name = "updatesscreen"\n    position = "center,center"\n    size = "1165,855"\n    backgroundColor = "#080000">\n\n\n    <widget\n        name = "key_green"\n        position = "580,806"\n        zPosition = "4"\n        size = "390,36"\n        halign = "center"\n        font = "Regular;30"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"/>\n    <ePixmap\n        position = "645,795"\n        pixmap = "/usr/lib/enigma2/python/Plugins//Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "306,56"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n    <ePixmap\n        position = "655,810"\n        size = "38,38"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"\n        zPosition = "3"\n        transparent = "1"\n        alphatest = "blend"/>\n\n\n    <ePixmap\n        position = "300,810"\n        size = "25,25"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/yellow.png"\n        zPosition = "3"\n        transparent = "1"\n        alphatest = "blend"/>\n        \n        \n    <widget\n        name = "key_yellow"\n        position = "280,806"\n        zPosition = "4"\n        size = "200,24"\n        halign = "center"\n        font = "Regular;20"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"/>\n    <ePixmap\n        position = "280,795"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "200,37"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n\n\n\n\n        \n    <widget\n        name = "info"\n        position = "30,75"\n        zPosition = "2"\n        size = "1140,728"\n        font = "Regular;33"\n        foregroundColor = "#ffffff"\n        transparent = "1"\n        halign = "center"\n        valign = "center"/>\n</screen>'

    def __init__(self, session):
        self.session = session
        Screen.__init__(self, session)
        self['key_green'] = Label('Upgrade')
        self['key_yellow'] = Label('Settings')
        self.updatestring = ''
        self.xmlversion = ''
        self.xmlupdates = ''
        self.xmlupdate = False
        self.update = False
        self.removefirst = False
        self.builddate = ''
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'ok': self.close,
         'cancel': self.close,
         'blue': self.installLastupdate,
         'yellow': self.showsetup,
         'green': self.runsoftupdate}, -1)
        info = 'Checking software updates,please wait...'
        self['info'] = Label(info)
        self.onLayoutFinish.append(self.getupgradeinfo)

    def showsetup(self):
        from .PluginSetup import TuneinRadioSetup
        self.session.open(TuneinRadioSetup)

    def installLastupdate(self):
        if self.builddate.strip() == '':
            return
        else:
            self.builddate = self.builddate.replace('.zip', '')
            filename = '/tmp/' + self.builddate + '.zip'
            if True:
                url = server_updatespath + '/' + self.builddate + '.zip'
                cmdlist = []
                cmdlist.append("wget -O '" + filename + "' -c '" + url + "'")
                cmdlist.append('unzip -o ' + filename + ' -d ' + '/')
                cmdlist.append('rm ' + filename)
                from .Console3 import Console3
                self.session.open(Console3, title='Installing last update', cmdlist=cmdlist, finishedCallback=None, closeOnSuccess=False, instr=None, endstr=None)
            return
            return

    def getupgradeinfo(self):
        debug = True
        try:
            new_addons = ''
            error, version, link, updates, builddate = dataupdates()
            self.builddate = builddate
            if error == 'error':
                self['info'].setText('Error in getting updates data,internet or server down,try later')
                return
            currbuild = builddate
            if error == 'error' or updates is None:
                self['info'].setText('Error getting data,check internet or server down')
                self['key_green'].setText(' ')
                self.update = False
                return
            if updates is None:
                self['info'].setText('Sorry unable to get updates info,no internet or server down!')
                self['key_green'].setText(' ')
                self.update = False
                return
            try:
                allupdates = updates.replace(':', '\n')
            except:
                self['info'].setText('Sorry unable to get updates info,no internet or server down!')
                self['key_green'].setText(' ')
                self.update = False
                return

            self.link = link
            print 'version,currversion', version, currversion
            if version.strip() == currversion.strip():
                self['info'].setText('Plugin version: ' + currversion + '\nlast update:' + currbuild + ' Press blue to re-install last update\n\n No new version available\n\npress green button to remove and re-install current version,some addons may need reinstall\n')
                self.update = True
                self.removefirst = True
                self['key_green'].setText('re-install')
                return
            if float(version) > float(currversion):
                updatestr = 'Plugin version: ' + currversion + '\n\nNew update ' + version + ' is available  \n updates:' + allupdates + '\n\npress green button to start updating\n'
                self['key_green'].setText('Upgrade')
                self.update = True
                self['info'].setText(updatestr)
            else:
                self['info'].setText('Plugin version: ' + currversion + '\n\n No new version available\n')
        except:
            self.update = False
            self['info'].setText('unable to check for updates-No internet connection or server down-please check later')

        return

    def runsoftupdate(self):
        if self.update == False:
            return
        target = '/tmp/updates.ipk'
        self.session.openWithCallback(self.close, ConsoleUpdateScreen, self.link)


class ConsoleUpdateScreen(Screen):
    skin_1280 = '    <screen\n        name = "ConsoleUpdateScreen"\n        position = "center,center"\n        size = "790,570"\n        title = "Plugin Update"\n        backgroundColor = "#00060606"\n        flags = "wfNoBorder">\n        <ePixmap\n            position = "15,5"\n            size = "65,65"\n            zPosition = "0"\n            pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/updates.png"\n            alphatest = "on"/>\n        <widget\n            name = "tslog"\n            position = "15,70"\n            size = "730,500"\n            font = "Regular;22"\n            valign = "top"\n            halign = "left"\n            backgroundColor = "#00000000"\n            transparent = "1"\n            zPosition = "1"/>\n    </screen>'
    skin_1920 = '<screen\n    name = "UpdateScreen"\n    position = "center,center"\n    size = "1185,855"\n    title = "Plugin Update"\n    backgroundColor = "#00060606"\n    flags = "wfNoBorder">\n    <ePixmap\n        position = "22,8"\n        size = "98,98"\n        zPosition = "0"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/updates.png"\n        alphatest = "on"/>\n    <widget\n        name = "tslog"\n        position = "22,105"\n        size = "1095,750"\n        font = "Regular;33"\n        valign = "top"\n        halign = "left"\n        backgroundColor = "#00000000"\n        transparent = "1"\n        zPosition = "1"/>\n</screen>\n'
    if sz_w == 1280:
        skin = skin_1280
    else:
        skin = skin_1920

    def __init__(self, session, updateurl):
        self.session = session
        self.updateurl = updateurl
        self['tslog'] = ScrollLabel()
        Screen.__init__(self, session)
        self.finsished = False
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'cancel': self.keyClose}, -2)
        self.onLayoutFinish.append(self.__onLayoutFinished)

    def __onLayoutFinished(self):
        sl = self['tslog']
        sl.instance.setZPosition(1)
        self['tslog'].setText('Starting update, please wait...')
        self.startPluginUpdate()

    def startPluginUpdate(self):
        try:
            downloadurl(str(self.updateurl))
        except:
            pass

        self.container = eConsoleAppContainer()
        if enigmaos == 'oe2.0':
            self.container.appClosed.append(self.finishedPluginUpdate)
            self.container.stdoutAvail.append(self.mplog)
            self.container.execute('opkg remove enigma2-plugin-extensions-tuneinradio ; opkg update ; opkg install --force-overwrite --force-depends ' + '/tmp/tmp.pac')
        else:
            self.container.appClosed_conn = self.container.appClosed.connect(self.finishedPluginUpdate)
            self.container.stdoutAvail_conn = self.container.stdoutAvail.connect(self.mplog)
            self.container.execute('dpkg -r enigma2-plugin-extensions-tuneinradio ;  dpkg -i --force-depends --force-overwrite /tmp/tmp.pac; apt-get -f -y install')

    def finishedPluginUpdate(self, retval):
        self.finished = True
        try:
            self.container.kill()
        except:
            pass

        if retval == 0:
            self.session.openWithCallback(self.restartGUI, MessageBox, _('Plugin successfully updated!\nDo you want to restart the Enigma2 GUI now?'), MessageBox.TYPE_YESNO)
        elif retval == 2:
            self.session.openWithCallback(self.returnGUI, MessageBox, _('Plugin update failed! Please check free space on your root filesystem, at least 6MB are required for installation.\nCheck the update log at tmp/TSmeida!\ntry to install from tools/files/official software'), MessageBox.TYPE_ERROR)
        else:
            self.session.openWithCallback(self.returnGUI, MessageBox, _('Plugin update failed! Check tmp/plugin_update_log !'), MessageBox.TYPE_ERROR)

    def restartGUI(self, answer):
        self.finished = True
        if answer is True:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close()

    def keyClose(self):
        self.close()

    def restartGUI2(self, answer):
        self.session.open(TryQuitMainloop, 3)

    def returnGUI(self, answer):
        pass

    def mplog(self, str):
        print 'st', str
        self['tslog'].setText(str)
        self.writeToLog(str)

    def writeToLog(self, log):
        global gLogFile
        if gLogFile is None:
            self.openLogFile()
        gLogFile.write(str(log) + '\n')
        gLogFile.flush()
        return

    def openLogFile(self):
        global gLogFile
        try:
            os.remove('/tmp/tmp.pac')
        except:
            pass

        baseDir = '/tmp'
        logDir = baseDir + '/'
        import datetime
        try:
            now = datetime.datetime.now()
        except:
            pass

        try:
            os.makedirs(baseDir)
        except OSError as e:
            pass

        try:
            os.makedirs(logDir)
        except OSError as e:
            pass

        try:
            gLogFile = open(logDir + '/plugin_update_%04d%02d%02d_%02d%02d.log' % (now.year,
             now.month,
             now.day,
             now.hour,
             now.minute), 'w')
        except:
            gLogFile = open(logDir + '/plugin_update', 'w')


def downloadurl(url):
    localf = '/tmp/tmp.pac'
    import urllib
    a, b = urllib.urlretrieve(url, localf)