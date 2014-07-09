#!/usr/bin/env python
# encoding: utf-8

import dbus

class IPCHandler(object):

    """Handler class for IPC communication with the Spotify application"""

    def __init__(self):
        """Initialize IPC communication with Spotify application """

        try:
            self.bus = dbus.SessionBus()

            self.main_obj = self.bus.get_object('com.spotify.qt', '/')
            self.props_obj = self.bus.get_object('com.spotify.qt',
                                                 '/org/mpris/MediaPlayer2')

            self.main_interface = dbus.Interface(self.main_obj,
                                                 'org.\
                                                  freedesktop.\
                                                  MediaPlayer2')

            self.props_interface = dbus.Interface(self.props_obj,
                                                  'org.\
                                                   mpris.\
                                                   MediaPlayer2.\
                                                   Player')
        except dbus.exceptions.DBusException:
            raise

    def __reconnect(self):
        """Tries to reconnect to DBus interface if connection was lost
        :returns: 1 if reconnect was successfull, 0 if otherwise

        """
        pass

    def __read_property(self, prop):
        """Returns the value of the given proptery

        :prop: Desired property value
        :returns: Value

        """
        pass

    def get_shuffle_mode(self):
        """Check if shuffle mode is enabled or disabled.
        :returns: True if shuffle is enabled, false if not

        """
        pass

    def set_shuffle_mode(self, state):
        """Enable or disable shuffle mode

        :bool state: True = enabled, false = disabled
        :returns: none

        """
        pass

    def get_playback_status(self):
        """Get the current playback status
        :returns: 1 if playing, 0 if paused

        """
        pass

    def get_artist(self):
        """Get artist of current played track
        :returns: string with artist name

        """
        pass

    def get_title(self):
        """Get title of current track
        :returns: string with track title

        """
        pass

    def get_album(self):
        """Get album name of current track
        :returns: string with album title

        """
        pass

    def play_next(self):
        """Skip to the next song if possible
        :returns: none

        """
        pass

    def play_previous(self):
        """Skip to the previous song if possible
        :returns: none

        """
        pass
