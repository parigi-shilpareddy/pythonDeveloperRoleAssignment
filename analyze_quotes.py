# Importing Sqlite3 Module
import sqlite3

def connecting_to_database():
    connection = sqlite3.connect('quotes.db')
    return connection.cursor()

def get_total_quotations():
    cursor = connecting_to_database()
    total_quotations = cursor.execute('''SELECT COUNT(*) FROM quote''')
    for count in total_quotations:
        print(count) #output (100,)

def get_quotations_by_author():
    cursor = connecting_to_database()
    author_name = input("enter author name: ")
    query = '''SELECT author.author_name,COUNT(*) FROM author JOIN quote WHERE quote.author_id = author.id AND author.author_name ={}'''
    string_query = query.format(author_name)
    total_quotations_by_author = cursor.execute(string_query)
    for count in total_quotations_by_author:
        print(count) #output ('Albert Einstein', 10)
    
def get_min_max_avg_count_tags():
    cursor = connecting_to_database()
    query = cursor.execute('''
        SELECT MAX(total_tags),MIN(total_tags),AVG(total_tags) FROM (
            SELECT COUNT(tag_id) AS total_tags
            FROM quotes_tags
            GROUP BY quote_id
        )
    ''')
    for max_min_avg in query:
        print(max_min_avg) #output (8, 1, 2.3917525773195876)
    
def get_data_by_limit_by_author():
    cursor = connecting_to_database()
    limit_value = input("Enter the limit value")
    query = '''
        SELECT author.author_name,COUNT(*) AS quotes_count 
        FROM quote JOIN author 
        WHERE quote.author_id = author.id 
        GROUP BY quote.author_id 
        ORDER BY quotes_count DESC 
        LIMIT {}
    '''
    string_query = query.format(limit_value)
    result_after_performing_query = cursor.execute(string_query)
    for each in result_after_performing_query:
        print(each)
    # output
    # ('Albert Einstein', 10)
    # ('J K Rowling', 9)
    # ('Marilyn Monroe', 7)
    # ('Mark Twain', 6)
    # ('Dr Seuss', 6)


def performing_queries():
    get_total_quotations()
    get_quotations_by_author()
    get_min_max_avg_count_tags()
    get_data_by_limit_by_author()


performing_queries()
