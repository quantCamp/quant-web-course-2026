from django.shortcuts import render
from django.http import Http404

from django.http import HttpResponse

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


def main_page(request):
    return render(request, './index.html', context={
        'courses': list(COURSES.items()),
        'teachers': TEACHER
    })


def course_description(request, course_name):
    if course_name not in COURSES:
        raise Http404(f"Курса {course_name} нет")

    return render(request, './course.html', context={"course": {'name': course_name, 'description': COURSES[course_name]}})

def teacher_description(request, teacher_name):
    for teacher in TEACHER:
        if teacher_name == teacher['name']:
            return render(request, './teacher.html', context={'teacher': teacher})

    raise Http404(f'Учителя {teacher_name} нет')