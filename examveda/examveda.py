
from bs4 import BeautifulSoup
from scrapQuestion import scrap_question
from getPage import get_page
from articles import scrap_articles

def main(url):
    html = get_page(url)
    if not html:
        print('no next url')

    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.select('div.page-content article h3 a')

    scrap_articles(soup) if articles else scrap_question(soup=soup)


if __name__ == '__main__':
    url='https://www.examveda.com/mcq-question-on-physics-gk-chapter-wise/'
    main(url)