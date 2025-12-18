
from bs4 import BeautifulSoup
from saveJSON import save_questions_to_json
from getPage import get_page
from nextSection import find_next_section
from nextPage import find_next_page
from parsePage import parse_page


def scrap_question(soup = None, url =None):
    
    all_questions = []
    name = None   # <-- yahan store hoga
    folder = None
    print(soup)
    if soup:
        path = soup.select('span[itemprop="itemListElement"]')
        name = path[2].text.strip()
        folder = path[1].text.strip()
        questions = parse_page(soup)
        all_questions.extend(questions)

        url = find_next_page(soup)
    print('page', url)
    while url:
        html = get_page(url)
        if not html:
            print('no next url')
            break

        # print('scrape while loop')
        soup = BeautifulSoup(html, 'html.parser')
        if name is None:
            path = soup.select('span[itemprop="itemListElement"]')
            name = path[2].text.strip()
            folder = path[1].text.strip()
        questions = parse_page(html)
        all_questions.extend(questions)
        url = find_next_page(soup)
        print('page loop', url)

        if url is None:
            url = find_next_section(soup)
            print('section', url)

    save_questions_to_json(questions=questions,category=folder,name= name)