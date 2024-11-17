# Данный python-скрипт имитирует запрос к БД
# Напишите ваш SQL-запрос в query и запустите данный python-скрипт для получения результата
# Перед запуском скрипта установите библиотеку duckdb

# Установка библиотеки duckdb
# pip install duckdb duckdb-engine

# Импорт библиотек
import pandas as pd
import duckdb
import os
print(os.getcwd())

# Задание таблиц БД
users = pd.read_csv('users.csv')
course_users = pd.read_csv('course_users.csv')
courses = pd.read_csv('courses.csv')
course_types = pd.read_csv('course_types.csv')
lessons = pd.read_csv('lessons.csv')
subjects = pd.read_csv('subjects.csv')
cities = pd.read_csv('cities.csv')
homework_done = pd.read_csv('homework_done.csv')
homework = pd.read_csv('homework.csv')
homework_lessons = pd.read_csv('homework_lessons.csv')
lessons = pd.read_csv('lessons.csv') 

# Задание SQL-запроса

query = """

SELECT
    course_users.course_id,
    courses.name AS course_name,
    subjects.name AS subject,
    course_types.name AS course_type,
    courses.starts_at,
    users.id AS user_id,
    users.last_name,
    cities.name AS city,
    course_users.active AS is_enrolled,
    course_users.created_at,
    EXTRACT(MONTH FROM AGE(CURRENT_DATE, course_users.created_at)) AS open_months_count, -- Количество месяцев
    COUNT(hd.id) AS homework_completed -- Количество сданных ДЗ на курсе

FROM 
    course_users
JOIN 
    users ON course_users.user_id = users.id
JOIN 
    courses ON course_users.course_id = courses.id
JOIN 
    course_types ON courses.course_type_id = course_types.id
JOIN 
    subjects ON courses.subject_id = subjects.id
JOIN 
    cities ON users.city_id = cities.id
LEFT JOIN 
    homework_done AS hd ON hd.user_id = course_users.user_id

WHERE
	subjects.project = 'ОГЭ' or subjects.project ='ЕГЭ'
    AND course_users.active = TRUE
	AND course_types.name = 'Годовой'
GROUP BY 
    course_users.course_id, courses.name, subjects.name, course_types.name, 
    courses.starts_at, users.id, users.last_name, cities.name, course_users.active, 
    course_users.created_at;
"""


# Выполнение SQL-запроса
df_result = duckdb.query(query).to_df()


# Вывод результата
print(df_result)


