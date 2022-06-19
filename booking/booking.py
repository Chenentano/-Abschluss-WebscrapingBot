import booking.constants as const
from playwright.sync_api import Page
from bs4 import BeautifulSoup
import time


class Booking:

    def __init__(self, page: Page, browser=None):
        self.base_url = const.BASE_URL
        self.page: Page = page
        self.browser = browser

    def land_first_page(self):
        self.page.goto(self.base_url)

    def change_currency(self, currency=None):
        self.page.click('button[data-tooltip-text="Choose your currency"]')
        self.page.click(f'a[data-modal-header-async-url-param*="selected_currency={currency}"]')

    def select_place_go_to(self, place_to_go):
        self.page.fill('#ss', '')
        self.page.fill('#ss', place_to_go)
        self.page.click('li[data-i="0"]')

    def select_dates(self, check_in_date, check_out_date):
        if self.page.is_visible(f'td[data-date="{check_in_date}"]'):
            self.page.click(f'td[data-date="{check_in_date}"]')
        else:
            while not self.page.is_visible(f'td[data-date="{check_in_date}"]'):
                self.page.click('div[data-bui-ref="calendar-next"] ')
            self.page.click(f'td[data-date="{check_in_date}"]')
        if self.page.is_visible(f'td[data-date="{check_out_date}"]'):
            self.page.click(f'td[data-date="{check_out_date}"]')
        else:
            while not self.page.is_visible(f'td[data-date="{check_out_date}"]'):
                self.page.click('div[data-bui-ref="calendar-next"] ')
            self.page.click(f'td[data-date="{check_out_date}"]')

    def select_adults(self, count=1):
        self.page.click('#xp__guests__toggle')
        while self.page.input_value('#group_adults') != '1':
            self.page.click('button[aria-label="Decrease number of Adults"]')
        for _ in range(count-1):
            self.page.click('button[aria-label="Increase number of Adults"]')

    def click_search(self):
        self.page.click('button[data-sb-id="main"]')

    def sort_by(self, order_type="price"):
        if self.page.is_visible('button[data-testid="sorters-dropdown-trigger"]'):
            self.page.click('button[data-testid="sorters-dropdown-trigger"]')
            self.page.click(f'button[data-id="{order_type}"]')
        else:
            self.page.click('div[data-sort-bar-container="sort-bar"] a[data-type="dropdown"]')
            self.page.click(f'a[data-type="{order_type}"]')
        while self.page.is_visible('div[data-testid="overlay-card"]'):
            pass

    @staticmethod
    def parse_hotel_detail(soup_hotel_object):
        result = {
            "name": soup_hotel_object.find('a', {"data-testid": "title-link"}).find('div', {"data-testid": "title"}).text,
            "price": soup_hotel_object.find('div', {"data-testid": "price-and-discounted-price"}).findAll('span')[-1].text
        }
        if soup_hotel_object.find('div', {"data-testid": "rating-stars"}):
            result.update({'rating': len(soup_hotel_object.find('div', {"data-testid": "rating-stars"}).findAll('span'))})
        elif soup_hotel_object.find('div', {"data-testid": "rating-squares"}):
            result.update({'rating': len(soup_hotel_object.find('div', {"data-testid": "rating-squares"}).findAll('span'))})
        return result

    def get_results(self):
        results_html = self.page.inner_html('div[data-block-id="hotel_list"]')
        soup = BeautifulSoup(results_html, 'html.parser')
        rows = soup.findAll('div', {"data-testid": "property-card"})
        hotels = []
        for row in rows:
            data = self.parse_hotel_detail(row)
            hotels.append([data.get('name'),  data.get('price'), data.get('rating', '-')])
        return hotels
