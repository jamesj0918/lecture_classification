import requests
import codecs
import re
from text_parser import parse as parse

book_classes = []
lectures = []

book_class_text = codecs.open("book_class.txt", "r", "UTF-8")
lecture_text = codecs.open("lectures.txt", "r", "UTF-8")
classified_result = codecs.open("classified_result.txt", "w", "UTF-8")
unclassified_lectures = codecs.open("unclassified_lectures.txt", "w", "UTF-8")

parse(book_class_text, book_classes)
parse(lecture_text, lectures)

response_regex = re.compile('title="+\D+" class=+.+">+\D+<em>[(]+\d+[)]<')
book_class_regex = re.compile('title="+\D+" ')
num_regex = re.compile('[(]+\d+[)]')
total_regex = re.compile('>전체<em>[(]+\d+[건)]')

for lecture in lectures:
    search = lecture.rstrip()

    if search[len(search) - 1] is '\n':
        search = lecture[:len(lecture) - 2]

    if search[len(search) - 1].isdigit() is True:
        search = lecture[:len(lecture) - 2]

    search = search.replace("ES-", "")
    search = search.replace("GMSW-", "")
    search = search.replace("SM-", "")
    search = search.replace("K-MOOC:", "")

    response = requests.get(
        'https://book.naver.com/search/search.nhn?sm=sta_hty.book&sug=&where=nexearch&query=' + search)

    total = 0
    response_data = []

    for data in response_regex.findall(response.text):
        data_book_class = book_class_regex.search(data).group().replace('title=', '').replace('"', '').rstrip()
        num = int(num_regex.search(data).group().replace('(', '').replace(')', ''))

        try:
            book_classes.index(data_book_class)
            total += num

            tmp_data = []
            tmp_data.append(num)
            tmp_data.append(data_book_class)

            response_data.append(tmp_data)

        except ValueError:
            pass

    response_data.sort(reverse=True)

    if response_data and response_data[0][0]/total > 0.2:
        classified_result.write(lecture + '\n')
        for data in response_data:
            if data[0]/total > 0.2:
                classified_result.write(data[1] + '\n')
        classified_result.write('\n')
    else:
        unclassified_lectures.write(lecture + '\n')