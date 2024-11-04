import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from pprint import pprint
import re

final_list = []
page_list = []


LINK= "https://spb.hh.ru" # соединение
PARAMS = {
    "area":["1", "2"], # Код региона по ISO 3166-1 alpha-2, для Москвы - 1, для Питера - 2
    "search_field":["name", "company_name", "description"], # Поиск в названии вакансии, названии компании, описании вакансии
    "enable_snippets":"true",
    "text":"Python"+"django"+"flask", # Поиск по ключевым словам
    "ored_clusters":"true",
    "items_on_page":"30", # Количество объявлений на странице
    "page":"0" # Номер страницы с объявлениями
}        
VACANCIES = f"{LINK}/search/vacancy"
HEADERS = Headers(browser="chrome", os="win").generate()

bannedWord = ['\xa0','\u202f']


#print(blocks)
page = 0
i = 0
while True:
    try:
        response = requests.get(VACANCIES, params=PARAMS, headers=HEADERS).text # записываем данные страницы в переменную ввиде текста
        response2 = requests.get(VACANCIES, params=PARAMS, headers=HEADERS)
        #print(response2.url)
        #print(response2.status_code)
        soup = BeautifulSoup(response, "lxml") 
        blocks = soup.findAll("div", class_ = "magritte-redesign")
        for block in blocks:

            #ищем название вакансии, ссылку и зарплату

            check_title = block.find("div", class_ = "vacancy-info--umZA61PpMY07JVJtomBA") 
            title = check_title.find("span",class_ ="magritte-text___pbpft_3-0-16 magritte-text_style-primary___AQ7MW_3-0-16 magritte-text_typography-title-4-semibold___vUqki_3-0-16").text
            get_ref = block.find("a", class_ = "magritte-link___b4rEM_4-3-9 magritte-link_style_neutral___iqoW0_4-3-9 magritte-link_enable-visited___Biyib_4-3-9", href=True)['href']
            #print(f'Вакансия {title}, ссылка {get_ref}',"\n")

            #поиск города
            city_check = block.find ("div", class_ = "info-section--Sy92rBBHNWJWHqwO3sl2")
            city_list = city_check.find_all("span", class_ = "magritte-text___pbpft_3-0-16 magritte-text_style-primary___AQ7MW_3-0-16 magritte-text_typography-label-3-regular___Nhtlp_3-0-16")
            for elem in city_list:
                if elem.get("data-qa") == "vacancy-serp__vacancy-address":
                    city = elem.text
                else:
                    continue 
            #print(employer_el,"\n")
            #print(f"Город: {city}\n")

            #поиск зарплаты
            salary_check = block.find("div", class_ = "vacancy-info--umZA61PpMY07JVJtomBA")
            salary = salary_check.find("span", class_ ="magritte-text___pbpft_3-0-16 magritte-text_style-primary___AQ7MW_3-0-16 magritte-text_typography-label-1-regular___pi3R-_3-0-16")
            if salary != None:
                salary_el = ' '.join(a for a in str(salary.text).split() if a not in bannedWord)
                
            else:
                salary_el = "В карточке не указана зарплата =("
            #print(f'Зарплата: {salary_el}\n')

            # поиск работодателя 
            employer_check = block.find("div", class_ = "info-section--Sy92rBBHNWJWHqwO3sl2")
            employer_next = employer_check.find("a", class_ = "magritte-link___b4rEM_4-3-9 magritte-link_style_neutral___iqoW0_4-3-9")
            employer = employer_next.find_all("span", class_ ="magritte-text___tkzIl_4-3-9")
            for el in employer:
                if el.attrs['data-qa'] == "vacancy-serp__vacancy-employer-text":
                    employer_el = el.text
                    #print(f'Работодатель: {employer_el}\n')
                else:
                    employer_el = "В карточке не указан работодатель =("
                    #print(employer_el,"\n")

            finall_dict = {
            "Вакансия":title,
            "Зарплата":salary_el,
            "Работодатель":employer_el,
            "Город": city,
            "Ссылка":get_ref
            }
            final_list.append(finall_dict)        
            


            
            i += 1
            #print(i)            
            #print(page)
            if blocks.index(block) == len(blocks)-1:                
                page +=1
                PARAMS["page"] = page
               
    except AttributeError:
        print(f"\nПросмотрены все страницы!")
        break   
            

       
pprint(final_list)