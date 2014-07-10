#!/usr/bin/env python

""" This module provides a class for inter process communication
     with the Spotify desktop application. """

# encoding: utf-8

# Simon Hofmann <mail@simon-hofmann.org>
# 2014

import dbus
import time
import sys

class DBusCommunicationException(Exception):

    """Custom exception for reconnecting to DBus interface"""

    def __init__(self):
        """Default constructor """
        Exception.__init__(self)

class IPCHandler(object):

    """Handler class for inter process communication
     with the Spotify desktop application"""

    __bus_name = 'com.spotify.qt'                       #bus name to connect to
    __play_path = '/'                                   #path to player object
    __props_path = '/org/mpris/MediaPlayer2'            #path to property object
    __play_iname = 'org.freedesktop.MediaPlayer2'       #interface name
    __props_iname = 'org.freedesktop.DBus.Properties'   #interface name

    __properties = 'org.mpris.MediaPlayer2.Player'

    def __init__(self):
        """Initialize IPC communication with Spotify application """

        try:
            self.__bus = dbus.SessionBus()

            self.__play_obj = self.__bus.get_object(self.__bus_name,
                                                    self.__play_path)
            self.__props_obj = self.__bus.get_object(self.__bus_name,
                                                     self.__props_path)

            self.__play_interface = dbus.Interface(self.__play_obj,
                                                   self.__play_iname)

            self.__props_interface = dbus.Interface(self.__props_obj,
                                                    self.__props_iname)

        except dbus.exceptions.DBusException:
            self.__reconnect()

    def __reconnect(self):
        """Tries to reconnect to DBus interface if connection was lost
        :returns: 0 if reconnect was successfull

        """
        try:
            trys = 5

            while trys:
                trys -= 1

                try:
                    self.__bus = dbus.SessionBus()

                    self.__play_obj = self.__bus.get_object(self.__bus_name,
                                                            self.__play_path)
                    self.__props_obj = self.__bus.get_object(self.__bus_name,
                                                             self.__props_path)

                    self.__play_interface = dbus.Interface(self.__play_obj,
                                                           self.__play_iname)

                    self.__props_interface = dbus.Interface(self.__props_obj,
                                                            self.__props_iname)

                    if self.__props_interface and self.__play_interface:
                        return 0

                except dbus.exceptions.DBusException as err:
                    print(err.get_dbus_message())
                    time.sleep(5)
                    print('Trying to reconnect to message bus...')

            raise DBusCommunicationException

        except DBusCommunicationException:
            print('ERROR: Broken pipe!')
            sys.exit(-1)

    def __read_property(self, prop):
        """Returns the value of the given proptery

        :prop: String
        :returns: value

        """

        try:
            return self.__props_interface.Get(self.__properties,
                                              '%s' % prop)

        except dbus.exceptions.DBusException as err:
            raise

    def __set_property(self, prop, val):
        """Sets a property to the given value

        :prop: string
        :val: value
        :returns: none

        """
        try:
            self.__props_interface.Set('org.mpris.MediaPlayer2.Player',
                                       '%s' % prop,
                                       '%s' % val)

        except dbus.exceptions.DBusException as err:
            raise

    def get_playback_status(self):
        """Get the current playback status
        :returns: status string

        """
        try:
            return self.__read_property('PlaybackStatus')

        except dbus.exceptions.DBusException as err:
            raise

    def get_artist(self):
        """Get artist of current played track
        :returns: string

        """
        try:
            artist = self.__read_property('Metadata')

            return artist['xesam:artist'][0]
        except dbus.exceptions.DBusException as err:
            raise

    def get_title(self):
        """Get title of current track
        :returns: string

        """
        try:
            title = self.__read_property('Metadata')

            return title['xesam:title']
        except dbus.exceptions.DBusException as err:
            raise

    def get_album(self):
        """Get album name of current track
        :returns: string

        """
        try:
            album = self.__read_property('Metadata')

            return album['xesam:album']
        except dbus.exceptions.DBusException as err:
            raise

    def play_next(self):
        """Skip to the next song if possible
        :returns: none

        """
        try:
            if self.__read_property('CanGoNext'):
                self.__play_interface.Next()
        except dbus.exceptions.DBusException as err:
            raise

    def play_previous(self):
        """Skip to the previous song if possible
        :returns: none

        """
        try:
            if self.__read_property('CanGoPrevious'):
                self.__play_interface.Previous()
        except dbus.exceptions.DBusException as err:
            raise

    def play_pause(self):
        """Toggle between play/pause mode
        :returns: none

        """
        try:
            self.__play_interface.PlayPause()
        except dbus.exceptions.DBusException as err:
            raise
    
    def quit(self):
        """Exit remote control application and quit Spotify
        :returns: None

        """
        try:
            self.__play_interface.Quit()
        except dbus.exceptions.DBusException as err:
            raise

    #TODO: The following methods are not working on my pc.
    #If this is a general problem I might drop them...

    def get_volume(self):
        """Returns current volume value
        :returns: double

        """
        try:
            return self.__read_property('Volume')
        except dbus.exceptions.DBusException as err:
            raise

    def set_volume(self, vol):
        """Set volume to given value

        :vol: double
        :returns: none

        """
        try:
            self.__set_property('Volume', vol)
        except dbus.exceptions.DBusException as err:
            raise

    def get_position(self):
        """Returns the position in current track
        :returns: int

        """
        try:
            return self.__read_property('Position')
        except dbus.exceptions.DBusException as err:
            raise

    def get_shuffle_mode(self):
        """Check if shuffle mode is enabled or disabled.
        :returns: 1 if shuffle is enabled, 0 if not

        """
        try:
            return self.__read_property('Shuffle')
        except dbus.exceptions.DBusException as err:
            raise

    def toggle_shuffle(self):
        """Toggle shuffle mode

        :returns: none

        """
        try:
            if self.__read_property('Shuffle'):
                self.__set_property('Shuffle', False)
            else:
                self.__set_property('Shuffle', True)

        except dbus.exceptions.DBusException as err:
            raise

# For testing purposes only
if __name__ == '__main__':
    test = IPCHandler()
