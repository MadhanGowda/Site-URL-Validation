"""Temp script."""

from bs4 import BeautifulSoup
import xlsxwriter
import datetime
import urllib.request
from urllib.error import URLError, HTTPError

bad_urls = []

total_start_time = datetime.datetime.now()
print(str(total_start_time))

production_url = ''  # Add wp url here
all_urls = []
page = urllib.request.urlopen(production_url + '/sitemap_index.xml')
soup1 = BeautifulSoup(page, "html.parser")

all_site_map_urls = soup1.findAll('loc')
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
    except URLError as e:
        # do something (set req to blank)
        print('Fail: Reason: ', e.reason, each.text)
    print('Pass: Scraped sitemap ->' + each.text)

all_urls = set(all_urls)
all_urls = list(all_urls)
print('Scraped all URLs found ' + str(len(all_urls)))

workbook = xlsxwriter.Workbook('demo1.xlsx')
worksheet1 = workbook.add_worksheet('error_url')
worksheet2 = workbook.add_worksheet('error_pages')

w2 = 0
number = 0
count = 1
for url in all_urls:
    start_time = datetime.datetime.now()
    try:
        page3 = urllib.request.urlopen(url)
        soup3 = BeautifulSoup(page3, "html.parser")
        b_url_list = []
        for link in soup3.findAll('a'):
            val_url = link.get('href')
            for b_url in bad_urls:
                if val_url and val_url.find(b_url) > 0:
                    b_url_list.append(val_url)

        if len(b_url_list) > 0:
            worksheet1.write(number, 0, datetime.datetime.now().strftime('%x'))
            worksheet1.write(number, 1, url)
            for wr_url in b_url_list:
                worksheet1.write(number, 2, wr_url)
                number += 1
        print(str(count) + '/' + str(len(all_urls)) + ' -> time taken ' + str(datetime.datetime.now() - start_time) +' -> Scraped sub url' + str(url) + 'found issue ' + str(len(b_url_list)), b_url_list)
    except HTTPError as e:
        # do something
        print('Fail: Error code: ', e.code, url)
        worksheet2.write(w2, 0, url)
        worksheet2.write(w2, 1, e.code)
    except URLError as e:
        # do something (set req to blank)
        print('Fail: Reason: ', e.reason, url)
        worksheet2.write(w2, 0, url)
        worksheet2.write(w2, 1, e.reason)
    count += 1

workbook.close()
print('Completed all total time taken is ' + str(datetime.datetime.now() - total_start_time))
