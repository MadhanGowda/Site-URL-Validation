"""Function to Get all urls from wordpress site."""

from bs4 import BeautifulSoup
import xlsxwriter
import datetime
import urllib.request
from urllib.error import URLError, HTTPError

total_start_time = datetime.datetime.now()
print(str(total_start_time))

production_url = ''  # Add wp url here
all_urls = []

page = urllib.request.urlopen(production_url + '/sitemap_index.xml')
soup1 = BeautifulSoup(page, "html.parser")

workbook = xlsxwriter.Workbook('all_urls.xlsx')
worksheet1 = workbook.add_worksheet('all_url')
worksheet2 = workbook.add_worksheet('error_url')

all_site_map_urls = soup1.findAll('loc')
good_url_num = 0
bad_url_num = 0
for each in all_site_map_urls:
    try:
        page2 = urllib.request.urlopen(each.text)
        soup2 = BeautifulSoup(page2, "html.parser")
        sub_urls = soup2.findAll('loc')
        for each1 in sub_urls:
            all_urls.append(each1.text)

    except HTTPError as e:
        # do something
        print('Fail: Error code: ', e.code, each.text)
        worksheet2.write(good_url_num, 0, each.text)
    except URLError as e:
        # do something (set req to blank)
        print('Fail: Reason: ', e.reason, each.text)
        worksheet2.write(good_url_num, 0, each.text)
    print('Pass: Scraped sitemap ->' + each.text)

all_urls = set(all_urls)
all_urls = list(all_urls)

for g_url in all_urls:
    worksheet1.write(good_url_num, 0, g_url)
    good_url_num += 1

print('Scraped all URLs found ' + str(len(all_urls)))
workbook.close()
