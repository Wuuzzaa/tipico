from tipico_scraper import TipicoScraper
from combination_bet_creator import CombinationBetCreator
from bets_to_excel import BetsToExcel


def main():
    # scrap
    scraper = TipicoScraper()
    scraper.scrape_all()
    print("########################")

    # filter
    print("Filtering...")
    scraper.sort_matches_by_lowest_quote()
    scraper.filter_time_horizon_start_in_next_days(7)
    scraper.filter_min_lowest_quote(1.15)
    scraper.filter_max_lowest_quote(1.45)
    print("########################\n")

    # matches
    print(f"matches for bets: {len(scraper.matches)}")
    scraper.print_matches()
    print("########################\n")

    # create, optimize bets
    cbc = CombinationBetCreator(matches=scraper.matches, combination_size=3)
    cbc.create_bets_with_outcome_lowest_quote()
    cbc.create_random_combi_bets()
    cbc.refresh_statistics()
    cbc.sort_combi_bets_by_quote()
    print(cbc.__str__(mode="SHORT"))
    print("########################")

    cbc.optimize()
    print(cbc.__str__(mode="SHORT"))

    saver = BetsToExcel(cbc.combi_bets)
    saver.fill_data_lists()
    saver.save_to_excel()


if __name__ == "__main__":
    main()




