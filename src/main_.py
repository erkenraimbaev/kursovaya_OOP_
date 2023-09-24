import json
from abc import ABC, abstractmethod
from vacancy_class import Vacancy
from json_saver_class import JSONSaver
import requests


class WorkingByAPI(ABC):
    """
    Абстрактный класс для работы с API сайтов
    """

    def __init__(self, params: dict):
        """
        Инициализация класса WorkingByAPI
        """
        self.params = params
        self.vacancy_data = self.get_vacancies()

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def filtered_vacancies(self):
        pass


class WorkingWithHeadHunter(WorkingByAPI):
    """
    Класс для работы с сайтом Headhunter
    """

    def __init__(self, params):
        """
        Инициализация класса
        """
        super().__init__(params)

    def __str__(self):
        """

        :return:
        """
        return f'{self.vacancy_data["name"]}, {self.vacancy_data.get("url")}, {self.vacancy_data.get("salary")},' \
               f'{self.vacancy_data["experience"]}'

    def get_vacancies(self):
        """
        Метод для получения объектов - вакансий с сайта HeadHunter
        :return: objects
        """
        global town_id
        user_area = search_dict['area']
        regions_dict = json.loads(requests.get('https://api.hh.ru/areas').content.decode())[0].get('areas')
        for region in regions_dict:
            for town in region.get('areas'):
                if user_area == town.get('name'):
                    town_id = town.get('id')
        params = {'text': search_dict['text'], 'area': town_id, 'page': 0, 'per_page': search_dict['page']}
        req = requests.get('https://api.hh.ru/vacancies', params=params)
        data = req.content.decode()
        hh_objects = json.loads(data)['items']
        return hh_objects

    def filtered_vacancies(self):
        """
        Метод для фильтрации объектов класса HeadHunter
        :return: list
        """
        filtered_vacancies = []
        for vac in self.vacancy_data:
            name_vacancy = vac.get('name')
            url_vacancy = vac.get('apply_alternate_url')
            if vac.get('salary') is None:
                salary_vacancy = 'По договоренности'
            else:
                salary_vacancy = f'{vac.get("salary").get("from")}'
            experience_vacancy = vac.get('experience').get('name')
            requirement = f"Требования: {vac.get('snippet').get('requirement')}\nОбязаности: " \
                          f"{vac.get('snippet').get('responsibility')}"
            requirement_and_responsibility = requirement.replace('\n', '')
            filtered_vacancy = {'name': name_vacancy,
                                'url': url_vacancy,
                                'salary': salary_vacancy,
                                'experience': experience_vacancy,
                                'requirement_and_responsibility': requirement_and_responsibility}
            filtered_vacancies.append(filtered_vacancy)
        return filtered_vacancies


class WorkingWithSuperJob(WorkingByAPI):
    """
    Класс для работы с сайтом SuperJob
    """

    def __init__(self, params):
        """
        Инициализация класса
        """
        super().__init__(params)

    def get_vacancies(self):
        """
        Метод для получения объектов - вакансий с сайта SuperJob
        :return: objects
        """
        parametres = {'town': search_dict.get('area'), 'catalogues': None, 'count': search_dict.get('page'),
                      'keyword': search_dict.get('text')}
        headers = {'X-Api-App-Id':
                       'v3.r.118672307.f907c53183d14ae792c5787074bc04885977f091.bc367a78bd4c722325f3524849bc575554eaf19f'
                   }
        super_job_objects = (requests.get('https://api.superjob.ru/2.0/vacancies/', params=parametres,
                                          headers=headers)).json()['objects']
        return super_job_objects

    def filtered_vacancies(self):
        """
        Метод для фильтрации объектов класса SuperJob
        :return: list
        """
        filtered_vacancies = []
        for vac in self.vacancy_data:
            name_vacancy = vac.get('profession')
            url_vacancy = vac.get('link')
            if int(vac.get('payment_to')) == 0:
                salary_vacancy = 'По договоренности'
            else:
                salary_vacancy = f'{vac.get("payment_from")}'
            experience_vacancy = vac.get('experience').get('title')
            requirement = vac.get('candidat')
            requirement_and_responsibility = requirement.replace('\n', '')
            filtered_vacancy = {'name': name_vacancy,
                                'url': url_vacancy,
                                'salary': salary_vacancy,
                                'experience': experience_vacancy,
                                'requirement_and_responsibility': requirement_and_responsibility}
            filtered_vacancies.append(filtered_vacancy)
        return filtered_vacancies


