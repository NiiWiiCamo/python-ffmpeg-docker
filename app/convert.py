import os
import subprocess
import sys
from time import sleep

watchdir = os.environ['WATCHDIR']
outputdir = os.environ['OUTPUTDIR']
extension_in = os.environ['FORMAT_IN']
extension_out = os.environ['FORMAT_OUT']
sleep_duration = int(os.environ['WATCH_SECONDS'])
replace_spaces = os.getenv("REPLACE_SPACES", 'True').lower() in ('true', '1', 't')
remove_specialchars = os.getenv("REMOVE_SPECIALCHARS", 'True').lower() in ('true', '1', 't')

debug = os.getenv("DEBUG", 'True').lower() in ('true', '1', 't')

image_formats = [ "jpg", "jpeg", "png", "tbn", "gif" ]
special_chars = [ '[', ']', '{', '}', '!', '$', '#', '"', "'", ' ' ]

if isinstance(extension_in, str):
  extension_in = [ extension_in ]

def findFiles(patterns: list = extension_in, path: str = watchdir):
  result = []
  for root, dirs, files in os.walk(path):
    for file in files:
      file_name, file_extension = os.path.splitext(file)
      for pattern in patterns:
        if pattern in file_extension:
          result.append(os.path.join(root, file))
  return result


def specialCharHandler(string):
  if debug:
    print("specialCharHandler input:", string)
  if replace_spaces:
    string = string.replace(" ", "_")
  if remove_specialchars:
    for char in special_chars:
      string = string.replace(char, "")
  if debug:
    print("specialCharHandler output:", string)
  return string


def convert(file, targetformat=extension_out):
  if debug:
    print("convert input:", file)
  file_name, file_extension = os.path.splitext(file)
  file_output = file_name + "." + targetformat
  if debug:
    print("convert file_output:", file_output)

  file_output = specialCharHandler(file_output)

  print("converting", file, "to format", targetformat)
  subprocess.call([
    'ffmpeg',
    '-vn',
    '-nostdin',
    '-hide_banner',
    '-nostats',
    '-loglevel',
    'panic',
    '-y',
    '-i',
    file,
    file_output
  ])
  print("success")


def fileMover(file):
  # move file or parent directory to target dir
  if debug:
    print("fileMover input:", file)
  if ( not os.path.dirname(file) == watchdir ):
    target_dir = os.path.join( outputdir , specialCharHandler( os.path.dirname(file) ) )
    if debug:
      print("mv source:", os.path.dirname(file))
      print("mv target:", target_dir)
    subprocess.call(['mv', os.path.dirname(file), target_dir])
  else:
    subprocess.call(['mv', file, outputdir])
    if debug:
      print("mv source:", file)
      print("mv target:", outputdir)

def fileHandler():
  # find files with extension
  for file in findFiles(extension_in, watchdir):
    # convert file
    convert(file)
    # remove source file
    os.remove(file)
    
    posterHandler(os.path.dirname(file))
    fileMover(file)


def posterHandler(dir):
  for file in findFiles(image_formats, dir):
    file_name, file_extension = os.path.splitext(file)
    new_file = os.path.join(os.path.dirname(file), "poster" + file_extension )
    subprocess.call(['mv', file, new_file])


def main():
  print("Trying to convert", extension_in, "files to", extension_out)
  print("Watching directory", watchdir, "with a", sleep_duration, "second delay between scans")
  while True:
    fileHandler()
    print("wating", sleep_duration, "seconds...")
    sleep(sleep_duration)
    

if __name__ == '__main__':
  sys.exit(main())