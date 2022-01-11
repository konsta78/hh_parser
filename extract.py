import requests
from bs4 import BeautifulSoup


HEADERS = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)' +
                      'Chrome/96.0.4664.45 Safari/537.36'
    }
ITEMS = 20


def extract_max_page(url):
    """
    Находит в тексте запарсенной ссылки максимальное кол-во сгенерированных страниц с вакансиями
    :return: максимальный номер страницы
    """
    hh_request = requests.get(url, headers=HEADERS)
    hh_soup = BeautifulSoup(hh_request.text, 'html.parser')
    #Находим все ссылки в пагинаторе
    paginator = hh_soup.find_all('a', {'data-qa': 'pager-page'})
    pages = []
    for i in paginator:
       pages.append(int(i.text)) #Забираем текст ссылки
    return pages[-1] if pages else 0#Максимальное число страниц с вакансиями


def extract_vacancy(vacancy):
    """
    Возвращает описание очередной вакансии
    :param vacancy: html-текст с описанием вакансии
    :return: словарь с описанием вакансии по ключам:
    'title' - название вакансии
    'company' - наименование работодателя
    'city' - местонахождение вакансии
    'link' - ссылка на подробное описание вакансии
    """
    name_vacancy = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
    title_vacancy = name_vacancy.text
    link_vacancy = name_vacancy['href']
    company_vacancy = vacancy.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).text
    city_vacancy = str(vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text).split(',')[0]
    return {'title': title_vacancy,
            'company': company_vacancy.replace(u'\xa0', ' '),
            'city': city_vacancy,
            'link': link_vacancy}


def extract_jobs(last_page, url):
    """
    Возвращает результат поиска по всем вакансиям на всех страницах
    :param last_page: максимальное число страниц с вакансиями
    :return: список словарей с описанием вакансии
    """
    jobs = []
    for page in range(last_page):
        result = requests.get(f'{url}&page={page}', headers=HEADERS)
        page_soup = BeautifulSoup(result.text, 'html.parser')
        vacancies = page_soup.find_all('div', {'class': 'vacancy-serp-item'})
        for vacancy in vacancies:
            jobs.append(extract_vacancy(vacancy))
    return jobs


def get_all_jobs(inquiry):
    """
    Возвращает список вакансий по уникльному запросу
    :param inquiry: текст запроса
    :return: список словарей с описанием вакансии по уникальному запросу
    """
    inquiry = inquiry.replace(' ', '+')
    # Упростим запрос и уберем лишние параметры
    url = f'https://spb.hh.ru/search/vacancy?text={inquiry}&area=2&items_on_page={ITEMS}'
    last_page = extract_max_page(url)
    return extract_jobs(last_page, url)