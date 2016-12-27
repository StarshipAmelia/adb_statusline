==============
adb_statusline
==============
``adb_statusline`` is a python script for displaying various simple information about a connected android phone via ``adb``. This information is colorized and formatted for either shell usage (via ANSI escapes) or ``tmux`` usage. It can also output colorless text.

Features
========
* Show the load average of the connected android device
* Show the CPU usage percentage of the connected android device
* Show the RAM usage of the connected android device
* Show the battery percentage of the connected android device
* Each of these can display multiple times, in any order
* Able to output in either ANSI escapes, ``tmux`` style color, or no color
* Able to output information about a specified android device, or if none is specified, the first printed by ``adb devices``
* Drains your battery

Usage
=====
::

    usage: adb_statusline [-h] [-s SPECIFIC] [-C [{ANSI,TMUX,NONE}]] [-l] [-m]
                          [-b] [-c]
    
    A statusline to display android phone info for shell and tmux via adb
    
    optional arguments:
      -h, --help            show this help message and exit
      -s SPECIFIC, --specific SPECIFIC
                            Use a specific device, otherwise, use the first
      -C [{ANSI,TMUX,NONE}], --color [{ANSI,TMUX,NONE}]
                            Chose color from ANSI, TMUX, or NONE
      -l, --load            ACTION - Display load average
      -m, --memory          ACTION - Display memory useage, in megabytes
      -b, --battery         ACTION - Display battery percentage
      -c, --cpu             ACTION - Display cpu usage percentage
    
    At least 1 "ACTION" is required!




Example
-------

::

    $ ./adb_statusline.py -s '192.168.1.101:5555' -clmb
    
    21.0% 7.82 7.36 7.22 1807/1857 93%

.. figure:: example.png
    :name: example
    :align: left
    :alt: An example, with color

.. list-table:: *Arguments*
    :widths: 20 20 20
    
    * - ./adb_statusline.py
      - -s '192.168.1.101:5555'
      - -clmb
    * - Script name
      - Device ID to use, optional
      - Actions to take, in that order

.. list-table:: *Output*
    :widths: 20 20 20 20

    * - 21.0%
      - 7.82 7.36 7.22
      - 1807/1857
      - 93%
    * - CPU usage percent
      - Load averages
      - Memory usage
      - Battery percent

Limitations
===========
* Occasionally, the command ``adb shell dumpsys cpuinfo``'s last line reports anomalous CPU usage (in the format ``-x.-y`` where both x and y are numbers). When this happens the CPU usage field will display an 'X'. This seems to be a bug in android, at least in version 7.1.1 on the Nexus 5x.
* By default, ``tmux`` refreshes the status bar every 2 seconds. This script takes around 0.35 seconds to run on a i5 4440 in a VM (2 cores). On a (simulated) busy system, this time can spike to 1.1 seconds! If you are worried about your system not being quick enough, try timing the execution of the script with ``time`` several times to see how long it takes on average.
* Similarly, at least in my testing, having this script running every 2 seconds will cause your battery to discharge faster than it otherwise would.

Installation
============
Requirements
------------
* Python >= 3.5
* ``tmux`` and terminal which supports 256color
* ``adb``
* Tested with android 7.1.1
* The amazing `colored <https://pypi.python.org/pypi/colored/>`_ module for python
* A willingness to charge your phone more frequently
* An Android phone or emulator (emulators not tested)

Instructions
------------
Install colored
+++++++++++++++
First, install colored

.. code:: shell

    $ pip3 install --user colored

Clone Repository
++++++++++++++++
Second, clone the repository

.. code:: shell

    $ git clone https://github.com/StarshipAmelia/adb_statusline

Run the script or place it in your ``.tmux.conf``
+++++++++++++++++++++++++++++++++++++++++++++++++
Third, use the script!

.. code:: shell

    $ python3 adb_statusline/adb_statusline.py --color ANSI -clmb

or

.. code:: shell

    $ cd adb_statusline && ./adb_statusline.py -lbcm

or (in ~/.tmux.conf)

.. code::

    set -g status-right '#(path/to/adb_statusline -C TMUX -clmb)'

The ``#(path/to/adb_statusline -C TMUX -clmb)`` bit should work in either tmux status bar, and with any other contents (provided you've used the paths you've cloned the repo to!). However, if it seems to be "cut off" try increasing ``status-right-length`` . Mine currently looks like ``set -g status-right-length 175`` , which is probably overkill.


Why?
====
I've previously made a version of this script in bash (unreleased), and felt like improving upon its functionality while also learning a more comprehensive language. Also I enjoy seeing colorful numbers in my tmux status bar, and picking up one's phone to check the battery is far too difficult! Hopefully someone else will also find this useful!

Inspiration
===========
Other ``tmux`` status line utilities, including `tmux-top <https://github.com/TomasTomecek/tmux-top>`_ and `tmux-mem-cpu-load <https://github.com/thewtex/tmux-mem-cpu-load>`_.

TODO
====
See `<TODO.rst>`_

License
=======
GPLv3