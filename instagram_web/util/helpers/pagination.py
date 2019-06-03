from math import ceil


class Pagination():
    # Initialises a Pagination object
    def __init__(self, items, items_per_page=5):
        self.items = items
        self.total_items = len(items)
        self.items_per_page = items_per_page
        self.total_pages = ceil(self.total_items/self.items_per_page)

    def paginate(self, current_page):
        # If current page is not within the range of 1 or the maximum number of possible pages
        if current_page < 1 or current_page > self.total_pages:
            return False
        start = (current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return [i for i in self.items][start:end]

    def prev_page(self, current_page):
        # If the prev page does not exist
        if current_page == 1:
            return False
        return True

    def next_page(self, current_page):
        # If the next page does not exist
        if current_page == self.total_pages:
            return False
        return True
