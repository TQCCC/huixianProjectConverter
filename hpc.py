# coding:utf-8
import os
import codecs
import sys
import subprocess
import re
import shutil
import platform

# TODO 可以删除/忽略无关文件夹，如IDE的配置文件、以及git的.git等等


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

origin = a_1
target = a_2

project_dir = a_3

mode = a_4

separator = "/"
if platform.system() == "Windows":
    separator = "\\"
else:
    separator = "/"

if os.path.exists("./" + project_dir) is False:
    print("project_dir: %s not found!" % (a_3))
    sys.exit(0)


def get_base_file_name(path):
    arr = re.split(r'/|\\', path)
    return arr[len(arr) - 1]


def custom_data_rule(data, file):
    """
    在文件内容中，项目关键字可能的情况

    全小写：demo
    全大写：DEMO
    一般，既有大写也有小写：Demo、deMo

    :param data:
    :param file:
    :return: new data you want.
    """

    new_data = data

    # 处理Maven的pom.xml
    if get_base_file_name(file.name) == "pom.xml":
        new_data = re.sub(r'<artifactId>.*?</artifactId>', "<artifactId>" + target + "</artifactId>", new_data, 1)
        new_data = re.sub(r'<name>.*?</name>', "<name>" + target + "</name>", new_data, 1)
        new_data = re.sub(r'<finalName>.*?</finalName>', "<finalName>" + target + "</finalName>", new_data, 1)

    # TODO 考虑周全
    new_data = re.sub(origin, target, new_data)
    new_data = re.sub(origin.upper(), target.upper(), new_data)

    origin_head_upper = origin[0].upper() + origin[1:]
    target_head_upper = target[0].upper() + target[1:]

    new_data = re.sub(origin_head_upper, target_head_upper, new_data)

    return new_data


def custom_rename_rule(old_name):
    """
    :param old_name:
    :return: return a new name you want.
    """
    new_name = old_name.replace(origin, target)
    return new_name


def resolve_file_content(path, rule):
    file = codecs.open(path, 'r+', 'utf-8', 'ignore')
    data = file.read()

    new_data = rule(data, file)

    file.seek(0)
    file.truncate()
    file.write(new_data)
    file.close()


def resolve_file_or_dir_name(path, old_name, rename_rule):
    arr = re.split(r'/|\\', path)

    new_name = rename_rule(old_name)
    if new_name != old_name:
        os.rename(path, separator.join(arr[:len(arr) - 1]) + separator + new_name)


def resolve(data_rule, rename_rule, root_path="."):
    i = 0
    for root, dirs, files in os.walk(root_path, topdown=False):
        print("STEP: %d************RESOLVING DIR: %s************" % (i, root))
        i += 1

        # ignore git 多个或条件是因为考虑到适配windows和linux路径分隔符的不同
        if root.find("\\.git\\") != -1 or root.find("/.git\\") != -1 or root.endswith("\\.git"):
            print("files in .git should not be modified.")
            continue

        for name in files:
            path = root + separator + name
            print(path)

            # modify file content
            resolve_file_content(path, data_rule)

            # modify filename
            resolve_file_or_dir_name(path, name, rename_rule)

        print("++++++dirs below++++++")
        for name in dirs:
            path = root + separator + name
            print(path)

            # modify directory_name
            resolve_file_or_dir_name(path, name, rename_rule)


def git_mode():
    print("this project has a git root, cloning from the remote repository......")

    os.chdir("./" + project_dir)

    command_result = subprocess.getstatusoutput("git remote -v")
    if command_result[0] == 1:
        print(command_result[1])
        print("clone failed or not a git root? You can try simple mode, type -s at the end.")
        sys.exit(0)

    print(command_result[1])
    git_address = re.search("http.*?\.git", command_result[1]).group(0)

    os.chdir("../")

    project_new_name = target
    print(project_new_name)

    command_result = subprocess.getstatusoutput("git clone %s %s" % (git_address, project_new_name))
    if command_result[0] == 1:
        print(command_result[1])
        sys.exit(0)

    resolve(custom_data_rule, custom_rename_rule, project_new_name)


def simple_mode():
    print("Start resolving.......simple mode")

    # 适配linux和windows的不同目录分隔符
    arr = re.split(r'/|\\', project_dir)

    # 用户没有输入最后一个分隔符的情况
    if arr[len(arr) - 1] == '':
        project_dir_new = separator.join(arr[:len(arr) - 2]) + separator + target
    else:
        project_dir_new = separator.join(arr[:len(arr) - 1]) + separator + target

    shutil.copytree(project_dir, project_dir_new)
    resolve(custom_data_rule, custom_rename_rule, project_dir_new)


if mode == "-s":
    simple_mode()
elif mode == "-g":
    git_mode()

print("Completed.")
