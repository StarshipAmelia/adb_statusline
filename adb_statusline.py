#!/usr/bin/env python3
"""
adb_statusline.py is a reasonably simple script that will print various pieces
of information about a connected android phone via adb.

Load average, memory usage, and/or battery percentage can be printed. They will
be formatted either for "standard" usage in a shell, or "tmux" usage in tmux.

Color is mandatory at this point.
"""

# For parsing arguments
import argparse
# For stderr and exit
import sys
# For exit codes
import errno
# For running adb and other commands
import subprocess
# For regexes
import re

# For easier color
from colored import fore, back, style

# Authorship information
__author__ = "Ameliai"
__copyright__ = "2016, Amelia"
__credits__ = ["Amelia"]

__license__ = "GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Amelia"
__email__ = "StarshipAmelia@gmail.com"
__status__ = "Prototype"

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Function Definitions START

def check_adb():
    """
    Checks for the existance of ADB, raises an exception if it's not available.

    This exception should usually be allowed to exit the program.

    If adb is available, makes sure that there's a device plugged in
    """
    try:
        subprocess.run(['which', 'adb'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL).check_returncode()

    except subprocess.CalledProcessError as e:
        print('adb not found!!', file=sys.stderr)
        raise FileNotFoundError from e

    # Grab output for `adb devices`
    device_exist = subprocess.run(['adb', 'devices'],
                                  stdout=subprocess.PIPE).stdout

    if not re.search(r'\bdevice\b', device_exist.decode('utf-8')):
        print('No device detected!!', file=sys.stderr)
        sys.exit(errno.ENXIO)


def colorize(num, maximum, tmux_needed):
    """
    Takes the value of num and uses it to determine what color the num
    should be.

    num             - The number that will be colorized
    maximum         - The 'maximum' value, used to create percentages
                      Make this negative if bigger num == worse
    tmux_needed     - Are tmux-style colors needed?

    The colorized text is returned

    Uses the colored module if tmux_needed is not True
    """

    class Colors:
        """
        Contains data members to store the choice of colors in, as well as
        functions to format according to the various levels
        """
        def __init__(self,
                     satisfied,
                     high_high,
                     high_low,
                     medium_high,
                     medium_low,
                     low_high,
                     low_low,
                     bold,
                     reset):

            self.satisfied = satisfied
            self.high_high = high_high
            self.high_low = high_low
            self.medium_high = medium_high
            self.medium_low = medium_low
            self.low_high = low_high
            self.low_low = low_low
            self.bold = bold
            self.reset = reset

        def format_satisfied(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            satisfied colors
            """
            return (self.satisfied + self.bold + string + self.reset)

        def format_high_high(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            high_high colors
            """
            return (self.high_high + self.bold + string + self.reset)

        def format_high_low(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            high_low colors
            """
            return (self.high_low + self.bold + string + self.reset)

        def format_medium_high(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            medium_high colors
            """
            return (self.medium_high + self.bold + string + self.reset)

        def format_medium_low(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            medium_low colors
            """
            return (self.medium_low + self.bold + string + self.reset)

        def format_low_high(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            low_high colors
            """
            return (self.low_high + self.bold + string + self.reset)

        def format_low_low(self, string):
            """
            returns the formatted string, according to the colors passed in the
            object initialization.

            low_low colors
            """
            return (self.low_low + self.bold + string + self.reset)

    if tmux_needed:
        # Use tmux-style colors
        colors = Colors("#[fg=colour51]",       # Cyan
                        "#[fg=colour46]",       # Bright Green
                        "#[fg=colour28]",       # Dark Green
                        "#[fg=colour226]",      # Yellow
                        "#[fg=colour3]",        # Orange
                        "#[fg=colour1]",        # Dark Red
                        "#[fg=colour196]",      # Bright Red
                        "#[bold]",              # Bold Text
                        "#[none fg=default]")   # Reset text
    else:
        # Use ANSI 256 color
        colors = Colors(fore.CYAN_1,            # Cyan
                        fore.GREEN_1,           # Bright Green
                        fore.GREEN_4,           # Dark Green
                        fore.YELLOW_1,          # Yellow
                        fore.YELLOW,            # Orange
                        fore.RED,               # Dark Red
                        fore.RED_1,             # Bright Red
                        style.BOLD,             # Bold Text
                        style.RESET)            # Reset text

    # Initalize
    return_string = ""

    # Find the percentage
    if maximum < 0:
        # If maximum is negative, a bigger num needs more hazardous colors...
        percent = ((float(num)/maximum) + 1) * 100
    else:
        percent = (float(num)/maximum) * 100

    # Check for the different levels
    if percent >= 100:  # >= just in case we get an absurdly high load average
        # Satisfied
        return_string = colors.format_satisfied(str(num))

    elif percent >= 80:
        # Mostly satisfied
        return_string = colors.format_high_high(str(num))

    elif percent >= 60:
        # Fairly satisfied
        return_string = colors.format_high_low(str(num))

    elif percent >= 45:
        # Begin to worry
        return_string = colors.format_medium_high(str(num))

    elif percent >= 30:
        # Worry
        return_string = colors.format_medium_low(str(num))

    elif percent >= 15:
        # Worry more
        return_string = colors.format_low_high(str(num))

    else:
        # Worry a lot
        return_string = colors.format_low_low(str(num))

    return return_string


def get_load(device):
    """
    Gets the load average of the android device represented by the string
    device (not implemented currently, assumes only 1 device is plugged in)

    Returns the load average in the format 'n.nn n.nn n.nn'
    """
    # Grab the output of `adb shell cat /proc/loadavg` only
    dirty_load = subprocess.run(['adb', 'shell', 'cat /proc/loadavg'],
                                stdout=subprocess.PIPE).stdout

    # Convert dirty_load to a python string and remove the trailing \n
    clean_load = dirty_load.decode('utf-8')[:-1]

    # Get the load averages by themselves
    just_load = re.search('^.*\d\.\d\d', clean_load).group()

    # Put each load into a list
    loads_list = just_load.split(' ')

    # Get number of cpu cores
    num_cores = subprocess.run(['adb', 'shell',
                               'cat /sys/devices/system/cpu/present'],
                               stdout=subprocess.PIPE).stdout

    # Get just the last number
    num_cores = num_cores.decode('utf-8')[-2:-1]

    # Increment the number, it's zero-indexed
    num_cores = int(num_cores) + 1

    # Double num_cores for "medium" usage when 100% taxed
    num_cores = num_cores * 2

    # Initalize
    loads_string = ''

    for load in loads_list:
        # This number gets more hazardous as it goes up, so num_cores should be
        # negative
        loads_string += colorize(load, (num_cores * -1), args.tmux_needed)
        loads_string += ' '

    return loads_string

# Function Definitions END


# Check for ADB first, no point in running more code if it's missing!
check_adb()


short_description = """A statusline to display android phone info for shell and
tmux via adb"""

# Set up parser and arguments
parser = argparse.ArgumentParser(description=short_description)

parser.add_argument('-t', '--tmux',
                    action='store_true',
                    dest='tmux_needed',
                    help='Use tmux-style colors'
                    )

parser.add_argument('-l', '--load',
                    action='append_const',
                    dest='flags',
                    const='load',
                    help='Display load average (action)'
                    )

parser.add_argument('-m', '--memory',
                    action='append_const',
                    dest='flags',
                    const='mem',
                    help='Display memory useage, human readable (action)'
                    )

parser.add_argument('-b', '--battery',
                    action='append_const',
                    dest='flags',
                    const='bat',
                    help='Display battery percentage (action)'
                    )

args = parser.parse_args()
print(args)

# The tmux flag can only be used with other flags, or there'd be nothing to
# print!
if args.tmux_needed and not args.flags:
    parser.error('-t or --tmux must be used with other flags!!')

# Similarly, at least one flag must be used...
if not args.flags:
    parser.error('Please specify an action, see -h')

# Main program loop
for flag in args.flags:
    print(flag)

print(get_load('foo'))
