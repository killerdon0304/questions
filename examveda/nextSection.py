
def find_next_section(soup):
    # print('find next section')
    active = soup.select_one('.chapter-section a.active')

    if active:
        next_a = active.find_next_sibling('a')
        if next_a:
            # print(next_a.get('href'), next_a.text)
            return next_a.get('href')

