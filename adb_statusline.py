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


# Function Definitions

def check_adb():
    """
    Checks for the existance of ADB, raises an exception if it's not available.

    This exception should usually be allowed to exit the program.
    """
    try:
        subprocess.run(['which', 'adb'],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL).check_returncode()

    except subprocess.CalledProcessError as e:
        print('adb not found!!', file=sys.stderr)
        raise FileNotFoundError from e


def colorize(percent, tmux_needed):
    """
    Takes the value of percent and uses it to determine what color the percent
    should be.

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
        colors = Colors(fore.CYAN_1,
                        fore.GREEN_1,
                        fore.GREEN_4,
                        fore.YELLOW_1,
                        fore.YELLOW,
                        fore.RED,
                        fore.RED_1,
                        style.BOLD,
                        style.RESET)

    # Initalize
    return_string = ""

    # Check for the different levels
    if percent == 100:
        # Satisfied
        return_string = colors.format_satisfied(str(percent))

    elif percent >= 80:
        # Mostly satisfied
        return_string = colors.format_high_high(str(percent))

    elif percent >= 60:
        # Fairly satisfied
        return_string = colors.format_high_low(str(percent))

    elif percent >= 45:
        # Begin to worry
        return_string = colors.format_medium_high(str(percent))

    elif percent >= 30:
        # Worry
        return_string = colors.format_medium_low(str(percent))

    elif percent >= 15:
        # Worry more
        return_string = colors.format_low_high(str(percent))

    else:
        # Worry a lot
        return_string = colors.format_low_low(str(percent))

    return return_string


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

    for num in range(100, 0, -1):
        print(colorize(num, args.tmux_needed))
