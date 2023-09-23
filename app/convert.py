import os
import subprocess
import sys

watchdir = os.environ['WATCHDIR']
outputdir = os.environ['OUTPUTDIR']
extension_in = os.environ['FORMAT_IN']
extension_out = os.environ['FORMAT_OUT']

def findFiles(name=extension_in, path=watchdir):
  result = []
  for root, dirs, files in os.walk(path):
    for file in files:
      file_name, file_extension = os.path.splitext(file)
      if name in file_extension:
        result.append(os.path.join(root, file))
  return result

# def convert(file, targetformat=extension_out):
#   file_name, file_extension = os.path.splitext(file)
#   file_output = file_name + "." + targetformat
#   print(file)
#   print(file_output)
#   stream = ffmpeg.input(file)
#   stream = ffmpeg.output("/watch/test.mp3")
#   # stream = ffmpeg.output(file_output)
#   ffmpeg.run(stream)

def convert(file, targetformat=extension_out):
  file_name, file_extension = os.path.splitext(file)
  file_output = file_name + "." + targetformat
  print(file)
  print(file_output)
  subprocess.call([
    'ffmpeg',
    '-i',
    '-vn',
    '-nostdin',
    '-hide_banner',
    '-nostats',
    '-loglevel',
    'panic',
    '-y', 
    file,
    file_output
  ])


def main():
  # find files with extension
  for file in findFiles(extension_in, watchdir):
    convert(file)


if __name__ == '__main__':
  sys.exit(main())