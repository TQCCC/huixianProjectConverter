# coding:utf-8
import os
import codecs
import sys
import subprocess
import re
import shutil

# TODO 可以删除/忽略无关文件夹，如IDE的配置文件、以及git的.git等等
# TODO 合理处理Maven的pom.xml


tip = "Wrong command\n" \
      "Usage:\n" \
      "     py " + __file__ + " \n\n" \
                              "     src_project_keyword \n\n" \
                              "     target_project_keyword \n\n" \
                              "     project_dir \n\n" \
                              "     [-g|-s]: \n" \
                              "     -g:if it is a git project, clone from remote repository " \
                              "under the same directory of the target. \n" \
                              "     -s:generate a new project under the same directory of the target.\n"

if len(sys.argv) < 4:
    print("missing argument(s)!")
    print(tip)
    sys.exit(0)
elif len(sys.argv) > 5:
    print("too many arguments!")
    print(tip)
    sys.exit(0)

a_1 = sys.argv[1]
a_2 = sys.argv[2]
a_3 = sys.argv[3]
if len(sys.argv) == 5:
    a_4 = sys.argv[4]
    if a_4 != "-s" and a_4 != "-g":
        print(tip)
        sys.exit(0)
else:
    a_4 = "-s"

mode = a_4

# origin = a_1.lower()
# target = a_2.lower()
origin = a_1
target = a_2
# origin_head_upper = origin[0].upper() + origin[1:]
# target_head_upper = target[0].upper() + target[1:]

project_dir = a_3

if os.path.exists("./" + project_dir) is False:
    print("project_dir: %s not found!" % (a_3))
    sys.exit(0)


def custom_replace_one_line_rule(line):
    # re.sub(r'demo', 'payment', line, re.IGNORECASE)
    return line.replace(origin, target)  # .replace(origin_head_upper, target_head_upper)


def replace_content_line_by_line(file_path, rule):
    file = codecs.open(file_path, 'r+', 'utf-8', 'ignore')
    lines = file.readlines()
    file.seek(0)

    for line in lines:
        newline = rule(line)
        file.write(newline)


def custom_file_rename_rule(path):
    # 用反斜杠来分割路径，迎合Windows
    arr = path.split("\\")
    base_file = arr[len(arr) - 1]

    new_name = base_file.replace(origin, target)
    if new_name != base_file:
        os.rename(path, "\\".join(arr[:len(arr) - 1]) + "\\" + new_name)

        # new_name = base_file.replace(origin_head_upper, target_head_upper)
        # if new_name != base_file:
        #     os.rename(path, "\\".join(arr[:len(arr) - 1]) + "\\" + new_name)


def resolve(root_path="."):
    i = 0
    for root, dirs, files in os.walk(root_path, topdown=False):
        print("STEP: %d************RESOLVING DIR: %s************" % (i, root))
        i += 1

        # ignore git
        if root.find("\\.git\\") != -1 or root.find("/.git\\") != -1 or root.endswith("\\.git"):
            print("files in .git should not be modified.")
            continue

        for name in files:

            total_path = root + "\\" + name
            print(total_path)

            # TODO 合理处理Maven的pom.xml
            if name == "pom.xml":
                file = open(total_path, 'r+')
                data = file.read()
                data = re.sub(r'<artifactId>.*?</artifactId>', "<artifactId>" + target + "</artifactId>", data, 1)
                data = re.sub(r'<name>.*?</name>', "<name>" + target + "</name>", data, 1)
                data = re.sub(r'<finalName>.*?</finalName>', "<finalName>" + target + "</finalName>", data, 1)

                file.seek(0)
                file.truncate()
                file.write(data)

                file.close()

                # continue

            # modify file content
            replace_content_line_by_line(total_path, custom_replace_one_line_rule)

            # modify filename
            custom_file_rename_rule(total_path)

        print("++++++dirs below++++++")
        for name in dirs:
            # if not name.startswith(dot):
            total_path = root + "\\" + name
            print(total_path)

            # modify dirname
            custom_file_rename_rule(total_path)


def git_mode():
    print("this project has a git root, clone from the remote repository......")

    os.chdir("./" + project_dir)

    command_result = subprocess.getstatusoutput("git remote -v")
    if command_result[0] == 1:
        print(command_result[1])
        sys.exit(0)
    print(command_result[1])
    gitaddr = re.search("(http).*?(\.git)", command_result[1]).group(0)

    os.chdir("../")

    project_new_name = target
    print(project_new_name)

    command_result = subprocess.getstatusoutput("git clone %s %s" % (gitaddr, project_new_name))
    if command_result[0] == 1:
        print(command_result[1])
        sys.exit(0)

    resolve(project_new_name)


def simple_mode():
    print("Start resolving.......simple mode")

    arr = re.split(r'/|\\', project_dir)  # 适配linux和windows的不同目录分隔符

    # 用户没有输入最后一个分隔符的情况
    if arr[len(arr) - 1] == '':
        project_dir_new = "/".join(arr[:len(arr) - 2]) + "/" + target
    else:
        project_dir_new = "/".join(arr[:len(arr) - 1]) + "/" + target

    shutil.copytree(project_dir, project_dir_new)
    resolve(project_dir_new)


if mode == "-s":
    simple_mode()
elif mode == "-g":
    git_mode()

print("Completed.")
