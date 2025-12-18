from bs4 import BeautifulSoup
from scrapQuestion import scrap_question
from saveJSON import save_questions_to_json
from getPage import get_page

def scrap_articles(soup):
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
    save_questions_to_json(questions=articles_data, category=category)

    for article in articles_data:
        print(article["title"])
        scrap_question(url = article["url"])
        



if __name__ == '__main__':
    url =''
    start_url = url  # Replace with the starting URL of the quiz site
    
