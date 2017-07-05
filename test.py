# import re


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

import platform

print(platform.system())

print(type(platform.system()))

print("*********************************************************")
