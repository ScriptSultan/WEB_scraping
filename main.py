import json
import requests

from bs4 import BeautifulSoup
from fake_headers import Headers
import re

headers_gen = Headers(os='win', browser='chrome')
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
r = requests.get(url, headers=headers_gen.generate())
r_data = r.text

main_html = BeautifulSoup(r_data, features="lxml")
html_tag_find = main_html.find_all('a', class_='serp-item__title') # нашел всё заголовки на странице

for hrefs in html_tag_find:

    hrefs_find = hrefs['href']  # получил ссылки какждой вакансии
    req_to_link = requests.get(hrefs_find, headers=headers_gen.generate()).text # перешел по ссылке каждой вакансии
    main_link_info = BeautifulSoup(req_to_link, features="lxml")
    tag_description = main_link_info.find('div', class_='g-user-content')  #нашел описание каждой вакансии
    data = {}
    # нашел все вакансии по ключевым словам в описании
    if "django" in str(tag_description).lower() or 'flask' in str(tag_description).lower():
        data['link'] = hrefs_find

        #Нахожу вилку зп
        zp_tag = main_link_info.find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text #находится в этом теге
        zp_pattern_1 = r"(\D+)[0]"
        zp = re.sub(zp_pattern_1, '0', zp_tag)
        zp_pattern_2 = r"(\D+)"
        zp = re.sub(zp_pattern_2,  ' ', zp)
        data['salary'] = zp

        try:
            tag_description_town = main_link_info.find('a', class_='bloko-link bloko-link_kind-tertiary bloko-link_disable-visited').text.split(',')[0]
            data['town'] = tag_description_town
        except AttributeError:
            town = 'Нет города'
            data['town'] = town

        #Нахожу название компании
        name_company = main_link_info.find_all('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
        name_company_1 = name_company[len(name_company)-1].text
        name_pattern = r"(\W+)"
        name = re.sub(name_pattern,  ' ', name_company_1)
        data['name'] = name
        with open('data_vacancy.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)