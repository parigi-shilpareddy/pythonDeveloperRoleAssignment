from multiprocessing import connection
import sqlite3
import json 

def get_json_data():
    with open('quotes.json','r') as read_file:
        json_file = json.loads(read_file.read())
    return json_file

def connecting_to_database():
    return sqlite3.connect('quotes.db')

def create_table(table,table_name):
    connection = connecting_to_database()
    cursor = connection.cursor()
    drop_table = "DROP TABLE IF EXISTS {}"
    cursor.execute(drop_table.format(table_name))
    cursor.execute('''PRAGMA foreign_keys = ON''')
    cursor.execute(table)
    connection.commit()
    connection.close()

def creating_authors_table():
    author_table = '''CREATE TABLE author (
        id INT NOT NULL PRIMARY KEY,
        author_name VARCHAR(250),
        born VARCHAR(250),
        reference VARCHAR(250)
    )'''
    create_table(author_table,"author")

def creating_quotes_table():
    quotes_table = '''CREATE TABLE quote (
        id INT NOT NULL PRIMARY KEY,
        quote VARCHAR(300),
        author_id INT,
        FOREIGN KEY (author_id) REFERENCES author(id)
        ON DELETE CASCADE
    )'''
    create_table(quotes_table,"quote")

def creating_tags_table():
    tags_table = '''CREATE TABLE tags (
        id INT NOT NULL PRIMARY KEY,
        tag VARCHAR(250)
    );'''
    create_table(tags_table,"tags")

def creating_quotes_tags_table():
    quotes_tags_table = '''CREATE TABLE quotes_tags (
        quote_id INT,
        tag_id INT,
        PRIMARY KEY (quote_id,tag_id),
        FOREIGN KEY (quote_id) REFERENCES quote(id)
        ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tags(id)
        ON DELETE CASCADE
    )'''
    create_table(quotes_tags_table,"quotes_tags")

def insert_values_into_table(query_statement,multiple_data):
    connection = connecting_to_database()
    cursor = connection.cursor()
    cursor.executemany(query_statement,multiple_data)
    connection.commit()
    connection.close()


def insert_values_into_authors_table(authors_list):
    id = 0 
    multiple_authors_data = []
    for each in authors_list:
        id += 1
        data_tuple = (id,each['name'],each['born'],each['reference'])
        multiple_authors_data.append(data_tuple)
    query_statement = '''INSERT INTO author VALUES (?,?,?,?);'''
    insert_values_into_table(query_statement,multiple_authors_data)

def inserting_values_into_quotes_table(quotes_list,authors_new_list):
    id = 0 
    multiple_quotes_data = []
    for each_quote in quotes_list:
        id += 1 
        author_id = authors_new_list.index(each_quote['author']) + 1 
        data_tuple = (id,each_quote['quote'],author_id)
        multiple_quotes_data.append(data_tuple)
    query_statement = '''INSERT INTO quote VALUES (?,?,?);'''
    insert_values_into_table(query_statement,multiple_quotes_data)

def inserting_values_into_tags_table(tags_list):
    id = 0 
    multiple_tags_data = []
    for each_tag in tags_list:
        id += 1 
        data_tuple = (id,each_tag)
        multiple_tags_data.append(data_tuple)
    query_statement = '''INSERT INTO tags VALUES (?,?);'''
    insert_values_into_table(query_statement,multiple_tags_data)

def inserting_values_quotes_tags_table(quotes_list,tags_list):
    quote_id = 0 
    multiple_tag_quote_data = []
    for each_quote in quotes_list:
        quote_id += 1
        for tag in each_quote['tags']:
            tag_id = tags_list.index(tag) + 1 
            data_tuple = (quote_id,tag_id)
            multiple_tag_quote_data.append(data_tuple)
    query_statement = '''INSERT INTO quotes_tags VALUES (?,?);'''
    insert_values_into_table(query_statement,multiple_tag_quote_data)


def get_new_authors_list(quotes_list):
    authors = []
    for each_author in quotes_list:
        name = each_author['author']
        if name not in authors:
            authors.append(name)
    return authors

def get_tags_list(quotes_list):
    tags_list = []
    for each_quote in quotes_list:
        for tag in each_quote['tags']:
            if tag not in tags_list:
                tags_list.append(tag)
    return tags_list

def getting_data():
    quotes_authors_data = get_json_data()
    authors_new_list = get_new_authors_list(quotes_authors_data['quotes'])
    tags_list = get_tags_list(quotes_authors_data['quotes'])
    insert_values_into_authors_table(quotes_authors_data['authors'])
    inserting_values_into_quotes_table(quotes_authors_data['quotes'],authors_new_list)
    inserting_values_into_tags_table(tags_list)
    inserting_values_quotes_tags_table(quotes_authors_data['quotes'],tags_list)

def main():
    creating_authors_table()
    creating_quotes_table()
    creating_tags_table()
    creating_quotes_tags_table()
    getting_data()

main()

