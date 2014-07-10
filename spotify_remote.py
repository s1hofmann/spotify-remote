#!/usr/bin/env python
# encoding: utf-8

# Simon Hofmann <mail@simon-hofmann.org>
# 2014

from interface import Interface

def main():
    """Main function
    :returns: 0

    """
    app = Interface()
    app.draw_interface()
    app.update_interface()
    app.window_loop()

if __name__ == '__main__':
    main()
