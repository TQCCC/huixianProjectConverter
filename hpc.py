# coding:utf-8
import os
import codecs
import sys

# import re
# TODO 生成另一份新项目，而不是直接修改原来项目内容，思路：可以巧妙调用git命令
# TODO 可以删除无关文件夹，如IDE、git生成的等等


if len(sys.argv) < 4:
    print("missing argument(s)!")
    print("py " + __file__ + " -src_project_name -target_project_name -project_dir")
    sys.exit(0)

origin = sys.argv[1].lower()
target = sys.argv[2].lower()

origin_head_upper = origin[0].upper() + origin[1:]
target_head_upper = target[0].upper() + target[1:]

project_name = sys.argv[3]

try:
    os.chdir("./" + project_name)
except:
    print("project_dir not found!")
    sys.exit(0)


def custom_rule(line):
    # re.sub(r'demo', 'payment', line, re.IGNORECASE)

    return line.replace(origin, target).replace(origin_head_upper, target_head_upper)


def replace(file_path, rule):
    file = codecs.open(file_path, 'r+', 'utf-8', 'ignore')
    lines = file.readlines()
    file.seek(0)

    for line in lines:
        newline = rule(line)
        file.write(newline)


def rename(path):
    arr = path.split("\\")
    base_file = arr[len(arr) - 1]

    new_name = base_file.replace(origin, target)
    if new_name != base_file:
        os.rename(path, "\\".join(arr[:len(arr) - 1]) + "\\" + new_name)

    new_name = base_file.replace(origin_head_upper, target_head_upper)
    if new_name != base_file:
        os.rename(path, "\\".join(arr[:len(arr) - 1]) + "\\" + new_name)


i = 0
dot = '.'
for root, dirs, files in os.walk(".", topdown=False):
    print("%d************resolving root: %s************" % (i, root))
    i += 1

    # ignore git
    if root.find("\\.git\\") != -1 or root.find("/.git\\") != -1 or root.endswith("\\.git"):
        print("files in .git should not be modified.")
        continue

    for name in files:
        # if not name.startswith(dot):
        totalPath = root + "\\" + name
        print(totalPath)

        # modify file content
        replace(totalPath, custom_rule)

        # modify filename
        rename(totalPath)

    print("++++++dirs below++++++")
    for name in dirs:
        # if not name.startswith(dot):
        totalPath = root + "\\" + name
        print(totalPath)

        # modify dirname
        rename(totalPath)

project_root = os.getcwd()
os.chdir("../")
rename(project_root)

print("Completed.")
