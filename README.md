<h1>Acebook</h1>

<h3>Краткие сведения о возможностях сервера</h3>

***Предметная область:** Платформа для написания и публикации статей.*

***Задача:** Реализовать сервер backend для платформы*

1) Сервер обеспечивает регистрацию и авторизацию пользователей.

2) Сервер поддерживает разграничение пользователей по ролям: Администратор, Модератор, Писатель, Читатель (прим.  Не зарегистрированный пользователь не имеет доступа к системе).

3) Статья может находиться в следющих состояниях: Черновик, Опубликована, Одобрена, Отклонена.

4) У одной статьи может быть несколько авторов и редакторов.

5) У одного пользователя может быть несколько ролей.

6) Сервер поддерживает процесс редактирования статьи в состоянии Черновик.

7) Существует возможность блокировки пользователей.

8) Статья, находящаяся в состоянии Одобрена, не может редактироваться, однако её автор может убрать её в черновик.

**Дополнительные возможности сервера:**

1) Сервер поддерживает оценки статей.

2) Сервер предоставляет информацию о новых одобренных статьях. 

3) Сервер поддерживает поиск статей по оценкам читателей, по количеству читателей, по названию, по содержимому, по ключевым словам, по авторам, по дате публикации.

4) Статьи группируются по секциям.

---

### Как запустить проект

1) Выполните команду `git clone https://github.com/Vamprsii/Acebook.git` в терминале вашего устройства.

2) Войдите в нужную директорию использовав команду `cd Acebook`.

3) Поднимите нужные докер контейнеры с помощбю команды `docker-compose up -d --build`.

4) Перейдите по данной ссылке через ваш браузер [localhost:8000](http://localhost:8000/docs).

