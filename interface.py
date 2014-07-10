#!/usr/bin/env python

"""This module provides the curses interface for the
   Spotify remote control application. """

# encoding: utf-8

# Simon Hofmann <mail@simon-hofmann.org>
# 2014

import curses
import dbus
import sys
from ipc import IPCHandler

class Interface(object):

    """Commandline interface for Spotify remote control application"""

    __bottom_height = 3
    __connector = IPCHandler()
    __win_top = None
    __win_bottom = None

    def __init__(self):
        """Default constructor """

        try:
            self.__scr = curses.initscr()

            #color settings
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

            curses.noecho()
            curses.cbreak()

        except curses.error as err:
            print(err.message)

    def draw_interface(self):
        """Draw the application interface
        :returns: None

        """

        maxy, maxx = self.__scr.getmaxyx()

        self.__win_top = curses.newwin(maxy - self.__bottom_height,
                                       maxx,
                                       0,
                                       0)
        self.__win_top.keypad(True)

        self.__win_bottom = curses.newwin(self.__bottom_height,
                                          maxx,
                                          maxy - self.__bottom_height,
                                          0)
        self.__win_bottom.keypad(True)

        self.__win_top.box()
        self.__win_top.refresh()
        self.__win_bottom.box()
        self.__win_bottom.refresh()

    def update_interface(self):
        """Update the applicatoin interface
        :returns: None

        """

        self.draw_interface()
        maxy, maxx = self.__scr.getmaxyx()

        try:
            artist = self.__connector.get_artist()
            album = self.__connector.get_album()
            track = self.__connector.get_title()

            status = self.__connector.get_playback_status()

            self.__win_top.addstr(int(maxy/2 - 4),
                                  int(maxx/2 - len('Now playing:')/2),
                                  'Now playing:')

            self.__win_top.addstr(int(maxy/2 - 3),
                                  int(maxx/2 - len(track)/2),
                                  track)
            self.__win_top.addstr(int(maxy/2 - 1),
                                  int(maxx/2 - len('from')/2),
                                  'from')
            self.__win_top.addstr(int(maxy/2 - 0),
                                  int(maxx/2 - len(artist)/2),
                                  artist)
            self.__win_top.addstr(int(maxy/2 + 2),
                                  int(maxx/2 - len('on')/2),
                                  'on')
            self.__win_top.addstr(int(maxy/2 + 3),
                                  int(maxx/2 - len(album)/2),
                                  album)

            if status == 'Paused':
                self.__win_top.addstr(int(maxy/2 + 5),
                                      int(maxx/2 - len('Paused')/2),
                                      'Paused',
                                      curses.A_BLINK | curses.COLOR_RED)

        except dbus.exceptions.DBusException as err:
            self.__win_top.addstr(int(maxy/2),
                                  int(maxx/2 - len(err.get_dbus_message())/2),
                                  err.get_dbus_message())

        self.__win_top.refresh()

    def cls(self):
        """Clear the interface and redraw it
        :returns: @todo

        """
        self.__win_bottom.clear()
        self.update_interface()

    def window_loop(self):
        """Event loop
        :returns: @todo

        """

        while True:
            var = self.__win_bottom.getch()

            if var == ord(':'):
                command = []
                offset = 1
                self.__win_bottom.addch(1, offset, ':')
                eingabe = self.__win_bottom.getch()
                command.append(eingabe)
                offset += 1

                while eingabe != 10:
                    self.__win_bottom.addch(1, offset, command[-1])
                    offset += 1
                    eingabe = self.__win_bottom.getch()
                    command.append(eingabe)

                self.__win_bottom.refresh()

                cmd = ''.join(map(chr, command))[:-1]

                if cmd == 'q':
                    sys.exit(0)
                elif cmd == 'q!':
                    self.__connector.quit()
                    sys.exit(0)
                elif cmd == 'next':
                    command.clear()
                    self.__connector.play_next()
                    self.cls()
                elif cmd == 'prev':
                    command.clear()
                    self.__connector.play_previous()
                    self.cls()
                elif cmd == 'toggle':
                    command.clear()
                    self.__connector.play_pause()
                    self.cls()
                else:
                    command.clear()
                    self.cls()
            elif var == ord('r'):
                self.update_interface()
            elif var == ord('h'):
                self.__connector.play_previous()
                self.update_interface()
            elif var == ord('l'):
                self.__connector.play_next()
                self.update_interface()
            elif var == ord(' '):
                self.__connector.play_pause()
                self.update_interface()
