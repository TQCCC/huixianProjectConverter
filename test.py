import re

file = open('testground/test_pom.xml', 'r+')
data = file.read()
# <text>(.*)</text>

# print(data)
print("*********************************************************")
data = re.sub(r'(<artifactId>.*?</artifactId>)', "<artifactId>payment</artifactId>", data, 1)
# data = re.sub(r'<name>.*?</name>', "<name>payment</name>", data, 0)
# data = re.sub(r'<finalNamr>.*?</finalName>', "<name>payment</name>", data, 0)

file.write("\n*****************************************************\n")
file.write(data)
print("*********************************************************")
