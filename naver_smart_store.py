import requests
from bs4 import BeautifulSoup
import re

def extract_sections(li_element):
    basicList_inner = li_element.find('div', recursive=False)
    image_area, info_area, mall_area = basicList_inner.find_all('div', recursive=False)
    return {'image': image_area, 'info': info_area, 'mall': mall_area}

def get_items_from_url(url):
    origin_html = requests.get(url).text
    soup = BeautifulSoup(origin_html, 'html.parser')
    ul_list_basis = soup.find('ul', {"class": "list_basis"})
    li_basicList_item = ul_list_basis.find_all('li', {"class": re.compile('^basicList_item')})
    sectioned_items = list(map(extract_sections, li_basicList_item))
    return sectioned_items

def save_data_from_url(url, filename):
    data = get_items_from_url(url)
    columns = ['상품명', '이미지', '가격', '카테고리']
    with open(filename, 'w') as fp:
        fp.write(','.join(columns) + '\n')
        # TODO: 컬럼명, 데이터 정리해서 채우기
