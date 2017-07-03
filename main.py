# coding:utf-8
import os
import codecs

baseDir = "./testdata"


# filename = "test.txt"
# totalPath = baseDir + filename


def myrule(line):
    return line.replace("demo", "payment").replace("Demo", "Payment")


def replace(filepath, rule):
    file = codecs.open(filepath, 'r+', 'utf-8', 'ignore')
    lines = file.readlines()
    file.seek(0)

    for line in lines:
        newline = rule(line)
        file.write(newline)


i = 0
dot = '.'
for root, dirs, files in os.walk(baseDir + "", topdown=False):
    print("*********************************************************: %d, %s" % (i, root))
    i += 1

    if root.find("\\.git\\") != -1 or root.endswith("\\.git"):
        print("files in .git should not be modified.")
        continue

    for name in files:
        # if not name.startswith(dot):
        totalPath = root + "\\" + name
        print(totalPath)

        # modify file content

        replace(totalPath, myrule)

        # TODO: modify filename

    print("++++++++")
    for name in dirs:
        # if not name.startswith(dot):
        totalPath = root + "\\" + name
        print(totalPath)

        # modify dirname
        oldname = name
        newname = oldname.replace("demo", "payment")
        if newname != oldname:
            os.rename(totalPath, root + "\\" + name)
