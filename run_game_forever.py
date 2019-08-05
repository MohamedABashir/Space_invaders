import subprocess
import sys

'''runs the space_invader infinitely times'''
filename = 'space_invader.py'
try:
    p = subprocess.Popen([sys.executable, filename])
    p.communicate()
except:
    pass