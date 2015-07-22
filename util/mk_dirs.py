#!/usr/bin/python3
"""\
    The program groups files into directories based 
    on a date field that is part of the file name. File names 
    are assumed to have a format of nn-yyyymmddnnnnnnn.ccc 
    where n is any integer, yyyy is the four digit year, 
    mm is a two digit month, dd is a two digit day, and c 
    is any character. The critical part is the -yyyymmdd which 
    is what the program attempts to match. It only matches files 
    meeting that pattern. By default the program puts matching files 
    from the base directory into daily directories.
    It was designed to organize 10's or 100's of video files 
    generated by motion software into something less cluttered.
    The daily directories are created under the base directory
    by default. If the montly option is set then all the daily
    directories will be moved into subdirectories organized by month.
"""

import sys
import re
import os
import datetime 
import logging as l
from path import path
from textwrap import dedent as d
from optparse import OptionParser

# Search pattern for date contained in individual file name
# This filename pattern is generated by motion software and is 
# specified in the motion.conf file
F_NAME_PATTERN = "-(\d\d\d\d)(\d\d)(\d\d)"

# This is the pattern for the daily directories that are auto-created
# <2 digit month>-<2 digit day>-<4 digit year> <3 letter day> <3 letter month>
# e.g. 01-03-2015 (Fri Jan 03)
DAILY_DIR_PATTERN = "(\d\d)-(\d\d)-(\d\d\d\d) \(([A-Z][a-z]{2,2} [A-Z][a-z]{2,2} \d\d)\))"

# This is the pattern for the monthly directories
# <4 digit year>-<2 digit month> (<3 letter month, lower case> <4 digit year>)
# e.g. 2015-01 (Jan 2015)
MONTH_DIR_PATTERN="(\d\d\d\d)-(\d\d) \(([A-Z][a-z]{2,2}) (\d\d\d\d)\)"

# FULLMATCH


def setup_cli():
    """Set up command line options and help text"""
    global __doc__
    prog_usage="""\
            mk_dirs.py [options] base_directory
            """
    parser = OptionParser(description=d(__doc__), usage=d(prog_usage))
    '''
    We don't want this for now. It's the default behavior ***** 
    help_txt = """\
            Group directories by day. Creates directories in the 
            form of mm-dd-yyyy and puts existing files into 
            the proper daily directory. Will create directories if they 
            do not already exist. Will place files in month based 
            sub-directories if they exist, otherwise it will create
            a daily directly under the base directory (see -m option).
            This is the default action.
            """
    parser.add_option('', '--daily', help=d(help_txt), action='store_true', 
            dest='day_action', default=True)
    '''
    help_txt = """\
            Group daily directories by month. Does not impact individual files
            Creates directories in the 
            form of yyyy-mm and puts existing daily sub-directories in 
            the form of dd-mm-yyyy under the proper month. Will 
            create monthly directories if they do not already exist. Does 
            not move individual files.
            """
    parser.add_option('-m', '--monthly', help=d(help_txt), action='store_true', 
            dest='month_action', default=False)
    help_txt = """\
            Log every action on every remote file to std-out. 
            """
    parser.add_option('-v', '--verbose', help=d(help_txt), 
            action='store_true', dest='verbose', default=False)
    help_txt = """\
            Surpress all output.
            """
    parser.add_option('-q', '--quiet', help=d(help_txt), action='store_true', 
            default=False, dest='quiet')
    help_txt = """\
            Debug level messages. Assumes -v and overrides -q.
            """
    parser.add_option('-d', '--debug', help=d(help_txt), action='store_true', 
            dest='debug', default=False)
    help_txt = """\
            Simulate. Do not perform moves, just log what the program would do
            (Implies -v).
            """
    parser.add_option('-s', '--simulate', help=d(help_txt), 
            action='store_true', dest='simulate', default=False)
    return parser

def generate_sub_dir_names(f_name):
    """Generate directory names
    
    Take file name in the format created by motion and generate
    day_dir_name and mon_dir_name
    Example daily dir name: 01-03-2015 (Fri Jan 03)
    """
    # Extract the needed elements from the file name
    fname_m = re.compile(F_NAME_PATTERN)
    match = p.search(f_name)
    if not match:
        l.debug("Did not find match in file name for file {0}".format(
                f_name))
        return None

    # Get the components and generate str (e.g. 01-31-2015)
    day_of_month = match.group(3)
    month_num = match.group(2)
    year = match.group(1)
    date_str = "{0}-{1}-{2}".format(month_num, day_of_month, year)

    # We need the 3 letter month and day of week
    dt = datetime.datetime.strptime(date_str, "%m-%d-%Y")
    month_str = dt.strftime("%b")
    day_str = dt.strftime("%a")
    
    # Now build the daily dir string
    # e.g. 01-03-2015 (Fri Jan 03)
    day_dir_name = "{0} ({2} {3} {4})".format(date_str, day_str, month_str, 
            day_of_month)

    # Now build the monthly dir name
    # e.g. 2015-01 (Jan 2015)
    month_dir_name = "{0}-{1} ({2} {0})".format(year, month_num, month_str)

    l.debug("Names:\n\tfile name: {0}\n\tdaily: {1}\n\tmonthly {2}".
            format(f_name, day_dir_name, mon_dir_name))
    return day_dir_name, mon_dir_name # END generate_sub_dir_names

def get_existing_dir_names():
    """Returns dict of directory names, gotta love path.py"""
    global base_dir
    dir_dict = {}
    src_dir = path(base_dir)
    for f in src_dir.walkdirs():
        dir_dict[f.name] = f
    return dir_dict



def group_by_day():
    global base_dir
    # Filenames look like this "53-20150623160000-snapshot.jpg"
    # So the below captures the year, month and day as groups 1, 2 and 3
    # fname_m = file name match
    fname_m = re.compile(F_NAME_PATTERN)

    src_dir = path(base_dir)
    for f in src_dir.files():
        print("file name {0}".format(f.name))
        m = fname_m.search(f.name)
        if not m:
            continue
        dir_name = "{0}-{1}-{2}".format(m.group(2), m.group(3), m.group(1))
        dir_name = src_dir / dir_name
        print("dir names \n\t{0}".format(dir_name))
        if dir_name.exists():
            print("{0} exists".format(dir_name))
        else:
            dir_name.mkdir()
        new_name = dir_name / f.name
        print("Moving {0} to {1}".format(f, new_name))
        f.rename(new_name)
    return # END group_by_day


# Main logic here
if __name__ == '__main__':

    #Process the command line options
    cli_parser = setup_cli()
    (opt, args) = cli_parser.parse_args()

    # Set up logging
    if opt.debug == True: l.basicConfig(format="%(asctime)s: %(message)s",
                level=l.DEBUG)
    # If simulate is on, then verbose must be set to true
    elif opt.verbose == True or opt.simulate == True:
        l.basicConfig(format="%(message)s", level=l.INFO)
        opt.verbose = True #Does nothing if verbose is already True
    elif opt.quiet == True: l.basicConfig(level=l.NOTSET)
    else: l.basicConfig(format="%(levelname)s: %(message)s")

    # Valdiate that the base directory exists
    if not args or len(args) > 1:
        l.critical("Base directory required")
        cli_parser.print_usage()
        sys.exit(1)
    base_dir = path(args[0])
    if base_dir.exists(): l.debug("base_dir <{0}> exists.".format(base_dir))
    else:
        l.critical("Base directory <{0}> does not exist. Exitting.".
                format(base_dir))
        sys.exit(1)

    # If monthly then do that, otherwise run daily
    if opt.month_action == True:
        pass
