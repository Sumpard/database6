from faker import Faker
from application import app, db
import random
import pandas as pd

fake = Faker(["zh_CN"])
Faker.seed(1)


def Users(t):
    id = t+1
    key_list = ["id", "uname", "pwd",
                "name", "phone", "email", "address", "is_vip", "is_valid"]
    uname = fake.name()
    address = fake.address()
    tel = fake.phone_number()
    uid = fake.user_name()
    email = fake.email()
    password = fake.password(length=8, special_chars=False,
                             digits=True, upper_case=True, lower_case=True)
    l = [1, 0]
    Isvip = random.choice(l)
    Isvalid = 1
    info_list = [id, uid,  password, uname,
                 tel, email, address,  Isvip, Isvalid]
    person_info = dict(zip(key_list, info_list))
    return info_list

""" df = pd.DataFrame(columns=["id", "uname", "pwd",
                  "name", "phone", "email", "address", "is_vip", "is_valid"])

for i in range(100):
    person_info = Users(i)
    df1 = pd.DataFrame(person_info, index=[0])
    df = pd.concat([df, df1])

df.to_csv("database.csv", index=None) """
