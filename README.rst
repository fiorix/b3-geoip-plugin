===============
B3 GeoIP Plugin
===============
:Info: See `github <http://github.com/fiorix/b3-geoip-plugin>`_ for the latest source.
:Author: Alexandre Fiori <fiorix@gmail.com>

About
=====

This plugin provides GeoIP information for players, using the `Free IP Geolocation Webservice <http://freegeoip.net>`_.
It will enable the ``!geoip`` (or ``!gl`` alias) command for players with a certain level,
and show automatic GeoIP messages on connection. The format of the GeoIP message
and the message itself is customizable.

See the `sample configuration file <http://github.com/fiorix/b3-geoip-plugin/tree/master/extplugins/conf/geoip.xml>`_ for details.

It has been only tested with `Urban Terror <http://www.urbanterror.info/>`_, but it might work with other games.

Installation
============

Copy the contents of `extplugins <http://github.com/fiorix/b3-geoip-plugin/tree/master/extplugins>`_ to your ``extplugins`` directory,
and add the following line in ``b3.xml``, under the ``<plugins>`` section::

    <plugin name="geoip" config="/path/to/extplugins/conf/geoip.xml"/>


Credits
=======
Thanks to (in no particular order):

- `TV Clan <http://www.tvclan.com.br>`_

  - For supporting development and testing.
