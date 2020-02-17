"""Temp script."""

from bs4 import BeautifulSoup
import xlsxwriter

import datetime

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()

soup = BeautifulSoup(open("./ht2.html"), "html.parser")

aa = soup.findAll('li', {"class": "node scenario fail", "status": "fail"})
number = 0
for each in aa:
    ss = each.findAll('ul', {"class": "steps"})
    for e1 in each.findAll('ul', {"class": "steps"}):
        for e2 in e1.findAll('li', {"status": "fail"}):
            all_pre = e2.findAll('div', {"class": "pre"})
            url = all_pre[1].text.split('Website launched successfully : ')[1]
            worksheet.write(number, 0, datetime.datetime.now().strftime('%x'))
            worksheet.write(number, 1, url)
            for e3 in all_pre[3:len(all_pre) - 2]:
                error_url = e3.text.split(' URL belongs to another domain')[0]
                worksheet.write(number, 2, error_url)
                number = number + 1

workbook.close()
