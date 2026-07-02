from django.db.models import Model
from django.shortcuts import render
from django.http import Http404

from django.http import HttpResponse

from main.models import Course, Teacher

def main_page(request):

    courses = Course.objects.all()
    teachers = Teacher.objects.all()

    return render(request, './index.html', context={
        'courses': courses,
        'teachers': teachers
    })


def course_description(request, course_name):

    course = Course.objects.get(name=course_name)

    if course is None:
        raise Http404(f"Курса {course_name} нет")

    return render(request, './course.html', context={"course": {'name': course.name,
                                                                'description': course.description}})

def teacher_description(request, teacher_name):

    teacher = Teacher.objects.get(name=teacher_name)
    if teacher is not None:
        return render(request, './teacher.html', context={'teacher': teacher})

    raise Http404(f'Учителя {teacher_name} нет')

