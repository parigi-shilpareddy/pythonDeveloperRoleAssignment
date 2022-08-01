import sqlite3
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM Quote")
print(len(cursor.fetchall())) #output = 100

#cursor.executemany(sqlite_insert_with_param, multiple_tags)
cursor.execute("SELECT * FROM Quote WHERE Author = 'Albert Einstein'")
print(len(cursor.fetchall())) #output = 10

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

#Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes
data = cursor.execute("""SELECT Quote.Qid,Quote.QuoteName,Quote.Author,Quote.Tags,Tags.tagCount
           FROM Quote
           INNER JOIN Tags 
           ON Quote.Tags=Tags.Tags ORDER BY Tags.tagCount DESC LIMIT 4""") 

for row in data:
    print(row)
# close our connection
connection.close()