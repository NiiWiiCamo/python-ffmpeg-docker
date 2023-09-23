import os
import subprocess
import sys
from time import sleep

watchdir = os.environ['WATCHDIR']
outputdir = os.environ['OUTPUTDIR']
extension_in = os.environ['FORMAT_IN']
extension_out = os.environ['FORMAT_OUT']
sleep_duration = int(os.environ['WATCH_SECONDS'])

image_formats = [ "jpg", "jpeg", "png", "tbn", "gif" ]

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


def convert(file, targetformat=extension_out):
  file_name, file_extension = os.path.splitext(file)
  file_output = file_name + "." + targetformat
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


def filehandler():
  # find files with extension
  for file in findFiles(extension_in, watchdir):
    # convert file
    convert(file)
    # remove source file
    os.remove(file)
    
    posterhandler(os.path.dirname(file))

    # move file or parent directory to target dir
    if ( not os.path.dirname(file) == watchdir ):
      subprocess.call(['mv', os.path.dirname(file), outputdir])
    else:
      subprocess.call(['mv', file, outputdir])


def posterhandler(dir):
  for file in findFiles(image_formats, dir):
    file_name, file_extension = os.path.splitext(file)
    new_file = os.path.join(os.path.dirname(file), "poster" + file_extension )
    subprocess.call(['mv', file, new_file])


def main():
  print("Trying to convert", extension_in, "files to", extension_out)
  print("Watching directory", watchdir, "with a", sleep_duration, "second delay between scans")
  while True:
    filehandler()
    print("wating", sleep_duration, "seconds...")
    sleep(sleep_duration)
    

if __name__ == '__main__':
  sys.exit(main())