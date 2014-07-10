spotify-remote
==============

spotify-remote offers a command-line interface to remote control the Spotify linux application via its D-Bus interface.

I simply wanted to things like previous/next or play/pause without the need to take my hands off the keyboard.
This little helper should integrate well with the i3 scratchpad (that's indeed the way I'm using it) and offers vim like controls.

(No editor flameware intended!)

Controls
========

| Key | Command | Action |
--------------------------
| h | :prev | Play previous song |
| l | :next | Play next song |
| Space | :toggle | Toggle play/pause mode |
| r | | Update view |
|  | :q | Exit the remote control app |
|  | :q! | Exit the remote control app and quit Spotify |

Remarks:
--------

I know there could be more features, but actually the Spotify DBus interface doesn't provide that much features.
Maybe I should consider developing a 'real' commandline client...
