SELECT
	-- Выбираем небходимые столбцы:
    course_users.course_id, -- ID курса, на который записан пользователь
    courses.name AS course_name, -- Название курса
    subjects.name AS subject, -- Название предмета
    course_types.name AS course_type, -- Тип курса (например, "Годовой")
    courses.starts_at, -- Дата начала курса
    users.id AS user_id, -- ID пользователя
    users.last_name, -- Фамилия пользователя
    cities.name AS city, -- Город, в котором находится пользователь
    course_users.active AS is_enrolled, -- Флаг, показывающий, активен ли пользователь на курсе
    course_users.created_at, -- Дата записи пользователя на курс
    EXTRACT(MONTH FROM AGE(CURRENT_DATE, course_users.created_at)) AS open_months_count, -- Количество месяцев, в течение которых пользователь записан на курс
    COUNT(hd.id) AS homework_completed -- Количество выполненных домашних заданий для данного пользователя на курсе

FROM 
    course_users --основная таблица
JOIN 
    users ON course_users.user_id = users.id -- Присоединяем таблицу пользователей по ID пользователя
JOIN 
    courses ON course_users.course_id = courses.id -- Присоединяем таблицу курсов по ID курса
JOIN 
    course_types ON courses.course_type_id = course_types.id -- Присоединяем таблицу типов курсов по типу курса
JOIN 
    subjects ON courses.subject_id = subjects.id -- Присоединяем таблицу предметов по ID предмета курса
JOIN 
    cities ON users.city_id = cities.id -- Присоединяем таблицу городов по ID города пользователя
LEFT JOIN 
    homework_done AS hd ON hd.user_id = course_users.user_id -- Левое соединение с таблицей выполненных домашних заданий по ID пользователя

WHERE
	-- Фильтруем по нужным условиям:
	subjects.project = 'ОГЭ' or subjects.project ='ЕГЭ' -- Условие, чтобы проект был либо "ОГЭ", либо "ЕГЭ"
    AND course_users.active = TRUE -- Условие, чтобы пользователь был активен на курсе
	AND course_types.name = 'Годовой' -- Условие, чтобы тип курса был "Годовой"
GROUP BY 
	-- Группируем по столбцам для финальной таблицы:
    course_users.course_id, courses.name, subjects.name, course_types.name, 
    courses.starts_at, users.id, users.last_name, cities.name, course_users.active, 
    course_users.created_at;
