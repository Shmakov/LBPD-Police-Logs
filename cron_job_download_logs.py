import lxml.html
import datetime
import urllib.request
import requests
import os.path

website_url = 'http://www.lagunabeachcity.net'
daily_police_log_page = '/cityhall/police/daily_police_log.htm'

pdf_logs_path = os.path.dirname(os.path.realpath(__file__)) + "/pdf_logs/"

replace_mapping = {', ': ' ', ',': ' ', '  ': ' ', '-': ''}

page = requests.get(website_url + daily_police_log_page)
doc = lxml.html.fromstring(page.content)

for a_tag in doc.cssselect('div.fb-node-contents a'):
    row_text = a_tag.text
    for k, v in replace_mapping.items():
        row_text = row_text.replace(k, v)
    s = row_text.split(' ')
    d = datetime.datetime.strptime(s[-3] + ' ' + s[-2] + ' ' + s[-1], '%B %d %Y')
    file_name = pdf_logs_path + str(d.year) + '_' + str(d.month) + '_' + str(d.day) + '.pdf'
    if not os.path.isfile(file_name):
        urllib.request.urlretrieve(website_url + a_tag.attrib['href'], file_name)
        print(file_name)