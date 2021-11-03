from urllib.request import urlopen
from time import time

def getStudents(group):
    group_page = urlopen("https://uni-dubna.ru/LK/GetGroup?number=" + group)

    students = list()
    for line in group_page:
        line = line.decode("utf-8")

        if "<span>" in line:
            full_name = line[38:-9]

            # skip one line
            group_page.readline()
            url = group_page.readline().decode("utf-8")[77:-50]
            url = "https://uni-dubna.ru" + url

            students.append([group, full_name, url])

    print("Done group " + group)

    return students

def storeToFile(students, filename):
    fout = open(filename, 'a')
    for student in students:
        group = student[0]
        full_name = student[1]
        url = student[2]

        fout.write(group + "," + full_name + "," + url + "\n")

    fout.close()

filename = "result_students_" + str(int(time())) + ".csv"
fout = open(filename, 'w')
fout.write("group,full_name,url\n")
fout.close()

groups_file = open("groups", 'r')
for group in groups_file:
    group = group[:-1]

    students = getStudents(group)
    storeToFile(students, filename)
groups_file.close()

