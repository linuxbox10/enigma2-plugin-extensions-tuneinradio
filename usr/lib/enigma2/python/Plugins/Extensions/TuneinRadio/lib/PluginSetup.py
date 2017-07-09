# Embedded file name: /usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/lib/PluginSetup.py
from Components.config import config, ConfigIP, ConfigInteger, ConfigDirectory, ConfigSubsection, ConfigSubList, ConfigEnableDisable, ConfigNumber, ConfigText, ConfigSelection, ConfigYesNo, ConfigPassword, getConfigListEntry, configfile
from Components.ConfigList import ConfigListScreen
from Screens.Screen import Screen
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap, NumberActionMap

class TuneinRadioSetup(Screen, ConfigListScreen):
    skin = '<screen\n    name = "TuneinRadioSetup"\n    position = "center,center"\n    size = "920,560"\n    backgroundColor = "#080000"\n    title = "TuneinRadio Settings">\n    <ePixmap\n        position = "79,521"\n        size = "25,25"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/red.png"\n        zPosition = "3"\n        transparent = "1"\n        alphatest = "blend"/>\n    <ePixmap\n        position = "283,521"\n        size = "25,25"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/green.png"\n        zPosition = "3"\n        transparent = "1"\n        alphatest = "blend"/>\n    <eLabel\n        position = "86,523"\n        zPosition = "4"\n        size = "200,24"\n        halign = "center"\n        font = "Regular;25"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"\n        text = "Cancel"/>\n    <eLabel\n        position = "295,523"\n        zPosition = "4"\n        size = "200,24"\n        halign = "center"\n        font = "Regular;25"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"\n        text = "Save"/>\n    <eLabel\n        position = "495,523"\n        zPosition = "4"\n        size = "200,24"\n        halign = "center"\n        font = "Regular;25"\n        transparent = "1"\n        foregroundColor = "#ffffff"\n        backgroundColor = "#41000000"\n        text = " "/>\n    <ePixmap\n        position = "75,514"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "204,37"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n    <ePixmap\n        position = "279,514"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "204,37"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n    <ePixmap\n        position = "484,514"\n        pixmap = "/usr/lib/enigma2/python/Plugins/Extensions/TuneinRadio/skin/images/tab_active.png"\n        size = "204,37"\n        zPosition = "2"\n        backgroundColor = "#ffffff"\n        alphatest = "blend"/>\n    <widget\n        name = "config"\n        position = "20,50"\n        size = "900,350"\n        itemHeight = "35"\n        scrollbarMode = "showOnDemand"\n        transparent = "1"\n        zPosition = "2"/>\n</screen>'

    def __init__(self, session):
        Screen.__init__(self, session)
        self.list = []
        self.list.append(getConfigListEntry(_('Show plugin in main menu(need e2 restart):'), config.TuneinRadio.menuplugin))
        ConfigListScreen.__init__(self, self.list, session)
        self['setupActions'] = ActionMap(['SetupActions', 'ColorActions'], {'green': self.keySave,
         'cancel': self.keyClose,
         'blue': self.resetdefaults}, -2)

    def resetdefaults(self):
        pass

    def keySave(self):
        for x in self['config'].list:
            x[1].save()

        configfile.save()
        self.close(True)

    def restartenigma(self, result):
        if result:
            self.session.open(TryQuitMainloop, 3)
        else:
            self.close(True)

    def keyClose(self):
        for x in self['config'].list:
            x[1].cancel()

        self.close(False)