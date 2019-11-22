def get_books_search_info(length):
    if length == 0:
        return {'searchInfo': "К сожалению, мы не нашли ни одной книги"}
    else:
        if length == 1:
            return {'searchInfo': "Найдена 1 книга"}
        elif length % 10 > 4 or 9 > length % 10 > 20 or length % 10 == 0:
            return {'searchInfo': f"Найдено {length} книг"}
        else:
            return {'searchInfo': f"Найдено {length} книги"}
