from booking.booking import Booking
from playwright.sync_api import sync_playwright
import time
from prettytable import PrettyTable
if __name__ == '__main__':
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(slow_mo=1000)
        page = browser.new_page()
        booking = Booking(page, browser)

        #Booking.com = land_first_page
        booking.land_first_page()
        #wählt die Währung aus
        booking.change_currency(currency='EUR')
        #input wo möchte man hin?
        booking.select_place_go_to(place_to_go=input('Wohin möchest du reisen? '))
        #input wann möchte man anreisen und wann abreisen?
        booking.select_dates(check_in_date=input('Wann möchtest du anreisen?: '), check_out_date=input('Wann möchtest du abreisen?: '))
        #input wie viele personen?
        booking.select_adults(int(input('Mit wie vielen Personen möchtest du reisen ? ')))
        #klickt auf den "Suchen-Button"
        booking.click_search()
        #Ergebnis wird Sortiert
        booking.sort_by()
        #ergebnis ausgabe
        results = booking.get_results()
        table = PrettyTable(
            field_names=['Name des Hotels', 'Preis', 'Bewertung des Hotels']
        )
        table.add_rows(results)
        print(table)
        browser.close()