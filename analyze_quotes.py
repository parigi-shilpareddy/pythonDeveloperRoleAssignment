from operator import ge
import sqlite3
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

def GetTotalQuotatins():
    TotalQuotations = cursor.execute('''SELECT COUNT(*) FROM Quote''')
    for row in TotalQuotations:
        print(row) #output = 100

def getCountOfQuotationsByAlbertEienstein():
    AuthorQuotationsCount = cursor.execute('''SELECT Author,COUNT(*) FROM Quote WHERE Author = "Albert Einstein"''')
    for row in AuthorQuotationsCount:
        print(row) #output=('Albert Einstein', 10)

def getMinMaxAvgCountOfTags():
#maximum minimum average number of tags on a quote
    max_min_avg_tag_count = "SELECT MAX(TagsCount),MIN(TagsCount),AVG(TagsCount) FROM Quote"
    for count in max_min_avg_tag_count:
        print(count) #output (8,1,2.35)

def getDataByLimitByAuthor():
#Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes
    print("top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes  where n = 5")
    quotes = cursor.execute('''SELECT Author,COUNT(*) AS quoteCount  FROM Quote GROUP BY Quote.Author ORDER BY quoteCount DESC LIMIT 5''')
    for row in quotes:
        print(row)

def main():
    GetTotalQuotatins()
    getCountOfQuotationsByAlbertEienstein()
    getMinMaxAvgCountOfTags()
    getDataByLimitByAuthor()

main()
# close our connection
connection.close()

#outputs

#Total No of quotations
#100

#Total no of quotations by Albert Einstein
#10

#maximum minimum average number of tags on a quote
#(8,1,2.35)


#Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes  where n = 5
#('Albert Einstein', 10)
#('J.K. Rowling', 9)
#('Marilyn Monroe', 7)
#('Mark Twain', 6)
#('Dr. Seuss', 6)