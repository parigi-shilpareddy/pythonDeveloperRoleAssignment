import json
import requests 
from bs4 import BeautifulSoup

def get_parsed_file(page_url):
    request = requests.get(page_url) 
    soup = BeautifulSoup(request.content,'html.parser')
    return soup

def return_next_page(page_url):
    parsed_file = get_parsed_file(page_url)
    next_page_class = parsed_file.select('nav ul li')[-1]['class']
    if next_page_class == ['next']:
        next_page_url =parsed_file.select('nav ul li a')[-1]['href']
        return "http://quotes.toscrape.com" + next_page_url    
    return ""

def get_quotes_data(quotes_data,page_url):
    parsed_file = get_parsed_file(page_url)
    for link in (parsed_file.find_all("div", attrs={"class": "quote"})):
        quote_text = link.find("span", attrs={"class": "text", "itemprop": "text"})
        quote_author = link.find("small", attrs={"class": "author", "itemprop": "author"})
        quote_tags = link.find_all("a", attrs={"class": "tag"})
        each_quote_data = {"quote": quote_text.text.encode("ascii", "ignore").decode('utf-8'), "author": quote_author.text, "tags": [_qt_.text for _qt_ in quote_tags]}
        quotes_data.append(each_quote_data)
    return quotes_data

def get_author_born_details(author_parsed_file):
    authors_born_date = author_parsed_file.select_one('.author-born-date').text.strip()
    authors_born_country = author_parsed_file.select_one('.author-born-location').text.strip()
    born = authors_born_date+' '+authors_born_country
    return born

def author_parsing_getting_unique(unique_authors_list,reference):
    if reference not in unique_authors_list:
        unique_authors_list.append(reference)
        author_page_url = "http://quotes.toscrape.com"+reference+"/"
        author_parsed_file = get_parsed_file(author_page_url)
        author_born = get_author_born_details(author_parsed_file)
        author_name = reference.split('/')[-1].replace('-',' ')
        return {'name':author_name,'born':author_born,'reference':author_page_url}


def get_authors_data(authors_data,page_url,unique_authors_list):
    parsed_file = get_parsed_file(page_url)
    for author_reference in parsed_file.find_all("div", attrs={"class": "quote"}):
        reference = author_reference.select_one('.quote a')['href']
        details = author_parsing_getting_unique(unique_authors_list,reference)
        if details != None:
            authors_data.append(details)
    return authors_data

def  getting_the_data(quotes_data,authors_data,unique_authors_list):
    page_url = "http://quotes.toscrape.com"
    while True:
        quotes_list = get_quotes_data(quotes_data,page_url)
        authors_list = get_authors_data(authors_data,page_url,unique_authors_list)
        page_url = return_next_page(page_url)
        if page_url == "":
            break
    quotes_dict = {"quotes":quotes_list,"authors":authors_list}
    return quotes_dict

def converting_data_json_file(quotes):
    with open('quotes.json', 'w') as f:
     json.dump(quotes, f, indent=4)

    with open('quotes.json', 'r') as f:
        quotes = json.load(f)
    
def main():
    unique_authors_list = []
    quotes_data = []
    authors_data = []
    quotes_authors_data_dict = getting_the_data(quotes_data,authors_data,unique_authors_list)
    converting_data_json_file(quotes_authors_data_dict)

main()