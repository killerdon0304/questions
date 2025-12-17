def find_next_page(soup):
    # print('find next page')

    next_page_link = soup.find(class_='pagination')
    if not next_page_link:
        return None  # No pagination on this page

    next_icon = next_page_link.find("i", class_="fa-angle-right")
    if next_icon and next_icon.parent:
        return next_icon.parent.get('href')

    return None
