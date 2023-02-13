from urllib.request import urlopen
from time import time
import os
import base64


def getStudents(group):
    group_page = urlopen("https://uni-dubna.ru/LK/GetGroup?number=" + group)

    students = list()
    for line in group_page:
        line = line.decode("utf-8")

        if "<span>" in line:
            full_name = line[38:-9]
            print("Parsing " + full_name)

            # skip one line
            group_page.readline()
            url = group_page.readline().decode("utf-8")[77:-50]
            url = "https://uni-dubna.ru" + url

            uid = url[-36:]
            (email, photo) = getEmailAndPhoto(uid)

            students.append([group, full_name, email, url, photo])

    print("Done group " + group)

    return students


def getEmailAndPhoto(uid):
    user_page = urlopen("https://uni-dubna.ru/LK/ProfilePublic?userId=" + uid)
    lines = user_page.readlines()

    imgline = lines[6]
    photo = b""
    if b"img-raised" in imgline:
        photoBase64 = imgline[79:-4]
        photo = base64.b64decode(photoBase64)

    email = lines[33][41:-7].decode("utf-8")

    return (email, photo)


def storeToFile(students, filename):
    fout = open(filename, "a")
    for student in students:
        group = student[0]
        full_name = student[1]
        email = student[2]
        url = student[3]
        photo = student[4]

        fout.write(group + "," + full_name + "," + email + "," + url + "\n")

        uid = url[-36:]

        # use uid in filename because there is some people with 2 profiles
        fphotoout = open(
            "photos_" + filename + "/" + group + "_" + full_name + "_" + uid +
            ".jpeg",
            "wb",
        )
        fphotoout.write(photo)
        fphotoout.close()

    fout.close()


filename = "result_students_" + str(int(time())) + ".csv"
fout = open(filename, "w")
fout.write("group,full_name,email,url\n")
fout.close()

os.makedirs("photos_" + filename, exist_ok=True)

groups_file = open("groups", "r")
for group in groups_file:
    group = group[:-1]

    students = getStudents(group)
    storeToFile(students, filename)
groups_file.close()
