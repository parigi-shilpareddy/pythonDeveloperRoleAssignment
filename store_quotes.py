import sqlite3
import json                                      

connection = sqlite3.connect('store.db')
cursor = connection.cursor()


with open("/Users\parig\VsCodePython\quotes.json") as f:
    data = json.load(f)
    

authors_table = '''
               CREATE TABLE authors(
              id INTEGER NOT NULL PRIMARY KEY,
               author VARCHAR(250),
               born VARCHAR(300),
               reference VARCHAR(300)
               );
               '''
quotes_table = ''' CREATE TABLE Quote
            (Qid INT PRIMARY KEY     NOT NULL,
             QuoteName TEXT    NOT NULL,
               Author TEXT     NOT NULL,
            TagsCount  INT);
            '''

tags_table = '''CREATE TABLE Tags
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               tag_name VARCHAR(250),
               quote_id INTEGER,
               FOREIGN KEY (quote_id) REFERENCES Quote(Qid) 
               ON DELETE CASCADE)'''


connection.execute(authors_table)
connection.execute(quotes_table)
connection.execute(tags_table)

multiple_quotes = []
for i in range(len(data['quotes'])):
    tag_count=len(data['quotes'][i]['tags'])
    data_tuple = (i+1,data['quotes'][i]['quote'],data['quotes'][i]['author'],tag_count)
    multiple_quotes.append(data_tuple)

sqlite_insert_with_param = """INSERT INTO Quote
                             VALUES (?, ?, ?, ?);"""
cursor.executemany(sqlite_insert_with_param, multiple_quotes)

multiple_authors = []
for i in range(len(data['authors'])):
    data_tuple = (i+100,data['authors'][i]['name'],data['authors'][i]['born'],data['authors'][i]['reference'])
    multiple_authors.append(data_tuple)

sqlite_insert_with_param_authors = """INSERT INTO Authors
                        VALUES (?, ?, ?,?);"""
cursor.executemany(sqlite_insert_with_param_authors, multiple_authors)


multiple_tags = []
for i in range(len(data['quotes'])):
    tag=data['quotes'][i]['tags']
    for each in tag:
        data_tuple = [each,i+1]
        multiple_tags.append(data_tuple)
sqlite_insert_with_param_authors = """INSERT INTO Tags(tag_name,quote_id)
                             VALUES (?,?);"""
cursor.executemany(sqlite_insert_with_param_authors, multiple_tags)




authors = connection.execute("SELECT * from Authors")
quotes = connection.execute("SELECT * from Quote")
tags = connection.execute("SELECT * from Tags")

for row in quotes:
    print(row)
for row in authors:
    print(row)
for row in tags:
    print(row)


TotalQuotations = cursor.execute('''SELECT COUNT(*) FROM Quote''')
for row in TotalQuotations:
    print(row) #output = 100


AuthorQuotationsCount = cursor.execute('''SELECT Author,COUNT(*) FROM Quote WHERE Author = "Albert Einstein"''')
for row in AuthorQuotationsCount:
    print(row) #output=('Albert Einstein', 10)

#maximum minimum average number of tags on a quote
max_min_avg_tag_count = "SELECT MAX(TagsCount),MIN(TagsCount),AVG(TagsCount) FROM Quote"
for count in max_min_avg_tag_count:
    print(count) #output (8,1,2.35)

#Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes
print("top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes  where n = 5")
quotes = cursor.execute('''SELECT Author,COUNT(*) AS quoteCount  FROM Quote GROUP BY Quote.Author ORDER BY quoteCount DESC LIMIT 5''')
for row in quotes:
    print(row)



# close our connection
connection.close()
