# Web-приложение для планирования целей

### Запуск приложения

    docker-compose up --build

## Функционал:

### 1. Вход/регистрация/аутентификация через вк.

![auth](https://github.com/gmoroz/todolist/blob/master/readme_files/auth.gif)

### 2. Создание целей.

1.  Выбор временного интервала цели с отображением кол-ва дней до завершения цели.
2.  Выбор категории цели (личные, работа, развитие, спорт и т. п.) с возможностью добавлять/удалять/обновлять категории.
3.  Выбор приоритета цели (низкий/средний/выскокий/критический).
4.  Выбор статуса выполнения цели (в работе, выполнен, просрочен, в архиве).

![goal create](https://github.com/gmoroz/todolist/blob/master/readme_files/goal_create.gif)

![add category](https://github.com/gmoroz/todolist/blob/master/readme_files/add_category.gif)

### 3. Изменение целей.

1.  Изменение описания цели.
2.  Изменение статуса.
3.  Возможность менять приоритет и категорию у цели.

![goal update](https://github.com/gmoroz/todolist/blob/master/readme_files/goal_update.gif)

### 4. Удаление цели, категории.

![delete category or goal](https://github.com/gmoroz/todolist/blob/master/readme_files/delete_cat_goal.gif)

5.  Поиск по названию цели.
6.  Фильтрация по статусу, категории, приоритету, году.
7.  Комментарии к целям.
