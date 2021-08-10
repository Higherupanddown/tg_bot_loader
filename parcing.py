from os import link, name, path
from bs4 import BeautifulSoup
import requests
import re
import json

# print('Введите название книги, серию или автора')
# text = input()
proxies = {
        'http':'socks5h://127.0.0.1:9150',
        'https':'socks5h://127.0.0.1:9150'
    }
books_dict = {}
links=['']*3

#возврат списка книг
def parcing(boockname, id):
    text = boockname.replace(' ', '+')
    url = 'http://flibustahezeous3.onion/booksearch?ask=' + text

    req = requests.get(url, proxies=proxies)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    content = soup.find('h3', text=re.compile('Найденные книги'))

    if content != None:
        content_number = content.text
        books = content.find_next_sibling().findAll('li')
        books_dict = {}
        i=0
        for item in books:
            i+=1
            item_text = str(i) + '. ' + item.text
            item_url = 'http://flibustahezeous3.onion' + item.find('a').get('href')
        #    print(f"{item.text}:{item_url}")
            books_dict[item_text] = item_url
        
        listbooks = list(books_dict.keys())
        book="\n".join(str(x) for x in listbooks)
        if len(book)>=4096:
            book=book[:4096]
            book=book.rpartition('\n')[0]
        with open(f'dicts/books{id}.json', 'w', encoding='utf-8') as file:
             json.dump(books_dict, file, indent=4, ensure_ascii=False)
        # i = 0
        # for item in book:
        #     i=i+1
        #     print(f'{i} {item}')
    else:
        book='404'
    return book

#возврат ссылки на выбранную книгу
def booknumber(number, id):
    with open(f'dicts/books{id}.json', 'r', encoding='utf-8') as f:
        books_dict=json.loads(f.read())
    book=list(books_dict.keys()) 
    i = int(number)-1
    if i < len(list(books_dict.values())):
        url = list(books_dict.values())[i]
        books_dict.update({'fb2':url+'/fb2'})
        books_dict.update({'epub':url+'/epub'})
        books_dict.update({'mobi':url+'/mobi'})
        books_dict.update({'i':i})
        number_of_form='Выберете формат для скачивания: \n1. fb2 \n2. epub \n3. mobi'
        with open(f'dicts/books{id}.json', "w", encoding='utf-8') as write_file:
            json.dump(books_dict, write_file)
    else:
        number_of_form='Цифры, Мейсон!'

    return number_of_form
#/\:*?«<>|
#возврат файла (названия)
def filename(number, id):
    with open(f'dicts/books{id}.json', 'r', encoding='utf-8') as f:
        books_dict=json.loads(f.read())
    number = int(number)
    book=list(books_dict.keys())
    path='books/' + str(id) + '.fb2'
    f=open(f'{path}', 'wb')
    if number == 1:
        links = books_dict.get('fb2')
    elif number == 2:
        links = books_dict.get('epub')
    elif number == 3:
        links = books_dict.get('mobi')
    content = requests.get(f'{links}', proxies=proxies)
    f.write(content.content)
    f.close
    return  path