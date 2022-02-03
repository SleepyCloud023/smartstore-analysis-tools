import requests
from bs4 import BeautifulSoup
import re

DEBUG_MODE = False

# return values: 썸네일이미지 url, 판매 페이지 url
def get_data_image_area(image_area_div):
    thumbnail_image_url = ''
    salepage_url = image_area_div.find('a', {'class': re.compile('^thumbnail_thumb')})['href']
    try:
        thumbnail_image_url = image_area_div.find('image')['src']
    except:
        if DEBUG_MODE:
            print(f'fail to gather thumbnail image data, selenium webdriver enviroment is needed')
    return {
        'thumbnail_url': thumbnail_image_url, 
        'salepage_url': salepage_url
    }

def get_data_info_area(image_area_div):
    title_div, price_div, depth_div, desc_div, etc_div = image_area_div.find_all('div', recursive=False)
    title = title_div.find('a')['title']
    price = price_div.find('span', {'class': re.compile('^price_num')}).text
    category_texts = list(map(lambda span: span.text, depth_div.find_all('span')))
    category =  '>'.join(category_texts)
    detail_contents = list(map(lambda a: a.text,
                            desc_div.find_all('a', {'class': re.compile('^basicList_detail')})))
    detail = ' | '.join(detail_contents)
    # TODO: 리뷰수, 구매건수, 등록일, 찜하기 수
    # etc_div 처리 

    return {
        'title': title,
        'price': price,
        'category': category,
        'detail': detail,
    }

def extract_sections(li_element):
    basicList_inner = li_element.find('div', recursive=False)
    image_area, info_area, mall_area = basicList_inner.find_all('div', recursive=False)
    return {'image': image_area, 'info': info_area, 'mall': mall_area}

def extract_data_from_li(li_element):
    sections = extract_sections(li_element)
    data_image_section = get_data_image_area(sections['image'])
    data_info_section = get_data_info_area(sections['info'])

    return {**data_image_section, **data_info_section}

def get_items_from_url(url):
    origin_html = requests.get(url).content
    soup = BeautifulSoup(origin_html, 'html.parser')
    ul_list_basis = soup.find('ul', {"class": "list_basis"})
    li_basicList_item = ul_list_basis.find_all('li', {"class": re.compile('^basicList_item')})
    sectioned_items = list(map(extract_data_from_li, li_basicList_item))
    return sectioned_items

def save_data_from_url(url, filename):
    data = get_items_from_url(url)
    columns = ['id', '상품명', '가격', '카테고리', '이미지', '링크']
    with open(filename, 'w') as fp:
        fp.write(','.join(columns) + '\n')
        # TODO: 컬럼명, 데이터 정리해서 채우기

# url_1인야채_추천순 = "https://search.shopping.naver.com/search/all?catId=50000160&frm=NVSHCAT&origQuery=1%EC%9D%B8%20%EC%95%BC%EC%B1%84&pagingIndex=1&pagingSize=40&productSet=total&query=1%EC%9D%B8%20%EC%95%BC%EC%B1%84&sort=review&timestamp=&viewType=list"
# items = get_items_from_url(url_1인야채_추천순)

