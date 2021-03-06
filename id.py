#!/usr/bin/python3

# Created 180625 - 180709
# Commandline id3 modification script through Mutagen
# Written for use with OSX High Sierra

import sys, os, textwrap
from pathlib import Path

# Required custom python modules
import muta as mu
import fsys as fs

# Check argument for valid path -----------
# Use current path if no path given as argument
path = str(Path(sys.argv[1])) if len(sys.argv) == 2 else fs.getpath()

# Start off with a clear screen
os.system('cls||clear')

# Determine which file types are present and select one
audioext = ['mp3', 'flac', 'm4a', 'ogg']
extensions = sorted(list(set(audioext) & set(fs.getfext(path))))

# Choose the file type to edit if multiple extensions are found
if len(extensions) > 1:
  print('More than one audio extension found.')
  for index, item in enumerate(extensions, start=1):
    print(index, item)
  ftype = input('Select audio extension: ')
  try:
    if int(ftype) - 1 >= 0:
      ext = extensions[int(ftype) - 1]
    else:
      raise Exception()
  except Exception:
    print('Not a valid entry')
    sys.exit()
elif len(extensions) == 1:
  # Automatically choose filetype if one type found
  ext = extensions[0]
  print(ext, 'found')
else:
  # Exit script if no files are found
  print('No files found')
  sys.exit()


# Clear screen for audio file options
os.system('cls||clear')
print('--', ext, 'files in folder --')

# Get path and parse files for music editing
files = fs.getfpath(path, ext)
mu.listattr(files, 30, 'title')

while True:
  # Print input options
  print('-' * 60,
        '\nTITLE:  (1) View Title   (2) Edit Title      (0/q) Exit'
        '\nALBUM:  (3) View Album   (4) Edit Album'
        '\nARTIST: (5) View Artist  (6) Edit Artist'
        '\nTRACK:  (7) View Track # (8) Edit Track #'
        '\nGENRE:  (9) View Genre   (10) Edit Genre     (14) Delete Comments'
        '\nMISC:   (11) View Tag    (12) Edit Tag       (13) Delete Tag')

  idtags = sorted(['title', 'artist', 'album', 'tracknumber', 'discnumber',
                   'length', 'genre', 'composer', 'date', 'performer',
                   'organization','copyright', 'comment'])

  # Get user selection and ensure input is an integer
  sel = input('Enter Selection: ')
  if not fs.isint(sel):
    print('Not a valid entry')
    #sys.exit()
  else:
    sel = int(sel)

  # Clear screen if not script exit
  if sel != 0 or sel != 'q' or sel != 'Q':
    os.system('cls||clear')

  # Options
  if sel == 1:
    # View Title
    mu.listattr(files, 30, 'title')
  elif sel == 2:
    # Edit Title
    mu.itertitle(files)
  elif sel == 3:
    # View Album
    mu.listattr(files, 20, 'album')
  elif sel == 4:
    # Edit Album
    mu.setbatch(files, 'album')
  elif sel == 5:
    # View Artist
    mu.listattr(files, 50, 'artist')
  elif sel == 6:
    mu.setbatch(files, 'artist')
  elif sel == 7:
    # View Track #
    mu.listattr(files, 60, 'tracknumber')
  elif sel == 8:
    # Edit Track # 
    mu.itertrack(files)
  elif sel == 9:
    # View Genre
    mu.listattr(files, 60, 'genre')
  elif sel == 10:
    # Edit Genre
    mu.setbatch(files, 'genre')
  elif sel == 11 or sel == 12 or sel == 13:
    # Custom/User Select Tag Options
    print('Available Tags:')
    print(textwrap.fill(' '.join(mu.tagnames()), width=75))
    print('\nCommon Tags:')
    print(textwrap.fill(' '.join(idtags), width=75), '\n')
    if sel == 11:
      # View tag by user input
      custom = input('Query tag: ')
      if mu.condinput(custom):
        mu.listattr(files, 50, custom)
    elif sel == 12:
      # Edit tag by user input
      custom = input('Edit tag: ')
      if mu.condinput(custom):
        tag = input('\nEnter tag content: ')
        [print('% s changed for: ' % custom, f.rsplit('/', 1)[1])
               for f in files if mu.settag(f, custom, tag)]
    elif sel == 13:
      # Delete tag by user input
      tag = input('Delete tag: ')
      if mu.condinput(tag):
        [print(tag, 'tag deleted from', f.rsplit('/', 1)[1])
               for f in files if mu.deltag(f, tag)]
  elif sel == 14:
    # Delete Commnets
    mu.listattr(files, 30, 'title')
    cinput = input('Delete comment tag from above files? [y/n]: ')
    if cinput == 'y' or cinput == 'Y':
      for f in (f for f in files if mu.removecomments(f)):
        print('Comments deleted from', f)
    else:
      print('No comment tags deleted.')
  elif sel == 0 or sel == 'q' or sel == 'Q':
    break

sys.exit()
