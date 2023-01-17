from application import db
import pandas as pd
import csv
file_path = r'BOOK.csv'


class Book(db.Model):
    __tablename__ = 'book'
    bid = db.Column(db.Integer, primary_key=True,
                    nullable=False)
    cover = db.Column(db.String(255))
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publisher = db.Column(db.String(255))
    abstract = db.Column(db.String(1000))
    price = db.Column(db.String(255))

    def read_data():
        with open('BOOK.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            list_of_csv = list(csv_reader)

        return list_of_csv
        """ csvFile=open(file_path,encoding='gbk')
        lines=csvFile.readlines()
        print(len(lines))
        nlist=[]

        for i in range(1,len(lines)):
            s=lines[i]
            s=s.replace('\n','')
            n=s.split(',')
            nlist.append(n)
        csvFile.close()
        return nlist
 """

    def add_data():
        nlist = Book.read_data()
        for i in range(nlist.__len__()-1):
            i += 1
            book = Book(bid=int(nlist[i][0]), cover=nlist[i][1], title=nlist[i][2], author=nlist[i][3],
                        publisher=nlist[i][4], abstract=nlist[i][5], price=nlist[i][6])
            db.session.add(book)
            db.session.commit()
