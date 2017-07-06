import re
import os
import codecs
separator = "/"

print("*********************************************************")

#
# file = open('testground/test_pom.xml', 'r+')
# # data = file.read()
# # # <text>(.*)</text>
# #
# # # print(data)
# # data = re.sub('<artifactId>.*?</artifactId>', "<artifactId>payment</artifactId>", data, 1)
# # data = re.sub('<name>.*?</name>', "<name>payment</name>", data, 1)
# # data = re.sub('<finalName>.*?</finalName>', "<finalName>payment</finalName>", data, 1)
# #
# #
# # file.seek(0)
# # file.truncate()
# # file.write(data)
# #
#
# print(file.name)
#
# def get_base_file_name(full_path):
#     arr = re.split(r'/|\\', full_path)
#     return arr[len(arr) - 1]
#
#
# print(get_base_file_name(file.name))
#
# file.close()
#
# import platform
#
# print(platform.system())
#
# print(type(platform.system()))
# string = "origin  http://gitlab.julanling.com/java/huixian-demo.git (fetch)" \
#          "origin  http://gitlab.julanling.com/java/huixian-demo.git (push)"
#
# print(re.search("http.*?\.git", string).group())


string = "abcd"
string_head_upper = string[0].upper() + string[1:]

print(string)

print(string.upper())


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


def d(data, file):
    if re.search("DEMO", data) is not None:
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print(file.name)

        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")

    return data


def n(old_name):
    return old_name


resolve(d, n, './testground/PPG')

print(re.search("DEMO", "dsadDEMO"))

print("*********************************************************")
