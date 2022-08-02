import sqlite3
import json                                      

connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

with open("/Users\parig\VsCodePython\quotes.json") as f:
    data = json.load(f)

connection.execute(''' CREATE TABLE Quote
         (Qid INT PRIMARY KEY     NOT NULL,
          QuoteName TEXT    NOT NULL,
            Author TEXT     NOT NULL,
         Tags  TEXT NOT NULL);
         ''')

connection.execute(''' CREATE TABLE Authors
       (Aid INT PRIMARY KEY     NOT NULL,
         AuthorName TEXT    NOT NULL,
           Born TEXT     NOT NULL);
        ''')

connection.execute('''CREATE TABLE Tags
        (Tid INT PRIMARY KEY     NOT NULL,
          Tags TEXT    NOT NULL,
          Author TEXT NOT NULL,
          TagCount INT);''')

multiple_quotes = []
for i in range(len(data['quotes'])):
    tag=" ".join(str(elem) for elem in data['quotes'][i]['tags'])
    data_tuple = (i+1,data['quotes'][i]['quote'],data['quotes'][i]['author'],tag)
    multiple_quotes.append(data_tuple)

sqlite_insert_with_param = """INSERT INTO Quote
                          VALUES (?, ?, ?, ?);"""
cursor.executemany(sqlite_insert_with_param, multiple_quotes)

multiple_authors = []
for i in range(len(data['authors'])):
    data_tuple = (i+100,data['authors'][i]['name'],data['authors'][i]['born'])
    multiple_authors.append(data_tuple)

sqlite_insert_with_param_authors = """INSERT INTO Authors
                          VALUES (?, ?, ?);"""
cursor.executemany(sqlite_insert_with_param_authors, multiple_authors)

multiple_tags = []
for i in range(len(data['quotes'])):
    tagCount = len(data['quotes'][i]['tags'])
    tag = " ".join(str(elem) for elem in data['quotes'][i]['tags'])
    data_tuple = (i+200,tag,data['quotes'][i]['author'],tagCount)
    multiple_tags.append(data_tuple)

sqlite_insert_with_param = """INSERT INTO Tags
                       VALUES (?, ?, ?,?);"""  
cursor.executemany(sqlite_insert_with_param, multiple_tags)

authors = connection.execute("SELECT * from Authors")
quotes = connection.execute("SELECT * from Quote")
tags = connection.execute("SELECT * from Tags")

for row in quotes:
    print(row)
for row in authors:
    print(row)
for row in tags:
    print(row)

cursor.execute("SELECT * FROM Quote")
print(len(cursor.fetchall())) #output = 100
                    #or
TotalQuotations = cursor.execute('''SELECT COUNT(*) FROM Quote''')
for row in TotalQuotations:
    print(row) #output = 100


cursor.execute("SELECT * FROM Quote WHERE Author = 'Albert Einstein'")
print(len(cursor.fetchall())) #output = 10
                    #or
AuthorQuotationsCount = cursor.execute('''SELECT Author,COUNT(*) FROM Quote WHERE Author = "Albert Einstein"''')
for row in AuthorQuotationsCount:
    print(row) #output=('Albert Einstein', 10)


max_tag_count = "SELECT MAX(tagCount) FROM Tags"
cursor.execute(max_tag_count)
print("The maximum no of tags on a quotation is:")
print(cursor.fetchone()[0]) #output = 8


min_tag_count = "SELECT MIN(tagCount) from Tags"
cursor.execute(min_tag_count)
print("The minimum no of tags on a quotation is:")
print(cursor.fetchone()[0]) #output = 1


avg_tag_count = "select avg(tagCount) from Tags"
cursor.execute(avg_tag_count)
print("The average no of tags on a quotation is:")
print(cursor.fetchone()[0]) #output = 2.35


#Given a number N return top N authors who authored the maximum number of tags on quotations sorted in descending order of no. of tags
data = cursor.execute("""SELECT Quote.Qid,Quote.QuoteName,Quote.Author,Quote.Tags,Tags.tagCount
           FROM Quote
           INNER JOIN Tags 
           ON Quote.Tags=Tags.Tags ORDER BY Tags.tagCount DESC LIMIT 4""") 

for row in data:
    print(row)

#Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes
print("top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes  where n = 5")
quotes = cursor.execute('''SELECT Author,COUNT(*) AS quoteCount  FROM Quote GROUP BY Quote.Author ORDER BY quoteCount DESC LIMIT 5''')
for row in quotes:
    print(row)



# close our connection
connection.close()
