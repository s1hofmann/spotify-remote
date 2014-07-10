#!/usr/bin/env python
""" This module provides a class for inter process communication
     with the Spotify desktop application. """
# encoding: utf-8

import dbus

class IPCHandler(object):

    """Handler class for inter process communication
     with the Spotify desktop application"""

    def __init__(self):
        """Initialize IPC communication with Spotify application """

        try:
            self.__bus = dbus.SessionBus()

            self.__player_obj = self.__bus.get_object('com.spotify.qt', '/')
            self.__props_obj = self.__bus.get_object('com.spotify.qt',
                                                     '/org/mpris/MediaPlayer2')

            self.__player_interface = dbus.Interface(self.__player_obj,
                                                     'org.freedesktop.MediaPlayer2')

            self.__props_interface = dbus.Interface(self.__props_obj,
                                                    'org.freedesktop.DBus.Properties')

        except dbus.exceptions.DBusException:
            raise

    def __reconnect(self):
        """Tries to reconnect to DBus interface if connection was lost
        :returns: 1 if reconnect was successfull, 0 if otherwise

        """
        #TODO: Implement reconnect method
        pass

    def __read_property(self, prop):
        """Returns the value of the given proptery

        :prop: String
        :returns: value

        """

        try:
            ret_val = self.__props_interface.Get('org.mpris.MediaPlayer2.Player',
                                                 '%s' % prop)
            return ret_val

        except dbus.exceptions.DBusException:
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

        except dbus.exceptions.DBusException:
            raise

    def get_shuffle_mode(self):
        """Check if shuffle mode is enabled or disabled.
        :returns: True if shuffle is enabled, false if not

        """
        return self.__read_property('Shuffle')

    def toggle_shuffle(self):
        """Toggle shuffle mode

        :returns: none

        """
        try:
            if self.__read_property('Shuffle'):
                self.__set_property('Shuffle', False)
            else:
                self.__set_property('Shuffle', True)

        except dbus.exceptions.DBusException:
            raise

    def get_playback_status(self):
        """Get the current playback status
        :returns: 1 if playing, 0 if paused

        """
        try:
            return self.__props_interface.Get('org.mpris.MediaPlayer2.Player',
                                              'PlaybackStatus')

        except dbus.exceptions.DBusException:
            raise

    def get_artist(self):
        """Get artist of current played track
        :returns: string

        """
        try:
            artist = self.__read_property('Metadata')

            return artist['xesam:artist'][0]
        except dbus.exceptions.DBusException:
            raise

    def get_title(self):
        """Get title of current track
        :returns: string

        """
        try:
            title = self.__read_property('Metadata')

            return title['xesam:title']
        except dbus.exceptions.DBusException:
            raise

    def get_album(self):
        """Get album name of current track
        :returns: string

        """
        try:
            album = self.__read_property('Metadata')

            return album['xesam:album']
        except dbus.exceptions.DBusException:
            raise

    def play_next(self):
        """Skip to the next song if possible
        :returns: none

        """
        try:
            if self.__read_property('CanGoNext'):
                self.__player_interface.Next()
        except dbus.exceptions.DBusException:
            raise


    def play_previous(self):
        """Skip to the previous song if possible
        :returns: none

        """
        try:
            if self.__read_property('CanGoPrevious'):
                self.__player_interface.Previous()
        except dbus.exceptions.DBusException:
            raise

    def play_pause(self):
        """Toggle between play/pause mode
        :returns: none

        """
        try:
            self.__player_interface.PlayPause()
        except dbus.exceptions.DBusException:
            raise

    def get_volume(self):
        """Returns current volume value
        :returns: double

        """
        pass

    def set_volume(self, vol):
        """Set volume to given value

        :vol: double
        :returns: none

        """
        pass

    def get_position(self):
        """Returns the position in current track
        :returns: int

        """
        pass

# For testing purposes only
if __name__ == '__main__':
    test = IPCHandler()
    print(test.get_album())
    test.play_pause()
    test.play_next()
