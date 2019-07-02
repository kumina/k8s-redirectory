import math


class Page:

    def __init__(self, items, page, page_size, total):
        self.items = items
        self.previous_page = None
        self.next_page = None

        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1

        previous_items = (page - 1) * page_size

        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1

        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))


def paginate(query, page: int, page_size: int) -> Page:
    """
    Creates a query with the help of limit() and offset() to represent a page.
    Also counts the total number of items in the given database.

    Args:
        query: the query which specifies the model tha paginate
        page (int): the page number
        page_size (int): how many items per page

    Returns:
        a Page object with all the items inside
    """
    assert isinstance(page, int) and page > 0
    assert isinstance(page_size, int) and page_size > 0

    items = query.limit(page_size).offset((page - 1) * page_size).all()
    total = query.order_by(None).count()
    return Page(items, page, page_size, total)
