#!/usr/bin/python3

# fsys.py -- 180709
# Module for interpreting files and directories
# Python 3 and OSX

import os, time, unicodedata

def getpath():
  # Confirm path where script is called
  path = os.path.dirname(os.path.realpath(__file__))
  return path

def getfiles(path, ext):
  # Check path for files with extension ext
  # Return list of files with the extension
  if os.path.exists(path):
    flist = [file for file in os.listdir(path) if file.endswith(ext) and os.path.isfile(os.path.join(path, file))]
    flist.sort()
  else:
    flist = []
  return flist

def getfpath(path, ext):
  # Check path for files with extension ext
  # Returns list of files with the full path extension
  flist = getfiles(path, ext)
  # Add full path to each file
  if len(flist) > 0:
    flist = [path + '/' + file for file in flist]
  else:
    flist = []
  return flist

def getfext(path):
  # Check path for all applicable file extensions
  if os.path.exists(path):
    flist = [file.rsplit('.',1)[-1] for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    return list(set(flist))

def getmtime(file):
  # Pull the modify timestamp of target file
  # Time in seconds since epoch
  return os.stat(file).st_mtime

def setmtime(file, mtime):
  # Set the modify timestamp of target file
  # Time in seconds since epoch
  os.utime(file, (mtime, mtime))
  return True

def termwidth():
  # Get current terminal screen character width
  return os.get_terminal_size()[0]

def charwidth(char):
  # Check if unicode character is full-width or half-width
  # Input is character or first character of input string
  # east_asian_width coding:
  #   A: ambiguous  F: full width H: halfwidth
  #   N: neutral    Na: narrow    W: wide
  clen = 0
  stat = unicodedata.east_asian_width(char[0])
  if stat == 'F' or stat == 'W' or stat == 'A':
    # Ignore Japanese dakuten and handakuten individual characters
    clen = (2 if ord(char[0]) not in range(12441, 12444) else 0)
  elif stat == 'Na' or stat == 'H':
    clen = 1
  return clen
  
def ulen(cstr):
  # Interpret character string regardless of half/full-width characters for Japanese
  # Add up and return all character spacing width
  slen = 0
  for char in cstr:
    slen += charwidth(char)
  return slen

def usubstr(cstr, length):
  # Return the unicode substring contained within a provided string length
  slen = 0
  i = 0 
  while i < len(cstr): 
    cwidth = charwidth(cstr[i])
    if slen + cwidth > length:
      break
    slen += cwidth
    i += 1
  # Return partial string with the truncated length
  return cstr[:i]

def isint(str):
  # Boolean check whether string is an integer or not
  try:
    int(str)
    return True
  except ValueError:
    return False

