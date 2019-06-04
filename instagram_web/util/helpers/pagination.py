from math import ceil


class Pagination():
    # Initialises a Pagination object
    def __init__(self, items, items_per_page=10):
        self.items = items
        self.total_items = len(items)
        self.items_per_page = items_per_page

    @property
    def total_pages(self):
        return ceil(self.total_items/self.items_per_page)

    def paginate(self, current_page):
        # If current page is not within the range of 1 or the maximum number of possible pages
        if current_page < 1 or current_page > self.total_pages:
            return False
        start = (current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        return [i for i in self.items][start:end]

    def prev_page(self, current_page):
        # If the current_page > 1, prev_page exists
        return current_page > 1

    def next_page(self, current_page):
        # If the next page does not exist
        return current_page < self.total_pages
