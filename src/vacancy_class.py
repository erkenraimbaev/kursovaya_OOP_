class Vacancy:
    """
    Класс для создания обънетов вакансий по параметрам пользователя
    """
    def __init__(self, name, url, salary, experience, requirement_and_responsibility):
        self.__name = name
        self.__url = url
        self.__salary = salary
        self.__experience = experience
        self.__requirement_and_responsibility = requirement_and_responsibility

    def name(self):
        return self.__name

    def url(self):
        return self.__url

    def salary(self):
        return self.__salary

    def experience(self):
        return self.__experience

    def requirement_and_responsibility(self):
        return self.__requirement_and_responsibility

    def __str__(self):
        """
        Магический метод для отображения удобочитаемой строки
        :return:
        """
        return f"{self.__name}, {self.__url}, Зарплата: {self.__salary}, Опыт: {self.__experience}, " \
               f"{self.__requirement_and_responsibility}"

    def __dict__(self):
        vacancy_dict = {'name': self.__name,
                        'url': self.__url,
                        'salary': self.__salary,
                        'experience': self.__experience,
                        'requirement_and_responsibility': self.__requirement_and_responsibility}
        return vacancy_dict

    def __gt__(self, other):
        """
        Метод срабатывает, когда используется оператор >.
        В параметре other хранится то, что справа от знака +
        """
        return self.__salary > other.__salary

    def __lt__(self, other):
        """
        Метод срабатывает, когда используется оператор <.
        В параметре other хранится то, что справа от знака +
        """
        return self.__salary < other.__salary

    def __eq__(self, other):
        """
        Метод срабатывает, когда используется оператор ==.
        В параметре other хранится то, что справа от знака +
        """
        return self.__salary == other.__salary
