import random
from datetime import datetime
from hashlib import sha512
from base64 import b64encode
import os



def fetchDate():
    creationDate = str(datetime.now())
    creationDate = creationDate[0:10]
    return creationDate

def generateEmailAlias():
    colorWord = ['red', 'blue', 'green', 'orange', 'black', 'brown', 'white', 'pink', 'purple']
    animalWord = ['lion', 'tiger', 'bear', 'fox', 'zebra', 'giraffe', 'elephant', 'mouse', 'dog', 'cat']
    numbers = [0,1,2,3,4,5,6,7,8,9]

    emailAlias = random.choice(colorWord) + random.choice(animalWord) + str(random.choice(numbers)) + str(random.choice(numbers))
    return emailAlias


def hashDate():
    hashDate = str(datetime.now())
    year = hashDate[:4]
    month = hashDate[5:7]
    day = hashDate[8:10]
    hour = hashDate[11:13]
    minute = hashDate[14:16]
    second = hashDate[17:19]
    hashedDateString = year + '.' + month + '.' + day + '.' + hour + '.' + minute + '.' + second
    return hashedDateString


def hashPassword(password):
    password = bytes(password.encode('utf-8'))
    salt = os.urandom(8)
    pw = sha512(password)
    pw.update(salt)
    return b64encode(pw.digest() + salt)