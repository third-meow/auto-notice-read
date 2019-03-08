import sys
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
        if self.room is not None:
            return f'{self.title} - {self.room} - {self.time}\n \
                    {self.detail}\n \
                    {self.staff}'
        else:
            return f'{self.title}\n{self.detail}\n{self.staff}'

    def selfprint(self):
        print(self.to_string())


def get_notice_data(url):
    # open url
    page = urlr.urlopen(url)

    # soup-ify page
    page_soup = soup(page, 'html.parser')

    # get both notice tables
    notice_tables = page_soup.find_all(
        'div',
        attrs={'class': 'table-responsive'})

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


def get_keywords():
    keywords = []

    if '-u' in sys.argv:
        # receive keywords from user
        print('Enter keywords, one per line. Enter DONE to finished')
        cmd = input()
        while(cmd != 'DONE'):
            keywords.append(cmd.strip().lower())
            cmd = input()
    else:
        # read keywords from file
        with open('keywords.txt', 'r') as f:
            contents = f.read().split('\n')

        # remove commented lines
        for line in contents:
            if '#' in line:
                position = line.find('#')
                keywords.append(line[:position].strip())
            else:
                keywords.append(line.strip())

    # remove blank lines
    keywords = [keyword for keyword in keywords if keyword != '']

    return keywords


def find_relevent_notices(notices, keywords):
    relevent = []
    for notice in notices:
        for keyword in keywords:
            if keyword in notice.title or keyword in notice.detail:
                # add notice to relevent list
                relevent.append(notice)
                break

    return relevent


def main():
    # notices page url
    notices_url = 'https://portal.whs.school.nz/index.php'

    # scrape page
    notices = get_notice_data(notices_url)

    # search keywords array
    keywords = get_keywords()

    # search notices for keywords
    relevent_notices = find_relevent_notices(notices, keywords)

    for rvn in relevent_notices:
        rvn.selfprint()


if __name__ == '__main__':
    main()
