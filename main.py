import urllib.request as urlr
from bs4 import BeautifulSoup as soup

class Notice:
    def __init__(self, first_row, second_row):
        # split first row into table cells 
        first_row = first_row.find_all('td')
        # set title
        self.title = first_row[1].text.lower()
        # set staff member
        self.staff = first_row[-1].text.upper()

        # set room / time
        if len(first_row) > 3:
            self.room = first_row[2].text.lower()
            self.time = first_row[3].text.lower()
        else:
            self.room = None
            self.time = None
        
        # set detail
        self.detail = second_row.find('td').text

    def to_string(self):
        if self.room != None:
            return f'{self.title} - {self.room} - {self.time}\n{self.detail}\n{self.staff}'
        else:
            return f'{self.title}\n{self.detial}\n{self.staff}'


def get_notice_data(url):
    # open url
    page = urlr.urlopen(url)

    # soup-ify page
    page_soup = soup(page, 'html.parser')

    # get both notice tables
    notice_tables = page_soup.find_all('div', attrs={'class':'table-responsive'})

    # put notices into objects
    notices = []
    for notice_table in notice_tables:

        # split notice table into rows
        rows = notice_table.find_all('tr')

        # remove header row
        rows = rows[1:]

        # build notice obj from html
        for row_id in range(0, len(rows), 2):

            # create notice
            notice = Notice(rows[row_id], rows[row_id + 1])

            # append to notices
            notices.append(notice)

    return notices


def main():
    # notices page url
    notices_url = 'https://portal.whs.school.nz/index.php'

    # scrape page
    notices = get_notice_data(notices_url)

    print(notices[0].to_string())


if __name__ == '__main__':
    main()
