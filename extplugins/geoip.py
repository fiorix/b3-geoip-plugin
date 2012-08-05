#!/usr/bin/env python
# coding: utf-8
# (c) 2010 /dev/null

__version__ = "0.3"
__author__ = "/dev/null"

import urllib
import functools
import unicodedata

import b3.plugin
import b3.events


def normalize(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s)
                    if unicodedata.category(c) != 'Mn'))


class GeoipPlugin(b3.plugin.Plugin):
    _adminPlugin = None
    _messages = {}
    _format = []

    def startup(self):
        self._adminPlugin = self.console.getPlugin("admin")
        if not self._adminPlugin:
            self.error("Could not find admin plugin")
            return False

        # load translatable strings
        try:
            self._messages["result"] = self.config.get("messages", "result")
        except:
            self._messages["result"] = "^2%s connecting from ^2%s"

        try:
            self._messages["invalid"] = self.config.get("messages", "invalid")
        except:
            self._messages["invalid"] = "Invalid client name or ID: ^2%s"

        try:
            self._messages["notfound"] = self.config.get("messages",
                                                         "notfound")
        except:
            self._messages["notfound"] = "^2Could not find GeoIP " \
                                         "information for ^2%s"

        try:
            self._messages["help"] = self.config.get("messages", "help")
        except:
            self._messages["help"] = "use: !geoip client"

        # load settings
        try:
            level = self.config.getint("commands", "geoip")
        except:
            # default level is 20
            level = 20

        try:
            show_on_connect = bool(self.config.getint("settings",
                                                      "show_on_connect"))
        except:
            show_on_connect = False

        try:
            format = self.config.get("settings", "format").split(",")
            for k in format:
                k = k.strip()
                assert k in ("country", "region", "city")
                self._format.append(k)
        except:
            self._format = ["country", "region", "city"]

        if show_on_connect:
            self.registerEvent(b3.events.EVT_CLIENT_AUTH)

        self._adminPlugin.registerCommand(self, "geoip", level,
                                          self.geoip_lookup, "gl")

    def onEvent(self, event):
        if event.type == b3.events.EVT_CLIENT_AUTH:
            self.geoip_lookup(-1, event.data)

    def geoip_lookup(self, data, client, cmd=None):
        self.debug("geoip data=(%s) client=(%s), cmd=(%s)" %
                   (data, client, cmd))
        if data == -1:
            return self.reply(self.console.write, client.ip, client.name)
        elif data:
            input = self._adminPlugin.parseUserCmd(data)
            if input:
                sclient = self._adminPlugin.findClientPrompt(input[0], client)
                say = functools.partial(cmd.sayLoudOrPM, client)
                if sclient:
                    return self.reply(say, sclient.ip, sclient.exactName)
                else:
                    try:
                        say(self._messages["invalid"] % data)
                    except Exception, e:
                        self.error("Could not use translated string "
                                   "``invalid``: %s" % e)

        cmd.sayLoudOrPM(client, self._messages["help"])

    def reply(self, say, ip, nick):
        try:
            location = self.geoip_query(ip)
        except:
            try:
                say(self._messages["notfound"] % nick)
            except Exception, e:
                self.error("Could not use translated string "
                           "``notfound``: %s" % e)
        else:
            try:
                msg = self._messages["result"] % (nick, location)
                say(msg.encode("ascii", "ignore"))
            except Exception, e:
                self.error("Could not use translated string "
                           "``result``: %s" % e)

    def geoip_query(self, ip):
        fd = urllib.urlopen("http://freegeoip.net/csv/" + ip)
        data = fd.read()
        fd.close()

        data = normalize(data.decode("utf-8")).split(",")
        self.debug("querying %s: %s" % (ip, data))
        info = []
        for fmt in self._format:
            if fmt == "country" and data[2]:
                info.append(data[2].strip())
            elif fmt == "region" and data[4]:
                info.append(data[4].strip())
            elif fmt == "city" and data[5]:
                info.append(data[5].strip())

        return ", ".join(info)


if __name__ == "__main__":
    from b3.fake import fakeConsole

    p = GeoipPlugin(fakeConsole, "./conf/geoip.xml")
    p.onStartup()

    while True:
        pass
