

from bs4 import BeautifulSoup


def parse_page(html):
    soup = BeautifulSoup(html, 'html.parser')

    questions = []
    abc = 0
    for question_div in soup.find_all("article",
                                      {"class": "question-type-normal"
                                       }):  # Adjust class name as per the site
        question_text = ''
        # question_text = question_div.p.b.text.strip()  # Adjust class name
        if question_div.find(class_="question-main"):
            question_text = question_div.find(
                class_="question-main").text.strip()
        ##options here
        options = []
        for option in question_div.find_all(
                class_='question-options'):  # Adjust class name
            for ptag in option.find_all('p'):
                # options.append(option.p.find_all('label')[1].text.strip())
                if ptag.find('label'):
                    finalOption = ptag.find_all('label')[1].text.strip()
                    if finalOption != "":
                        options.append(finalOption)


        ##correct answer here
        correct_answer = ''
        note = ''
        if question_div.find(class_='answer_container'):
            Answer_section = question_div.find(class_='answer_container').find(
                "div", {
                    "class": 'page-content'
                }).find_all('div')
            correct_answer = Answer_section[1].strong.text[7:].strip().lower()  # Adjust class name
            note = Answer_section[2].text.strip().replace('Solution:',
                                                          '').strip()

        if question_text:
            questions.append({
                'question': question_text,
                'options': options,
                'correct_answer': correct_answer,
                'note': note if note else ""  #note
            })

    return questions