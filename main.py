from tipico_scraper import TipicoScraper
from combination_bet_creator import CombinationBetCreator
from bets_to_excel import BetsToExcel

from bs4 import BeautifulSoup as Bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def main():
    scraper = TipicoScraper()
    scraper.scrape_all()
    print("########################")
    scraper.sort_matches_by_lowest_quote()
    #scraper.filter_min_lowest_quote(1.15)
    #scraper.filter_max_lowest_quote(1.7)
    scraper.print_matches()
    print("########################")

    cbc = CombinationBetCreator(matches=scraper.matches, combination_size=3)
    cbc.create_bets_with_outcome_lowest_quote()
    cbc.create_random_combi_bets()
    cbc.refresh_statistics()
    cbc.sort_combi_bets_by_quote()
    print(cbc)
    print("########################")

    cbc.optimize()
    print(cbc)

    saver = BetsToExcel(cbc.combi_bets)
    saver.fill_data_lists()
    saver.save_to_excel()


def driver_scrap_test():
    driver = webdriver.Firefox()
    driver.get("https://www.tipico.de/de/online-sportwetten/fussball/deutschland/bundesliga/g42301/")
    soup = Bs(driver.page_source, "html.parser")
    print(soup.prettify())

    buttons = driver.find_elements_by_xpath("//div[@class='t_more bl align_c right']")

    for button in buttons:
        button.click()

    pass

    # div class="limits_hover "

if __name__ == "__main__":
    #main()
    driver_scrap_test()




