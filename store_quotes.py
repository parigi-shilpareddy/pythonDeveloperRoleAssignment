import sqlite3
import json                                      

connection = sqlite3.connect('quotations.db')
cursor = connection.cursor()

with open("/Users\parig\VsCodePython\quotes.json") as f:
    data = json.load(f)

#connection.execute(''' CREATE TABLE Quote
         #(Qid INT PRIMARY KEY     NOT NULL,
          #QuoteName TEXT    NOT NULL,
           # Author TEXT     NOT NULL,
         #Tags  TEXT NOT NULL);
         #''')

#connection.execute(''' CREATE TABLE Authors
 #        (Aid INT PRIMARY KEY     NOT NULL,
  #        AuthorName TEXT    NOT NULL,
   #         Born TEXT     NOT NULL);
    #     ''')

#connection.execute('''CREATE TABLE Tags
 #       (Tid INT PRIMARY KEY     NOT NULL,
  #        Tags TEXT    NOT NULL,
   #       Author TEXT NOT NULL);''')

#multiple_columns = []
#for i in range(len(data['quotes'])):
    #tag=" ".join(str(elem) for elem in data['quotes'][i]['tags'])
    #data_tuple = (i+1,data['quotes'][i]['quote'],data['quotes'][i]['author'],tag)
    #multiple_columns.append(data_tuple)

#sqlite_insert_with_param = """INSERT INTO Quote
   #                       VALUES (?, ?, ?, ?);"""
#cursor.executemany(sqlite_insert_with_param, multiple_columns)
#multiple_authors = []

#for i in range(len(data['authors'])):
#    data_tuple = (i+100,data['authors'][i]['name'],data['authors'][i]['born'])
 #   multiple_authors.append(data_tuple)

#sqlite_insert_with_param_authors = """INSERT INTO Authors
#                          VALUES (?, ?, ?);"""
#cursor.executemany(sqlite_insert_with_param_authors, multiple_authors)
#multiple_tags = []
#for i in range(len(data['quotes'])):
 #   tag = " ".join(str(elem) for elem in data['quotes'][i]['tags'])
 #   data_tuple = (i+200,tag,data['quotes'][i]['author'])
  #  multiple_tags.append(data_tuple)

#sqlite_insert_with_param = """INSERT INTO Tags
 #                      VALUES (?, ?, ?);"""   

#authors = connection.execute("SELECT * from Authors")
#data = connection.execute("SELECT * from Quote")
#tags = connection.execute("SELECT * from Tags")
cursor.execute("SELECT * FROM Quote")
print(len(cursor.fetchall()))

#cursor.executemany(sqlite_insert_with_param, multiple_tags)
cursor.execute("SELECT * FROM Quote WHERE Author = 'Albert Einstein'")
print(len(cursor.fetchall()))

# close our connection
connection.close()
