# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from src.Extractor import Extractor


def run_scrapper(url):
    # Use a breakpoint in the code line below to debug your script.
    extractor = Extractor()
    raw_page = extractor.consume_page(url)
    print(raw_page)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    url = "https://www.meilleursagents.com/annonces/achat/search/?item_types=ITEM_TYPE.APARTMENT&place_ids=2259,2260&page=1"
    run_scrapper(url)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
