# Полный сценарий занятия по теме «Django ORM и Базы Данных»

Этот сценарий содержит готовые реплики для преподавателя (выделены курсивом и оформлены в блоки цитат) и код, который нужно показывать на проекторе или писать вместе с учениками.

---

## Введение: Ставим проблему (5-10 минут)

**Преподаватель:**
> *«Ребята, привет! На прошлых занятиях мы с вами создали сайт Кванта с главной страницей, списком преподавателей и описанием курсов. Всё работает, но у нашей текущей реализации есть одна огромная скрытая проблема.*
> 
> *Давайте откроем файл `main/views.py` и посмотрим на него внимательно.»*

**(Покажите на проекторе файл [main/views.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/views.py)):**

```python
COURSES = {
    "Python": "Здесь изучаем питон",
    "plusy": "Здесь изучаем плюсы",
    "Super_course": "Здесь изучаем что такое супер",
    "Tatar_language": "учим татарский"
}

TEACHER = [
    {
        'name': 'raushan',
        'age': 20,
        'course': 'web'
    },
    {
        'name': 'ishkhan',
        'age': 20,
        'course': 'web'
    }
]
```

**Преподаватель:**
> *«Посмотрите на списки `COURSES` и `TEACHER`. Они написаны прямо внутри Python-кода.*
> 
> *Представьте, что к нам в лагерь приехал новый преподаватель или мы хотим добавить новый крутой курс. Что нам придется сделать? Нам придется лезть руками в код, дописывать словари, коммитить в Git и перезапускать весь сайт. А если обычный пользователь захочет зарегистрироваться? Мы же не дадим ему доступ к нашему коду!*
> 
> *Более того: если мы перезапустим наш сервер на Python, все изменения, которые мы внесли бы в эти списки во время работы, просто сотрутся из оперативной памяти.*
> 
> *Где должны храниться такие данные в реальных проектах?»*

**(Ждем ответа учеников: «В базе данных!»)**

**Преподаватель:**
> *«Правильно, в базах данных. На прошлом занятии мы с вами работали с СУБД SQLite и писали запросы на языке SQL. Помните команды вроде `CREATE TABLE`, `INSERT INTO` и `SELECT * FROM`?*
> 
> *Писать длинные SQL-запросы прямо внутри Python-кода — неудобно. Легко ошибиться в кавычке или запятой, и всё сломается. Поэтому умные программисты придумали штуку, которая называется **ORM**.»*

---

## Теория: Что такое ORM? (5 минут)

**Преподаватель:**
> *«**ORM (Object-Relational Mapping)** — это объектно-реляционное отображение, или, проще говоря, "переводчик" между Python и Базой Данных.*
> 
> *В Python мы привыкли работать с объектами и классами: `user.name = "Иван"`.*
> *В базах данных всё хранится в таблицах: строки, колонки, связи.*
> 
> *ORM переводит наши действия с классами на язык базы данных. Вместо написания SQL-запроса `INSERT INTO teachers...` мы просто напишем привычный Python-код: `Teacher.objects.create(...)`. Django сам поймет нас, переведет это в SQL и отправит в базу данных SQLite.*
> 
> *Давайте создадим наши первые модели!»*

---

## Шаг 1: Создание моделей (15 минут)

**Преподаватель:**
> *«Давайте откроем файл [main/models.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/models.py). Сейчас он пустой.*
> 
> *Мы создадим две модели — `Course` (Курс) и `Teacher` (Преподаватель). Модель в Django — это обычный Python-класс, который наследуется от `models.Model`.*
> 
> *Пишем вместе со мной: сначала опишем курс.»*

**(Пишем на проекторе):**

```python
from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса")

    def __str__(self):
        return self.name
```

**Преподаватель:**
> *«Смотрите: `models.CharField` — это текстовое поле для коротких строк (мы ограничили длину в 100 символов). `models.TextField` — это поле для большого объема текста (описания).*
> *Метод `__str__` нужен для того, чтобы в админке или в консоли объект красиво отображался по своему имени, а не как `<Course object (1)>`.*
> 
> *Теперь давайте опишем преподавателя. У него есть имя, возраст и курс, который он ведет. Как нам связать преподавателя с курсом? Используем связь "Один ко многим". Один курс могут вести много преподавателей, но за преподавателем мы закрепим один курс. В базах данных это называется внешним ключом (Foreign Key).*
> 
> *Дописываем в [main/models.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/models.py):»*

**(Пишем далее):**

```python
class Teacher(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя преподавателя")
    age = models.IntegerField(verbose_name="Возраст")
    # Связываем преподавателя с курсом
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name="teachers", 
        verbose_name="Курс"
    )

    def __str__(self):
        return f"{self.name} ({self.course.name})"
```

**Преподаватель:**
> *«Параметр `on_delete=models.CASCADE` означает: если мы удалим какой-то курс из базы, то все преподаватели, которые его вели, тоже автоматически удалятся (каскадное удаление).*
> *Параметр `related_name="teachers"` позволит нам легко получить список всех учителей курса прямо из объекта курса: например, `course.teachers.all()`.»*

