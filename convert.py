import os
import ffmpeg
import sys

watchdir = os.environ['WATCHFOLDER']
outputdir = os.environ['OUTPUTFOLDER']
extension_in = os.environ['FORMAT_IN']
extension_out = os.environ['FORMAT_OUT']

def findFiles(name, path):
  result = []
  for root, dirs, files in os.walk(path):
    if name in files:
      result.append(os.path.join(root, name))
  return result

def convert(file: os.path, targetformat: str):
  file_name, file_extension = os.path.splitext(file)
  file_output = file_name + "." + targetformat
  (
    ffmpeg
    .input(file)
    .output(file_output)
  )

def main():
  # find files with extension
  print(findFiles(extension_in, watchdir))




if __name__ == '__main__':
  sys.exit(main())