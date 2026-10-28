import random
from csv import reader
import xml.etree.ElementTree as ET


clt = 0
books = []
tags = set()

with open('books.csv', 'r', encoding='windows-1251') as csvfile:
    table = reader(csvfile, delimiter=';')
    
    next(table) 
    
    for row in table:
        title = row[1]   
        author = row[3]  
        date_str = row[6]
        
        try:
            year = int(date_str.split('.')[2].split()[0])
        except (IndexError, ValueError):
            year = 0
            
        book_info = {
            'title': title,
            'author': author,
            'year': year,
            'row_data': row 
        }
        books.append(book_info)
        
        if len(title) > 30:
            clt += 1
            
        #доп 1
        row_tags = row[12].split('#')
        for tag in row_tags:
            tagstriped = tag.strip()
            if tagstriped and len(tagstriped) > 2:
                tags.add(tagstriped)

print('1. Количество книг с названием длиннее 30 символов:', clt)


output = open('result.txt', 'w')

while True:
    flag = 0
    search = input('\n2. Введите имя автора для поиска (или 0 для выхода): ')
    if search == '0':
        break
        
    print('Результаты поиска автора (не ранее 2018 года):')
    
    for book in books:
        lower_case = book['author'].lower()
        index = lower_case.find(search.lower())
        
        if index != -1 and book['year'] >= 2018:
            print(book["author"], "|", book["title"], "(", book["year"], ")")
            output.write(f'{book["author"]}. {book["title"]} - {book["year"]}\n')
            flag += 1
            
    if flag == 0:
        print('Ничего не найдено.')
    else:
        print('Найдено', flag, 'результатов.')

output.close()


random_books = random.sample(books, min(20, len(books))) #20 случайных книг
file = open('bibliography.txt', 'w', encoding='utf-8')

for i in range(len(random_books)):
    book = random_books[i]
    file.write(f'{i + 1}. {book["author"]}. {book["title"]} - {book["year"]}\n')

file.close()
print('\n3. Библиографические ссылки сохранены в файл bibliography.txt')


print('\nДоп задание 1')
print('Уникальных жанров/тегов найдено:', len(tags), sorted(tags))

input('\nEnter для продолжения (2 часть)')
currency_dict = {}


xml_file = open('currency.xml', 'r', encoding='windows-1251')
xml_data = xml_file.read()
xml_file.close()

root = ET.fromstring(xml_data)

for valute in root.findall('Valute'):
    name_element = valute.find('Name')
    char_code_element = valute.find('CharCode')
    
    if name_element is not None and char_code_element is not None:
        name = name_element.text
        char_code = char_code_element.text
        
        currency_dict[name] = char_code


print('\nПолученный словарь "Name - CharCode"')

items = list(currency_dict.items()) #первые 10 элементов
for i in range(min(10, len(items))):
    key, value = items[i]
    print("'", key, "': '", value, "'", sep="")

print('Всего элементов в словаре:', len(currency_dict))