---

## Шаг 2: Создание и применение миграций (10 минут)

**Преподаватель:**
> *«Мы написали код на Python. Но база данных SQLite пока ничего не знает про наши новые таблицы. Чтобы передать эту структуру в базу данных, нам нужны **миграции**.*
> 
> *Миграции — это чертежи изменений. Сначала мы просим Django сгенерировать чертеж на основе нашего кода.*
> 
> *Открываем терминал в папке проекта и пишем:»*

```bash
python manage.py makemigrations
```

**(Показываем вывод терминала. Должно появиться сообщение, что создан файл `0001_initial.py`).**

**Преподаватель:**
> *«Django создал файл-чертеж. Теперь даем команду применить этот чертеж непосредственно к файлу базы данных `db.sqlite3`:»*

```bash
python manage.py migrate
```

**(Показываем успешное выполнение миграций с отметками `OK`).**

**Преподаватель:**
> *«Ура! Таблицы созданы в нашей базе данных. Теперь давайте наполним их данными.»*

---

## Шаг 3: Работа в Django Shell. Практика CRUD (20 минут)

**Преподаватель:**
> *«Django позволяет управлять базой данных прямо из консоли. Давайте запустим специальную интерактивную оболочку:»*

```bash
python manage.py shell
```

**Преподаватель:**
> *«Давайте импортируем наши новые модели, чтобы работать с ними:»*

```python
from main.models import Course, Teacher
```

**Преподаватель:**
> *«Мы изучим 4 главные операции с данными — **CRUD**: Create (Создание), Read (Чтение), Update (Обновление), Delete (Удаление).*
> 
> *Начнем с **Create**. Создадим курс по Python:»*

```python
python_course = Course.objects.create(name="Python", description="Изучаем основы Python и Django")
```

**Преподаватель:**
> *«Мы создали объект в базе данных и сохранили его в переменную `python_course`. Давайте создадим еще один курс:»*

```python
cpp_course = Course.objects.create(name="C++", description="Алгоритмы и структуры данных на C++")
```

**Преподаватель:**
> *«Теперь добавим преподавателей. Обратите внимание: в поле `course` мы передаем не просто текст, а целый объект курса, который мы только что создали!»*

```python
Teacher.objects.create(name="Raushan", age=20, course=python_course)
Teacher.objects.create(name="Ishkhan", age=20, course=python_course)
```

**Преподаватель:**
> *«Отлично. Переходим к операции **Read** (Чтение). Как посмотреть все курсы, которые есть в базе?»*

```python
Course.objects.all()
```

**Преподаватель:**
> *«А как найти конкретный курс по его названию? Для этого есть метод `get`:»*

```python
course_py = Course.objects.get(name="Python")
print(course_py.description)
```

**Преподаватель:**
> *«А если нам нужно отфильтровать данные? Например, найти учителей, которым ровно 20 лет:»*

```python
Teacher.objects.filter(age=20)
```

**Преподаватель:**
> *«Благодаря связи `ForeignKey` мы можем легко посмотреть всех учителей, привязанных к курсу:»*

```python
python_course.teachers.all()
```

**Преподаватель:**
> *«Теперь разберем **Update** (Обновление). Допустим, мы хотим изменить описание курса по Python. Мы получаем курс, меняем атрибут и вызываем метод `save()`:»*

```python
course = Course.objects.get(name="Python")
course.description = "Самый лучший веб-курс в Кванте!"
course.save()
```

**Преподаватель:**
> *«И последняя операция — **Delete** (Удаление). Давайте удалим курс по C++:»*

```python
course_to_delete = Course.objects.get(name="C++")
course_to_delete.delete()
```

**Преподаватель:**
> *«Супер! Консоль — это здорово, но давайте теперь сделаем так, чтобы наш сайт брал данные именно из базы данных, а не из старых хардкодных списков.»*

**(Выходим из shell с помощью команды `exit()` или нажатия `Ctrl + Z` затем `Enter`).**

---

## Шаг 4: Обновление Views (15 минут)

**Преподаватель:**
> *«Открываем файл [main/views.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/views.py).*
> *Давайте полностью удалим старые словари `COURSES` и списки `TEACHER`.*
> 
> *Вместо них импортируем наши модели и перепишем логику функций-представлений так, чтобы они запрашивали данные из базы.»*

**(Замените код во [views.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/views.py) на следующий):**

```python
from django.shortcuts import render
from django.http import Http404
from .models import Course, Teacher

def main_page(request):
    # Достаем ВСЕ курсы и ВСЕХ учителей из базы данных
    courses = Course.objects.all()
    teachers = Teacher.objects.all()
    
    return render(request, './index.html', context={
        'courses': courses,
        'teachers': teachers
    })

def course_description(request, course_name):
    try:
        # Ищем в базе курс с таким именем
        course = Course.objects.get(name=course_name)
    except Course.DoesNotExist:
        # Если такого курса нет в БД, отдаем ошибку 404
        raise Http404(f"Курса {course_name} нет")

    return render(request, './course.html', context={"course": course})

def teacher_description(request, teacher_name):
    try:
        # Ищем в базе преподавателя с таким именем
        teacher = Teacher.objects.get(name=teacher_name)
    except Teacher.DoesNotExist:
        # Если преподавателя нет в БД, отдаем ошибку 404
        raise Http404(f'Учителя {teacher_name} нет')

    return render(request, './teacher.html', context={'teacher': teacher})
```