def user_interaction():
    """
    Метод для получения от пользователя параметров поиска вакансий
    :return: параметры поиска
    """
    print("Привет, я могу найти подходящие вакансии для вас, отфильтровать их и вывести ТОП вакансий!\n")
    parametres = {}
    filter_word = input('Введите название вакансии для поиска:\n')
    parametres['text'] = filter_word
    user_area = input('Введите нужный вам регион:\n')
    parametres['area'] = user_area.title()
    user_count_page = input('Введите желаемое число вакансий\n')
    parametres['page'] = int(user_count_page)
    return parametres


# Принимаем параметры у пользователя
search_dict = user_interaction()

while True:
    user_site = (input(f'С какого сайта хотите получить вакансии?\n'
                       f'Введите 1 - получить вакансии с HeadHunter\n'
                       f'Введите 2 - получить вакансии с SuperJob\n'
                       f'Введите 3 - получить вакансии с HeadHunter и SuperJob'))
    if int(user_site) not in [1, 2, 3]:
        print('Неправильный ответ! Попробуйте еще раз!')
        continue
    elif user_site == '1':
        hh_api = WorkingWithHeadHunter(search_dict)
        hh_vac = hh_api.filtered_vacancies()
        vacancies_full = hh_vac
        break
    elif user_site == '2':
        super_job_api = WorkingWithSuperJob(search_dict)
        super_job_vac = super_job_api.filtered_vacancies()
        vacancies_full = super_job_vac
        break
    elif user_site == '3':
        # С 2 сайтов вакансий будет вдвое больше
        count_vacancy = search_dict["page"] * 2
        print(f'Будут показаны: {count_vacancy} вакансий с HeadHunter и SuperJob')
        # Создаем объекты - вакансии с сайтов
        hh_api = WorkingWithHeadHunter(search_dict)
        super_job_api = WorkingWithSuperJob(search_dict)
        # Получаем списки вакансий по нужным параметрам
        hh_vac = hh_api.filtered_vacancies()
        super_job_vac = super_job_api.filtered_vacancies()
        # Объединяем списки с разных сайтов
        vacancies_full = hh_vac + super_job_vac
        break


# Создаем список объектов класса Vacancy для дальнейшей работы
vacancies_objects = []
# Заполняем этот список
for vac in vacancies_full:
    vacancy = Vacancy(name=vac['name'], url=vac['url'], salary=vac['salary'], experience=vac['experience'],
                      requirement_and_responsibility=vac['requirement_and_responsibility'])
    vacancies_objects.append(vacancy)
# Сохраняем данные в json файл
json_saver = JSONSaver(vacancies_full)
print('\n')
print(f'Вакансии записаны в файл "vacancies.json"\n')

# Выводим информацию о найденных вакансиях по запросу пользователя
number_count = 0
for i in vacancies_objects:
    number_count += 1
    print(f'Вакансия №{number_count}: {i.__str__()}')
print('\n')
print(f'Вы можете оставить только вакансии с указанной зп а также установить значение '
      f'минимума зарплаты')
print(f'Введите интерсующий вас размер заработной платы')
print(f'Введите 0 - если в этом нет необходимости')
user_salary = input()
if int(user_salary) / 1 != int(user_salary):
    print(f'Некорректный ввод')
elif int(user_salary) == 0:
    print(f'Хорошо')
json_saver.get_vacancies_from_salary(user_salary)

# Узнаем у пользователя нужно ли удалить какую то вакансию из файла? (по названию)
print("\n")
print(f'Если необходимо удалить вакансию из файла:\n'
      f'Введите название вакансии для удаления\n'
      f'Введите 0 если это не требуется')
user_del = input()
if user_del == 0:
    print(f'Работа программы завершена.\n'
          f'В "vacancies.json" вся нужная информация о вакансиях. ')
else:
    json_saver.delete_vacancy(user_del)
    print(f'Работа программы завершена.\n'
          f'В "vacancies.json" вся нужная информация о вакансиях')

# if __name__ == "__main__":
#     user_interaction()
