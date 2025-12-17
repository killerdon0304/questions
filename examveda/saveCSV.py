import csv

def save_to_csv(questions, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            'category', 'subcategory', 'language_id', 'question_type',
            'Question', 'Option 1', 'Option 2', 'Option 3', 'Option 4',
            'Option 5', 'answer', 'level', 'note'
        ])  # Adjust the headers as necessary

        for index, question in enumerate(questions):
            current_level = (index // 25) + level
            # print(len(question['options']))
            if len(question['options']) == 4:
                row = [category] + [subcategory] + [language_id] + [1] + [
                    question['question']
                ] + question['options'] + [''] + [
                    question['correct_answer']
                ] + [current_level] + [question['note']]
                writer.writerow(row)
            else:
                row = [category] + [subcategory] + [language_id] + [1] + [
                    question['question']
                ] + question['options'] + [question['correct_answer']] + [
                    current_level
                ] + [question['note']]
                writer.writerow(row)