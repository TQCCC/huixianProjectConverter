import re
import os
import time
import sys
import subprocess
import shutil

print("********************************************")

# command_result = subprocess.getoutput("git remote -v")
#
# print(command_result)
#
# gitaddr = re.search("(http).*?(\.git)", command_result).group(0)
#
# print(gitaddr)
#
# os.chdir("./testdata")
#
# subprocess.getoutput("git clone %s" % (gitaddr))

print(subprocess.getstatusoutput("dirasa"))
# os.chdir("../../")
# print(os.getcwd())
#
# print(sys.path[0])
#
# shutil.copytree("./testdata", "./testdata"+"_1")

print("********************************************")
