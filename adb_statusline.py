#!/usr/bin/env python3
"""adb_statusline.py is a reasonably simple script that will print a number of
statistics about the connected android phone, via adb. These are customizable.
Further information will be added later..."""

# For parsing arguments
import argparse
# For stderr and exit
import sys
# For exit codes
import errno

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
                    help='Display load average'
                    )

parser.add_argument('-m', '--memory',
                    action='append_const',
                    dest='flags',
                    const='mem',
                    help='Display memory useage, human readable'
                    )

parser.add_argument('-b', '--battery',
                    action='append_const',
                    dest='flags',
                    const='bat',
                    help='Display battery percentage'
                    )

args = parser.parse_args()
print(args)

# The tmux flag can only be used with other flags, or there'd be nothing to
# print!
if args.tmux_needed == True and not args.flags:
    print('-t or --tmux must be used with other flags!!', file=sys.stderr)
    sys.exit(errno.EPERM)
