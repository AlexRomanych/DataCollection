# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient(host='localhost', port=27017)
        self.mongo_base = client.vacancies_271124

    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]

        vacancy_item = {
            '_id': item.get('_id'),
            'vacancy': parce_vacancy(item.get('name')),
            'salary': parse_salary(item.get('salary')),
            'experience': item.get('experience'),
            'condition': parse_condition(item.get('condition')),
            'description': parse_description(item.get('description')),
            'url': item.get('url'),
            'company': {
                'name': parse_company_name(item.get('company_name')),
                'location': parse_company_location(item.get('company_location')),
            }
        }

        collection.insert_one(vacancy_item)

        return item


def parce_vacancy(vacancy):
    return ' '.join(vacancy).replace(' ,', ',').replace('  ', ' ').strip()


def parse_condition(condition):
    if len(condition) == 0:
        return "Не указано"
    return ' '.join(condition).replace(' ,', ',').replace('  ', ' ').strip()


def parse_company_name(company_name):
    if len(company_name) == 0:
        return 'Не указана'
    if len(company_name) == 1:
        return company_name[0]
    if company_name[0] == company_name[1]:
        return company_name[0]
    return company_name[0] + ' ' + company_name[1]


def parse_company_location(company_location):
    return ' '.join(company_location).replace(' ,', ',').replace('  ', ' ').strip()


def parse_description(company_description):
    description_str = ''
    for str_line in company_description:
        if str_line != ' ':
            description_str += str_line + ' '
    return description_str.replace(' ,', ',').replace('  ', ' ').strip()


def parse_salary(salary):
    # return salary
    if len(salary) == 0:
        return "Не указана"

    min_salary = 0
    max_salary = 0
    salary_condition = ''
    salary_currency = ''

    black_list = ['от', 'до', '', '-']

    for str_salary in salary:

        digits_text = get_digits_part(str_salary)

        if digits_text.isdigit():
            if min_salary == 0:
                min_salary = int(digits_text)
            else:
                max_salary = int(digits_text)

        else:
            if not str_salary.strip().lower() in black_list:
                if "налог" in str_salary.lower() or "руки" in str_salary.lower():
                    salary_condition = str_salary.lower().strip()
                else:
                    salary_currency = str_salary.lower().strip()

    salary_obj = {}

    if min_salary != 0:
        salary_obj['min'] = min_salary

    if max_salary != 0:
        salary_obj['max'] = max_salary

    if salary_condition:
        salary_obj['condition'] = salary_condition

    currency = 'руб.'
    if salary_currency:
        if salary_currency == '$':
            currency = 'доллар'
        else:
            if salary_currency == '€':
                currency = 'евро'

        salary_obj['currency'] = currency

    return salary_obj


def get_digits_part(text):
    digits_text = ''
    for char in text:
        if char.isdigit():
            digits_text += char
    return digits_text

