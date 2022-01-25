# yamdb_final
yamdb_final
# Автор
Влад Татаринов

# О чем проект
Данный проект представляет из себя копию проекта YaMDb(api_yamdb) упакованую в контенеры Docker и использованием технологии Continious Integration(CI) с помощью инструмента GitHub Actions.
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). 
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

# Как развернуть проект локально
Для разворачивания проекта необходимо зайти в директорию infra и выполнить команду docker-compose up --build.
После запуска данной команды будут собраны необходимые образы и запустятся 3 взаимосвязанных контейнера.
После этого необходимо выполнить 3 последовательные команды:
docker-compose exec web python manage.py migrate # Выполнить миграции
docker-compose exec web python manage.py createsuperuser # Создать суперпользователя
docker-compose exec web python manage.py collectstatic --no-input # Собрать статические файлы в одну папку
проект будет доступен по адресу http://localhost.

# Доступ к проекту на удаленном сервере.
Данный проект развернут на удаленном сервере и доступен по адрессу http://62.84.118.133

# Бейдж о статусе работы в Workflow.
![example workflow](https://github.com/oilman23/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
