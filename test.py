import re

file = open('testground/test_pom.xml', 'r+')
data = file.read()
# <text>(.*)</text>

# print(data)
print("*********************************************************")
data = re.sub('<artifactId>.*?</artifactId>', "<artifactId>payment</artifactId>", data, 1)
data = re.sub('<name>.*?</name>', "<name>payment</name>", data, 1)
data = re.sub('<finalName>.*?</finalName>', "<finalName>payment</finalName>", data, 1)


file.seek(0)
file.truncate()
file.write(data)

file.close()
print("*********************************************************")
