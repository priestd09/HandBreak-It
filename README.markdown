# "HandBreak It" is an advanced batch script for HandbrakeCLI

The goal behind this is not to replace Handbrake gui but to add a way to quickly and easily do a large batch encode of files based on saved presets. I am currently taking what started as a simple script and am trying to refactor it in to a full program.

The current beta now takes the preset as a flag, and will default to Apple > Universal as its default encoding preset. Use --help or -h to see command line options.

## Currently there is a version 1.0;
* This version is CLI with a option sparse GUI for selecting folders and errors.
* It only uses the AppleTV 2 preset.
* This version is currently only for Mac OS X

## USAGE:
1. Install HandBrakeCLI from http://handbrake.fr/downloads2.php in to your /Applications Directory.
2. Run this script from the command line
3. Enjoy