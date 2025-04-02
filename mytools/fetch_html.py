# -*- encoding: utf-8 -*-
'''
@Time    :   2025/02/14 01:01:35
@Author  :   47bwy
@Desc    :   None
'''


import requests
from bs4 import BeautifulSoup


class FetchHtml:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        response = requests.get(self.url)
        response = requests.get(url)
        html_content = response.text
        return html_content

    def get_soup(self):
        # 解析网页
        return BeautifulSoup(self.get_html(), 'lxml')
    


url = ""
obj = FetchHtml(url)
soup = obj.get_soup()
a_tag = soup.find_all('a')
for a in a_tag:
    if "chapter" in a['href']:
        print(a['href'])
# print(a_tag)
# print(soup.prettify())
