import json
from abc import ABC, abstractmethod


class WorkingSaver(ABC):
    """
    Абстрактный класс для сохранения данных в файл
    """

    @abstractmethod
    def get_vacancies_from_salary(self, value):
        pass

    @abstractmethod
    def delete_vacancy(self, value):
        pass


class JSONSaver(WorkingSaver):
    """
    Класс для сохранения вакансий в json файл
    """

    def __init__(self, vacancies: list):
        """
        Инициализация класса JSONWorking
        :param vacancies: объекты класса Vacancy
        """
        self.vacancies = vacancies
        # for i in self.vacancies:
        with open('vacancies.json', 'w', encoding='utf-8') as file:
            json.dump(self.vacancies, file, ensure_ascii=False)

        # vacancies_json = json.dumps(self.vacancies)

    def get_vacancies_from_salary(self, value: str):
        """
        Метод для получения данных из файла по зарплате
        :return:
        """
        need_vacancy = []
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        for i in data:
            if i['salary'] == 'По договоренности':
                continue
            if int(i.get('salary')) >= int(value):
                need_vacancy.append(i)
        numer_count = 0
        for vacancy in need_vacancy:
            numer_count += 1
            print(f'Вакансия №{numer_count}:{vacancy["name"]}, {vacancy["url"]}, {vacancy["salary"]},'
                  f'{vacancy["experience"]}, {vacancy["requirement_and_responsibility"]}')

    def delete_vacancy(self, value: str):
        """
        Метод для удаления вакансий из json_файла
        :param value: Полученное от пользователя название вакансии
        :return:
        """
        with open('vacancies.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for i in data:
                if i.get('name') == value:
                    del i
            with open('vacancies.json', 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
