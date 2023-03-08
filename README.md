# md_disc_filler
A simple script to copy enough random MP3 files for an LP4 MD (MD-LP).

LP4 encoding handles lofi stuff really well and [Web MiniDisc Pro](https://web.minidisc.wiki/) takes whatever ffmpeg can handle as input. 
This script takes a directory of MP3 files and randomly selects enough of them to fill a 74 minute MD with LP4 encoding.

The code isn't built to handle all eventualities. 
For example it looks at artists and titles in the ID3 tags to create a list of what's already been included - skipping files that have the same tags. 
If your files don't have tags then then the duplicate checking isn't going to work. 
I'd use something like [EasyTag](https://gitlab.gnome.org/GNOME/easytag) or [Kid3](https://kid3.kde.org/) to batch tag them.

## Randomisation

When using Web MiniDisc Pro I'd drag and drop the tracks into it and select "use track names" (from the ID3 tags). 
In doing so the files will end up in alphabetical order which isn't what I wanted. 
Of course you could use your MD's shuffle setting, if it has one (my old car radio doesn't!), but the way I handle this in the code is by adding a random integer as a prefix to the filenames. 
This means the filenames become fairly random which is good enough here (and as the filenames aren't used for the track names it doesn't impact the automatic tagging that Web MiniDisc Pro does).

## Known Issues

I think there's some rounding issues at play as the total output always seems to be about 1.5% under the desired length. 
I've added a 1.013 multiplier to combat this (under is still better than over) but it annoys me that it's necessary.

Also if you're filling an LP4 disc with lots of short tracks you will run out of characters for titles when using Web MiniDisc Pro.
MD tables of contents (ToCs) weren't designed to handle 100+ track names! 
It'll just mean that once the ToC is full the rest of the tracks won't have titles. 
Even though it's not an issue with this script it's something you'll run into if using it as intended so I figured I'd flag it up.
