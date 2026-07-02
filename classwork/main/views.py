from django.shortcuts import render
from django.http import HttpResponse

courses = {
    "cpp": "si plus plus",
    "python": "pyton"
}

teachers = [
    {"name": "Раушан Ханипов", "age": 20, "course": "Web programming on Python", "link": "raushan-hanipov", "image": "raushan.webp"},
    {"name": "Ишхан Мартиросян", "age": 20, "course": "Web programming on Python", "link": "ishkhan-martirosyan", "image": "ishkhan.jpg"},
    {"name": "Денис Меганайт", "age": 67, "course": "Olimpiad math-10", "link": "denis-megaknight", "image": "burger.jpg"}
]

def main_page(request):
    return render(request, './index.html', context={"courses": list(courses.items()), "teachers": teachers})

def course_page(request, course_name):
    if course_name not in courses:
        return HttpResponse(f"нету {course_name}", status=200)
    return HttpResponse(courses[course_name])

def teacher_page(request, teacher_link):
    for teacher in teachers:
        if teacher_link == teacher['link']:
            return render(request, './teacher.html', context={"teacher": teacher})
    return HttpResponse(status=404)
    