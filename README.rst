==============
adb_statusline
==============
``adb_statusline`` is a python script for displaying various simple information about a connected android phone via ``adb``. This information is colorized and formatted for either shell usage (via ANSI escapes) or ``tmux`` usage.

Features
========
* Show the load average of the connected android device
* Show the RAM usage of the connected android device
* Show the battery percentage of the connected android device
* Each of these can display multiple times, in any order
* Able to output in either ANSI escapes or ``tmux`` style color

Usage
=====
::

    usage: adb_statusline.py [-h] [-t] [-l] [-m] [-b]
    
    A statusline to display android phone info for shell and tmux via adb
    
    optional arguments:
      -h, --help     show this help message and exit
      -t, --tmux     Use tmux-style colors
      -l, --load     Display load average (action)
      -m, --memory   Display memory useage, human readable (action)
      -b, --battery  Display battery percentage (action)

At least one "action" must be selected for the script to actually do anything!

Installation
============
Requirements
------------
* Python >3.5
* ``tmux`` which supports 256color
* ``adb``
* Tested with android 7
* The amazing `colored <https://pypi.python.org/pypi/colored/>`_ module for python!
* TODO: FINISH ME AFTER FINISHING THE SCRIPT


TODO: FINISH ME AFTER FINISHING THE SCRIPT


Why?
====
I felt like it (TODO: elaborate here...)

Inspiration
===========
Other ``tmux`` statusline utilities, including `tmux-top <https://github.com/TomasTomecek/tmux-top>`_ and `tmux-mem-cpu-load <https://github.com/thewtex/tmux-mem-cpu-load>`_.

TODO
====
See TODO.rst

License
=======
GPLv3