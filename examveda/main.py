from bs4 import BeautifulSoup
import csv

from saveJSON import save_questions_to_json
from nextSection import find_next_section
from getPage import get_page
from nextPage import find_next_page
from parsePage import parse_page
# from translateHindi import translate_questions_to_hindi, save_to_csv_hindi

url = 'https://www.examveda.com/general-knowledge/practice-mcq-question-on-indian-politics/'
category = 1
subcategory = 6
language_id = 14  # 14 for english ur 22 for hindi
level = 1

def scrape_site(start_url):
    url = start_url
    all_questions = []
    page_title = None   # <-- yahan store hoga
    folder = None

    while url:
        html = get_page(url)
        if not html:
            print('no next url')
            break

        # print('scrape while loop')
        soup = BeautifulSoup(html, 'html.parser')

        # 🔹 Title sirf ek baar scrape hoga
        if page_title is None:
            path = soup.select('span[itemprop="itemListElement"]')
            page_title = path[2].text.strip()
            folder = path[1].text.strip()

        questions = parse_page(html)
        all_questions.extend(questions)

        url = find_next_page(soup)
        # print('page', url)

        if url is None:
            url = find_next_section(soup)
        #     print('section', url)

    return all_questions, page_title, folder

def scrap_category():
    url = 'https://www.examveda.com/mcq-question-on-history/'

    html = get_page(url)
    if not html:
        print('no next url')

    soup = BeautifulSoup(html, 'html.parser')
    articles_data = []

    articles = soup.select('div.page-content article h3 a')
    for a in articles:
        text = a.get_text(strip=True)
        link = a.get('href')

        articles_data.append({
            "title": text,
            "url": link
        })
    # print(articles_data)
    category = soup.select('span[itemprop="itemListElement"]')[1].text.strip()
    save_questions_to_json(articles_data, category)

    for article in articles_data:
        print(article["title"])
        questions, name, category = scrape_site(article["url"])
        save_questions_to_json(questions, category, name)



if __name__ == '__main__':
    start_url = url  # Replace with the starting URL of the quiz site
    # scrap_category()
    questions, name, category = scrape_site(start_url)
    save_questions_to_json(questions, category, name)
    # save_to_csv(all_questions, 'questions.csv')

    # Hindi translate + save
    # hindi_questions = translate_questions_to_hindi(all_questions)
    # save_to_csv_hindi(hindi_questions, 'questions_hi.csv',category,subcategory,level)
