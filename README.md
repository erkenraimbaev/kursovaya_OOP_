# kursovaya_OOP_
Проект для поиска вакансий с различных сайтов
Эта программа поможет найти информацию с сайтов по поиску работы.

Программа поддерживает поиск по ключевому слову (название профессии), а также выбор города.

На данный момент программе доступно использование сайтов HeadHunter и SuperJob (можно расширить в будущем).


Прграмма выполняет следующие шаги:
Введение ключевого слова пользователя - По нему будет поиск вакансий.
Введение региона поиска - Город в котором вы хотели бы посмотреть вакансии (Россия).
Введение количества вакансий - Число вакансий выводимых пользователю на экран.
Необходимо выбрать источник поиска информации

После выполнения всех пунктов в консоль будет выведен пронумерованный список вакансий.
Будет предложено отфильтровать вакансии по минимуму зарплаты и удалить не нужные по названию.

Также в папке проекта будет создан файл vacancies.json со структурой:
[
{
"name": "название",
"url": "ссылка",
"salary": "зарплата_до",
"experience": "опыт",
"requirement_and_responsibility": "требования_и_обязаности"
},
]
В следующие запуски файл будет переписываться.
