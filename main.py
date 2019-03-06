''' Web scraping application, eventually for use with AIY google home device'''

import urllib.request as urlr
from bs4 import BeautifulSoup as soup


def main():
    page_url = 'https://portal.whs.school.nz/index.php'
    page = urlr.urlopen(page_url)
    page_soup = soup(page, 'html.parser')

    notice_table = page_soup.find_all('div', attrs={'class':'table-responsive'})
    print(len(notice_table))
    print(notice_table[0])


if __name__ == '__main__':
    main()
