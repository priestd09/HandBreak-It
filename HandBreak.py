#!/usr/bin/env python
# encoding: utf-8
"""
Hand Break It
This program is a wrapper to the HandBrakeCLI Application. It is designed to
help batch encode chunks of videos without having to constantly use custom one
line bash scripts. It uses presets only to simplify the process.
It also can be used as a "slightly easier to use" quick front end to processing
a batch of video files as if run without any flags it will prompt for
directories with gui windows.

Created by David "BunnyMan" on 2011-08-13.
Copyright (c) 2011 White Rabbit Code. All rights reserved.
"""

import sys
import os
import re
from subprocess import call, check_output
import argparse
import traceback


class HandbrakeError(Exception):
    """
    The exception used for handbrake blowing up.
    """
    pass


def parse_arguments():
    """This sets up all the arguments the program takes and then returns the
    results of parse_args() so none of it needs to be done in main
    """
    parser = argparse.ArgumentParser(description="Batch encode a directory of\
        video files using handbrake presets")
    parser.add_argument('--in-directory', '-i',
        help="Input directory. You need both -in & -out to run headless")
    parser.add_argument('--out-directory', '-o',
        help="Output directory. You need both -in & -out to run headless")
    parser.add_argument('--recursive', '-r', action='store_false',
        default=True, help="DISABLE recursive scanning of input directory")
    parser.add_argument('--preset', '-p', default='Universal',
        help="Handbrake preset to use, defaults to Apple Universal")
    parser.add_argument('--list-presets', '-l', action='store_true',
        help="List available presets and quit")
    return parser.parse_args()


def get_presets():
    """This runs the HandBrakeCLI command and parses output.
    It returns an array of the valid preset names."""
    handbrakeApp = '/Applications/HandBrakeCLI'
    output = check_output([handbrakeApp, '--preset-list'])
    pattern = re.compile('\+ ([\w\s]+):')
    presetList = re.findall(pattern, output)
    return tuple(presetList)


def get_recursive_files(directory):
    """This isn't too special really,
    just a copy/paste function for crawling a path and getting all the files
    Feed it a directory and it uses os.walk to return array of files
    """
    fileArray = []
    for (directory, subdirectories, files) in os.walk(directory):
        for filename in files:
            fileArray.append(os.path.join(directory, filename))
    return fileArray


def encode_file(inFile, outDirectory, preset="Universal"):
    """
    Pass this a video file, output directory and optionally a handbrake preset
    Nothing is returned
    """
    handbrakeCLI = '/Applications/HandBrakeCLI'
    if not os.path.isfile(handbrakeCLI):
        raise HandbrakeError(
            'HandbrakeCLI not installed in Applications! Please install.')
    outFile = os.path.basename(inFile)[:-4] + '.m4v'
    outFile = os.path.join(outDirectory, outFile)
    call([handbrakeCLI, '-Z', preset, '-i', inFile, '-o', outFile])


def cli_main(args):
    """ This is the cli version, it's designed to run completely "headless".
    """
    inDirectory, outDirectory = args.in_directory, args.out_directory
    if not os.path.isdir(outDirectory):
        os.makedirs(outDirectory)

    if args.recursive:
        videos = get_recursive_files(inDirectory)
    else:
        videos = [os.path.join(inDirectory, videoFile) for
                   videoFile in os.listdir(inDirectory)]

    try:
        for episode in videos:
            encode_file(episode, outDirectory, args.preset)
    except OSError, e:
        print "I had a directory access error: {}".format(e)
        return 1
    except HandbrakeError, e:
        print "HandBrake had an error: {}".format(e)
        return 1
    except Exception:
        print "I had an error:\n {}".format(traceback.format_exc())
        return 1

    print "I, PhotoFinish, am done.\nCheck the Log for details"
    return 0


def gui_main(args):
    """This is the gui version, it will prompt for what information it needs
    and also uses pop ups to display errors"""
    import Tkinter
    import tkMessageBox
    import tkFileDialog
    root = Tkinter.Tk()
    root.withdraw()
    inDirectory = tkFileDialog.askdirectory(title="Pick Video Directory",
        mustexist=True)
    outDirectory = tkFileDialog.askdirectory(title="Pick Output Directory",
        mustexist=False)
    if not inDirectory or not outDirectory:
        tkMessageBox.showerror(
            "Hand Break It",
            "You have to select both in and out directories")
        return 1
    if not os.path.isdir(outDirectory):
        os.makedirs(outDirectory)

    if args.recursive:
        videos = get_recursive_files(inDirectory)
    else:
        videos = [os.path.join(inDirectory, videoFile) for
                   videoFile in os.listdir(inDirectory)]

    try:
        for episode in videos:
            encode_file(episode, outDirectory, args.preset)
    except OSError, e:
        tkMessageBox.showerror(
            "Hand Break It",
            "I had a directory access error: {}".format(e))
        return 1
    except HandbrakeError, e:
        tkMessageBox.showerror(
            "Hand Break It",
            "HandBrake had an error: {}".format(e))
        return 1
    except Exception:
        tkMessageBox.showerror(
            "Hand Break It error",
            "I had an error:\n {}".format(traceback.format_exc()))
        return 1
    tkMessageBox.showinfo("Done",
        "I am done!\nCheck the Log for details")
    return 0


if __name__ == '__main__':
    args = parse_arguments()
    presetTuple = get_presets()
    if args.list_presets:
        print "Available presets; {}.".format(", ".join(presetTuple))
        print "Please check HandBrake for more information."
        sys.exit(0)
    if not args.preset in presetTuple:
        print "\"{}\" is not in the valid preset list".format(args.preset)
        print "Available presets; {}.".format(", ".join(presetTuple))
        print "Please check HandBrake for more information."
        sys.exit("9")
    if args.in_directory and args.out_directory:
        sys.exit(cli_main(args))
    else:
        sys.exit(gui_main(args))