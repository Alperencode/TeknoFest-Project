from pyzbar.pyzbar import decode
from isbnlib import *

result_dictionary = {}
last_book = ""

def ParseISBN(isbn):
    if not is_isbn10(isbn) and not is_isbn13(isbn):
        return False
    else:
        return meta(isbn)

def ParseMeta(isbn_meta):
    global last_book
    if isbn_meta["Title"] != last_book:
        print("Title:", isbn_meta["Title"])
        last_book = isbn_meta["Title"]
    # print("Kitap:", isbn_meta["Title"])
    for key, value in isbn_meta.items():
        result_dictionary[key] = value

def OutputTXT():
    if result_dictionary:
        with open('output.txt', 'w',encoding='utf-8') as f:
            for key, value in result_dictionary.items():
                if type(result_dictionary[key]) == list:
                    f.write(f"{key}: ")
                    for item in result_dictionary[key]:
                        f.write(f"{item}, ") if item != result_dictionary[key][-1] else f.write(f"{item}")
                    f.write("\n")
                else:
                    f.write(f"{key}: {value}\n")
    else:
        pass

def GetResult():
    return result_dictionary