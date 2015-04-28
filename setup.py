from distutils.core import setup
import os
from subprocess import call
import py2exe

# data_files = []
# for dirname, dirnames, files in os.walk('resources'):
#     files = [os.path.join(dirname, fn) for fn in files]
#     data_files.append((dirname, files))
#
# setup(
#     options={'py2exe': {
#         'excludes': ['numpy.linalg'],
#         'optimize': 2,
#         'bundle_files': 3,
#         'compressed': False}},
#     windows=[os.path.join('jrpg.py')],
#     data_files=data_files,
#     zipfile=None,
# )

config_data = """;!@Install@!UTF-8!
Title="RPG Tutorial"
RunProgram="jrpg.exe"
;!@InstallEnd@!"""

with open('config.txt', 'w') as fp:
    fp.write(config_data)

args = 'c:\\7za\\7z.exe a app.7z .\dist\*'.split()
call(args, shell=True)

args = 'copy /b c:\\7za\\7zSD.sfx + config.txt + app.7z jrpg.exe'.split()
call(args, shell=True)

os.unlink('config.txt')
os.unlink('app.7z')
