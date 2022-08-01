import sqlite3
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

print("Total No of quotations:")
cursor.execute("SELECT * FROM Quote")
print(len(cursor.fetchall())) #output = 100

#cursor.executemany(sqlite_insert_with_param, multiple_tags)
print("Total no of quotations by Albert Einstein")
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
print("Top N authors who authored and their Quotations")
data = cursor.execute("""SELECT Quote.Qid,Quote.QuoteName,Quote.Author,Quote.Tags,Tags.tagCount
           FROM Quote
           INNER JOIN Tags 
           ON Quote.Tags=Tags.Tags ORDER BY Tags.tagCount DESC LIMIT 4""") 

for row in data:
    print(row)
# close our connection
connection.close()

#outputs
#Total No of quotations
#100
#Total no of quotations by Albert Einstein
#10
#The maximum no of tags on a quotation is:
#8
#The minimum no of tags on a quotation is:
#1
#The average no of tags on a quotation is:
#2.35
#Top N authors who authored and their Quotations where n = 5
#(17, "“The opposite of love is not hate, it's indifference. The opposite of art is not ugliness, it's indifference. The opposite of faith is not heresy, it's indifference. And the opposite of life is not death, it's indifference.”", 'Elie Wiesel', 'activism apathy hate indifference inspirational love opposite philosophy', 8)
#(77, "“You may say I'm a dreamer, but I'm not the only one. I hope someday you'll join us. And the world will live as one.”", 'John Lennon', 'beatles connection dreamers dreaming dreams hope inspirational peace', 8)
#(97, '“You have to write the book that wants to be written. And if the book will be too difficult for grown-ups, then you write it for children.”', "Madeleine L'Engle", 'books children difficult grown-ups write writers writing', 7)
#(11, "“This life is what you make it. No matter what, you're going to mess up sometimes, it's a universal truth. But the good part is you get to decide how you're going to mess it up. Girls will be your friends - they'll act like it anyway. But just remember, some come, some go. The ones that stay with you through everything - they're your true best friends. Don't let go of them. Also remember, sisters make the best friends in the world. As for lovers, well, they'll come and go too. And baby, I hate to say it, most of them - actually pretty much all of them are going to break your heart, but you can't give up because if you give up, you'll never find your soulmate. You'll never find that half who makes you whole and that goes for everything. Just because you fail once, doesn't mean you're gonna fail at everything. Keep trying, hold on, and always, always, always believe in yourself, because if you don't, then who will, sweetie? So keep your head high, keep your chin up, and most importantly, keep smiling, because life's a beautiful thing and there's so much to smile about.”", 'Marilyn Monroe', 'friends heartbreak inspirational life love sisters', 6)
#(18, '“It is not a lack of love, but a lack of friendship that makes unhappy marriages.”', 'Friedrich Nietzsche', 'friendship lack-of-friendship lack-of-love love marriage unhappy-marriage', 6)