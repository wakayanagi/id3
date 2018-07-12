#!/usr/bin/python3

# muta.py -- 180629
# Module utilizing Mutagen for ID3 tag manipulation

import mutagen as mg
from mutagen.easyid3 import EasyID3, EasyID3KeyError
import fsys as fs

def openfile(file, eflag):
  # Try to guess and open music file and return file modify timestamp
  # EasyID3 format: eflag = True
  try:
    aud = mg.File(file, easy=eflag)
  except mg.MutagenError:
    print('No ID3 or file found')
    aud = None
  # Return music object and file timestamp
  return aud, fs.getmtime(file)

def removecomments(file):
  # Open music file and remove comments if they exist
  # Open file and preserve modify timestamp
  aud, ts = openfile(file, False)
  # Iterate through the music file for comment tags and remove
  for tag in list(aud):
    if tag.startswith('TXXX') or tag.startswith('COMM') or ('cmt' in tag) or tag == 'comment':
      aud.pop(tag)
  # Save modified file and restore modify timestamp
  aud.save()
  fs.setmtime(file, ts)
  return True

def tagnames():
  # Return list of all valid EasyID3 tags
  return sorted(list(EasyID3.valid_keys.keys()))

def gettag(file, tag):
  # Open music file and query the target ID3 tag
  aud, ts = openfile(file, True)
  # Return tag details if it exists
  return aud[tag][0] if tag in aud.keys() else None

def settag(file, tag, desc):
  # Open music file, modify/add the tag details, and save
  aud, ts = openfile(file, True)
  try:
    aud[tag] = desc
    # Save modified file and restore modify timestamp
    aud.save()
    fs.setmtime(file, ts)
    return True
  except EasyID3KeyError:
    print('Invalid tag name', tag, 'for', file.rsplit('/', 1)[1])
    return False

def deltag(file, tag):
  # Open music file, delete target tag, and save
  aud, ts = openfile(file, True)
  if tag in aud.keys():
    del aud[tag]
  aud.save()
  fs.setmtime(file, ts)
  return True

def listattr(files, padding, tag):
  # Function to list attributes within music files
  print('\nFilename', '-' * (padding - 9), '|', tag.capitalize())
  for f in files:
    # Display file name and tag details
    fname = fs.usubstr(f.rsplit('/', 1)[1], padding)
    tname = gettag(f, tag)

    # If tag attributes are too long, shorten to width of term screen
    if tname != None:
      tname = fs.usubstr(tname, fs.termwidth() - padding - 4)

    print(fname + (padding - fs.ulen(fname)) * '.', '|', tname)

def condinput(inpt):
  # Interpret input sring to check for scenario exceptions
  if inpt == 'q' or inpt == 'Q':
    # Break out of loop if exit condition is called
    return False
  elif inpt == '':
    # If Enter is pressed with no vale, no change to the tag description
    print('No change to file/tag')
    return False
  else:
    return True

def setbatch(files, tag):
  # Function to set all files to the same tag description
  print('[ENTER] No Change  [Q/q] Exit Tag Edit')

  # List out the different tag names found
  currenttag = [gettag(f, tag) for f in files]
  print(tag.capitalize(), 'names found:')
  [print('> ', ctag) for ctag in set(currenttag)]
  newtag = input('Enter new %s name: ' % tag.capitalize())

  # Check input, if valid, modify tags
  if condinput(newtag):
    for f in (f for f in files if settag(f, tag, newtag)):
      print('%s set for: ' % newtag, f.rsplit('/', 1)[1])
  return True

def itertrack(files):
  # Go through all files one by one to change the track number of each
  print('[ENTER] No Change  [Q/q] Quit Tracknumber Edit')
  for f in files:
    padding = 30
    fname = fs.usubstr(f.rsplit('/', 1)[1], padding)
    print(fname + (padding - fs.ulen(fname)) * '.', '|', gettag(f, 'title'))
    # Get current track number
    ctrack = gettag(f, 'tracknumber')
    if ctrack == None:
      ctrack = '--'
    istr = 'Track [' + ctrack + ']'
    ntrack = input(istr + (12 - len(istr)) * ' ' + ': ')

    # Analyze the tracknumber input
    if ntrack == 'q' or ntrack == 'Q':
      # Break out of loop if exit condition is called
      break;
    elif ntrack == '':
      # If Enter is hit, do not change the tag
      print('No change to file/tag')
    elif fs.isint(ntrack) == False or (fs.isint(ntrack) == True and int(ntrack) <= 0):
      # No change if input is not a number
      print('No change to file/tag.  Input is not a positive integer.')
    elif fs.isint(ntrack):
      # Modify tag since input is an integer
      if settag(f, 'tracknumber', str(int(ntrack))):
        print('Track changed to %s' % int(ntrack))
  return True
       
def itertitle(files):
  # Go through all files one by one to change the title of each file
  print('[ENTER] No Change  [Q/q] Quit Title Edit')
  for f in files:
    padding = 30
    print('Filename:', f.rsplit('/', 1)[1])
    print('Title   :', gettag(f, 'title'))
    ntitle = input('Song Title: ')

    if condinput(ntitle):
      if settag(f, 'title', ntitle):
        print('Title tag changed to: %s' % ntitle)
    else:
      if ntitle == 'q' or ntitle == 'Q':
        break
  return True

