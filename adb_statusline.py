#!/usr/bin/env python3
"""
adb_statusline.py is a reasonably simple script that will print various pieces
of information about a connected android phone via adb.

Load average, cpu percent, memory usage, and/or battery percentage can be
printed. They will be formatted either for "ANSI" usage in a shell,
"TMUX" usage in tmux, or colorless usage via "NONE"
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
from colored import fore, style


__status__ = "Development"
__license__ = "GPLv3"
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


# Class Definitions START

class Colors:
    """
    Contains data members to store the choice of colors in, as well as
    functions to format according to the various levels
    """
    def __init__(self=None,
                 satisfied=None,
                 high_high=None,
                 high_low=None,
                 medium_high=None,
                 medium_low=None,
                 low_high=None,
                 low_low=None,
                 bold=None,
                 reset=None):

        # If any value is not set, set it to an empty string
        if self is None:
            self = ''

        if satisfied is None:
            satisfied = ''

        if high_high is None:
            high_high = ''

        if high_low is None:
            high_low = ''

        if medium_high is None:
            medium_high = ''

        if medium_low is None:
            medium_low = ''

        if low_high is None:
            low_high = ''

        if low_low is None:
            low_low = ''

        if bold is None:
            bold = ''

        if reset is None:
            reset = ''

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

# Class Definitions END


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


def find_first_device():
    """
    Finds the first device listed in adb devices.
    Should only be used if -s is not specified.
    """

    # Get the output of adb devices
    dirty_devices = subprocess.run(['adb', 'devices'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True).stdout

    # Return just the device ID
    return re.sub(r'(^.*?\n|\t.*)', '', dirty_devices, flags=re.S)


def colorize(string, num, maximum, colors):
    """
    Takes the value of num and uses it to determine what color the num
    should be.

    string          - The string (often a number) to colorize
    num             - The number to compare against maximum
    maximum         - The 'maximum' value, used to create percentages
                      Make this negative if bigger num == worse
    colors          - Colors() object containing the colors to use

    The colorized text is returned

    Uses the colored module if tmux_needed is not True
    """

    # Initalize
    return_string = ''

    # Find the percentage
    if maximum < 0:
        # If maximum is negative, a bigger num needs more hazardous colors...
        percent = ((float(num)/float(maximum)) + 1) * 100
    else:
        percent = (float(num)/float(maximum)) * 100

    # Check for the different levels
    if percent >= 100:  # >= just in case we get an absurdly high load average
        # Satisfied
        return_string = colors.format_satisfied(str(string))

    elif percent >= 80:
        # high_high
        return_string = colors.format_high_high(str(string))

    elif percent >= 60:
        # high_low
        return_string = colors.format_high_low(str(string))

    elif percent >= 45:
        # medium_high
        return_string = colors.format_medium_high(str(string))

    elif percent >= 30:
        # medium_low
        return_string = colors.format_medium_low(str(string))

    elif percent >= 15:
        # low_high
        return_string = colors.format_low_high(str(string))

    else:
        # low_low
        return_string = colors.format_low_low(str(string))

    return return_string


def get_load(device, colors):
    """
    Gets the load average of the android device

    device      - The device to get the load average of
    colors      - The Colors() object to use the colors in

    Returns the load average in the format 'n.nn n.nn n.nn'
    """
    # Grab the output of `adb shell cat /proc/loadavg` only
    dirty_load = subprocess.run(['adb',
                                 '-s', device,
                                 'shell',
                                 'cat /proc/loadavg'],
                                stdout=subprocess.PIPE).stdout

    # Convert dirty_load to a python string and remove the trailing \n
    clean_load = dirty_load.decode('utf-8')[:-1]

    # Get the load averages by themselves
    just_load = re.search('^.*\d\.\d\d', clean_load).group()

    # Put each load into a list
    loads_list = just_load.split(' ')

    # Get number of cpu cores
    num_cores = subprocess.run(['adb',
                                '-s',
                                device,
                                'shell',
                                'cat /sys/devices/system/cpu/present'],
                               stdout=subprocess.PIPE).stdout

    # Get just the last number
    num_cores = num_cores.decode('utf-8')[-2:-1]

    # Increment the number, it's zero-indexed
    num_cores = int(num_cores) + 1

    # triple num_cores for a more useful gradient of color vs usage than *2
    num_cores = num_cores * 3

    # Initalize
    loads_string = ''

    for load in loads_list:
        # This number gets more hazardous as it goes up, so num_cores should be
        # negative
        loads_string += colorize(load,
                                 load,
                                 (num_cores * -1),
                                 colors)
        loads_string += ' '

    # Remove the last space while returning
    return loads_string[:-1]


def get_memory(device, colors):
    """
    Gets the memory usage of the android device

    device      - The device to get the memory usage of
    colors      - The Colors() object to use the colors in

    Returns the memory in the format USED/TOTAL, in MB
    """

    # Grab all of the phone's /proc/meminfo
    dirty_meminfo = subprocess.run(['adb',
                                    '-s',
                                    device,
                                    'shell',
                                    'cat /proc/meminfo'],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True).stdout

    # Remove extraneous fields
    cleaner_meminfo = re.sub(r'Buffers:.*', '',
                             dirty_meminfo.replace('\n', ' '))

    # Remove non-numbers
    meminfo_list = re.sub(r'[^\d ]', '', cleaner_meminfo).split()

    # Get memory utilized, [0] is full, [1] is free
    mem_used = int(meminfo_list[0]) - int(meminfo_list[1])

    # /proc/meminfo gives KB, convert to MB
    mem_used = mem_used // 1000
    meminfo_list[0] = int(meminfo_list[0]) // 1000
    # No need to convert meminfo_list[1], it's not used again...

    # Colorize used memory
    return_string = colorize(str(mem_used) + '/' + str(meminfo_list[0]),
                             mem_used,
                             (meminfo_list[0] * -1),
                             colors)
    return return_string


def get_battery(device, colors):
    """
    Gets the battery level of the android device

    device      - The device to get the battery level of
    colors      - The Colors() object to use the colors in

    Returns the battery in the format PERCENT%
    """

    capacity_location = '/sys/class/power_supply/battery/capacity'

    # Get the battery level from /sys/class/power_supply/battery/capacity
    battery_level = subprocess.run(['adb',
                                    '-s',
                                    device,
                                    'shell',
                                    'cat',
                                    capacity_location],
                                   stdout=subprocess.PIPE,
                                   universal_newlines=True).stdout
    # Remove newline
    battery_level = battery_level.replace('\n', '')

    # Return the value
    return colorize(battery_level,
                    battery_level,
                    100,
                    colors) + '%'


def get_cpu_percent(device, colors):
    """
    Gets the CPU usage percent from the last ~30 seconds of the android device

    device      - The device to get the cpu percent of
    colors      - The Colors() object to use the colors in

    Returns the cpu percentage in the format PERCENT%
    """

    # Get the cpu percentage from dumpsys cpuinfo
    dirty_percent = subprocess.run(
        ['adb', '-s', device, 'shell', 'dumpsys cpuinfo'],
        universal_newlines=True,
        stdout=subprocess.PIPE).stdout.split('\n')[-2:-1]

    cpu_percent = re.sub(r'%.*', '', ''.join(dirty_percent))

    # Is the output anomalous?
    try:
        cpu_percent = float(cpu_percent)
    except ValueError:
        # The output is anomalous, return a placeholder
        return 'X'

    return colorize(cpu_percent,
                    float(cpu_percent),
                    (-100),
                    colors) + '%'

# Function Definitions END


# Check for ADB first, no point in running more code if it's missing!
check_adb()


short_description = """A statusline to display android phone info for shell and
tmux via adb"""

# Set up parser and arguments
parser = argparse.ArgumentParser(description=short_description,
                                 epilog='At least 1 "ACTION" is required!')

parser.add_argument('-s', '--specific',
                    action='store',
                    dest='specific',
                    help='Use a specific device, otherwise, use the first'
                    )

parser.add_argument('-C', '--color',
                    action='store',
                    dest='color_choice',
                    default='ANSI',
                    const='ANSI',
                    nargs='?',
                    choices=['ANSI', 'TMUX', 'NONE'],
                    help='Chose color from ANSI, TMUX, or NONE'
                    )

parser.add_argument('-l', '--load',
                    action='append_const',
                    dest='flags',
                    const='load',
                    help='ACTION - Display load average'
                    )

parser.add_argument('-m', '--memory',
                    action='append_const',
                    dest='flags',
                    const='memory',
                    help='ACTION - Display memory useage, in megabytes'
                    )

parser.add_argument('-b', '--battery',
                    action='append_const',
                    dest='flags',
                    const='battery',
                    help='ACTION - Display battery percentage'
                    )

parser.add_argument('-c', '--cpu',
                    action='append_const',
                    dest='flags',
                    const='cpu',
                    help='ACTION - Display cpu usage percentage'
                    )

args = parser.parse_args()

# At least one flag must be used...
if not args.flags:
    parser.error('Please specify an action, see -h')

# Check if a -s has been passed
if not args.specific:
    device = find_first_device()
else:
    device = args.specific

# Make sure that device is a valid device for adb
try:
    subprocess.run(['adb', '-s', device, 'get-state'],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL).check_returncode()
except subprocess.CalledProcessError:
    print(device, 'is an invalid device!', file=sys.stderr)
    sys.exit(errno.ENXIO)

if args.color_choice == 'TMUX':
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
elif args.color_choice == 'ANSI':
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
else:
    colors = Colors()  # No colors!

# Initalize to_print string
to_print = ''

# Initalize strings to store get_*() functions into, for multiple prints
load_string = ''
memory_string = ''
battery_string = ''
cpu_string = ''


# Main program loop
for flag in args.flags:
    # Check for each flag, if it's already been calculated, use that instead of
    # calculating it again.
    if flag == 'load':
        if not load_string:
            load_string = get_load(device, colors)
            to_print += (load_string) + ' '
        else:
            to_print += (load_string) + ' '

    if flag == 'memory':
        if not memory_string:
            memory_string = get_memory(device, colors)
            to_print += (memory_string) + ' '
        else:
            to_print += (memory_string) + ' '

    if flag == 'battery':
        if not battery_string:
            battery_string = get_battery(device, colors)
            to_print += (battery_string) + ' '
        else:
            to_print += (battery_string) + ' '

    if flag == 'cpu':
        if not cpu_string:
            cpu_string = get_cpu_percent(device, colors)
            to_print += (cpu_string) + ' '
        else:
            to_print += (cpu_string) + ' '

# Print, slicing off the trailing space
print(to_print[:-1])
