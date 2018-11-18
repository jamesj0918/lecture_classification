import codecs
from text_parser import parse as parse

book_classes = []
classified_result = []

book_class_text = codecs.open("book_class.txt", "r", "UTF-8")
classified_result_text = codecs.open("classified_result.txt", "r", "UTF-8")
final_result = codecs.open("final_result.txt", "w", "UTF-8")

parse(book_class_text, book_classes)
parse(classified_result_text, classified_result)

for book_class_data in book_classes:

    try:
        classified_result.index(book_class_data)
        final_result.write(book_class_data + '\n')
    except ValueError:
        continue

    for i, result_data in enumerate(classified_result):
        if book_class_data == result_data:
            tmp = i
            while classified_result[tmp][len(classified_result[tmp]) - 1] is not '\r':
                tmp = tmp-1
            final_result.write(classified_result[tmp].rstrip() + ' ')
    final_result.write('\n\n')