---

## Шаг 5: Обновление HTML-шаблонов (10 минут)

**Преподаватель:**
> *«Поскольку структура передаваемых данных изменилась, нам нужно поправить наши HTML-файлы.*
> 
> *Раньше в списке курсов мы передавали словарь `.items()` (где были ключ и значение), а теперь передаем список объектов `Course`.*
> 
> *Давайте откроем [main/templates/index.html](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/templates/index.html).»*

**(Покажите шаблон и исправьте цикл):**

**Было:**
```html
    {% for course_name, _ in courses %}
    <li><a href="course/{{ course_name }}">{{ course_name }}</a></li>
```

**Стало:**
```html
    {% for course in courses %}
    <li><a href="course/{{ course.name }}">{{ course.name }}</a></li>
```

**Преподаватель:**
> *«И в списке преподавателей: поле `teacher.course` теперь возвращает не просто строку вроде `'web'`, а целый связанный объект курса. Чтобы вывести его имя, напишем `teacher.course.name`.*
> 
> *Исправляем строчку с преподавателями в [main/templates/index.html](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/templates/index.html):»*

**Было:**
```html
    <li><a href="teacher/{{ teacher.name }}">{{ teacher.name }}, {{ teacher.course }}</a></li>
```

**Стало:**
```html
    <li><a href="teacher/{{ teacher.name }}">{{ teacher.name }}, {{ teacher.course.name }}</a></li>
```

**Преподаватель:**
> *«Теперь перейдем в шаблон описания курса [main/templates/course.html](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/templates/course.html).*
> *У нас там выводилось `course.course` (которого вообще не существовало в словаре). Давайте заменим это на нормальное описание из базы данных `course.description`.*
> 
> *Открываем [main/templates/course.html](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/templates/course.html) и переписываем:»*

**Стало:**
```html
{% extends 'base.html' %}

{% block title %}{{ course.name }}{% endblock %}

{% block content %}
<h1>{{ course.name }}</h1>
<p>{{ course.description }}</p>
{% endblock %}
```

---

## Шаг 6: Подключение к Django Admin (10 минут)

**Преподаватель:**
> *«Теперь самое интересное. Django «из коробки» предоставляет готовую красивую панель администратора, где мы можем удобно управлять нашими таблицами БД через браузер.*
> 
> *Давайте зарегистрируем наши модели в файле [main/admin.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/admin.py). Открываем его и пишем:»*

**(Пишем в [main/admin.py](file:///c:/Users/imart/PycharmProjects/quant-web-course-2026/django-project/main/admin.py)):**

```python
from django.contrib import admin
from .models import Course, Teacher

admin.site.register(Course)
admin.site.register(Teacher)
```

**Преподаватель:**
> *«Чтобы зайти в админку, нам нужен аккаунт суперадминистратора. Давайте создадим его в консоли. Пишем команду:»*

```bash
python manage.py createsuperuser
```

**Преподаватель:**
> *«Введите логин (например, `admin`), почту можно пропустить (нажать Enter), и дважды введите пароль (символы при вводе отображаться не будут, это нормально — защита от шпионов).»*

**(Создаем пользователя вместе с учениками).**

**Преподаватель:**
> *«Теперь запускаем наш сервер:»*

```bash
python manage.py runserver
```

**Преподаватель:**
> *«Открываем в браузере страницу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), вводим логин и пароль.*
> 
> *Посмотрите, у нас появились разделы Courses и Teachers!*
> *Давайте зайдем в Teachers и попробуем нажать "Add teacher". Видите поле "Курс"? Это выпадающий список со всеми курсами из базы данных. Django ORM автоматически связал наши таблицы и сделал удобный интерфейс!*
> 
> *Попробуйте добавить несколько курсов и преподавателей через админку, а потом перейдите на главную страницу нашего сайта [http://127.0.0.1:8000/](http://127.0.0.1:8000/) и убедитесь, что все они сразу отображаются на сайте!»*

---

## Заключение и вопросы для закрепления (5 минут)

**Преподаватель:**
> *«Итак, сегодня мы совершили переход от хранения данных в памяти Python к профессиональному подходу с использованием базы данных SQLite и Django ORM.*
> 
> *Давайте повторим:*
> 1. *Зачем нам нужны миграции?*
> 2. *Что означает связь `ForeignKey`?*
> 3. *Как расшифровывается аббревиатура CRUD?*
> 
> *На этом всё, на следующем уроке мы научимся создавать формы, чтобы пользователи могли сами отправлять данные на сайт без админки!»*
