from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from .models import *
from .cgpa import gpa_calculator
from django.db.models import Sum
# Create your views here.
def homepage(request):
    return render(request, "main/homepage.html", {})

def main(request):
    if request.method == "POST":
        is_username_valid = check_password(request.POST.get("username"),"pbkdf2_sha256$320000$lbdPKNBNhahP8djLxDR3eQ$hASC23bxRRzvyN+o+78YuLJ2v11GUPf1Sm68Y1+a4SA=")
        is_password_valid = check_password(request.POST.get("password"),"pbkdf2_sha256$320000$Wjv7CzD7B0DYOYaCeX0gjA$9YcYztHU2wMxcLcd3s8RjwOg26QRt9ETYodOD8PK6EE=")
        if is_username_valid and is_password_valid:
            return render(request, "main/index.html", {})
        else:
            messages.error(request, "Invalid Username or Password")
    else:
        messages.error(request, "You don't have access to this page, Please login.")
    return redirect("home")

def create_course(request):
    print(request)
    if request.method == "POST":
        print(request.POST)
        department = Department.objects.get(pk=int(request.POST.get("department")))
        course = Course.objects.create(name=request.POST.get("course-name"),code=request.POST.get("course-code"),level=request.POST.get("level"), unit=float(request.POST.get("course-unit")) ,semester=request.POST.get("semester"),department=department)
        return HttpResponse(f'''
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>Successful!</strong> {course.name} Course has been created.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        ''')

    return render(request, "main/create-course.html", {"departments": Department.objects.all()})

def create_student(request):
    if request.method == "POST":
        print(request.POST)
        department = Department.objects.get(pk=int(request.POST.get("department")))
        student = Student(name=request.POST.get("name"),matric_no=request.POST.get("matric-no"),program=request.POST.get("program"),level=request.POST.get("level"),department=department)
        student.full_clean()
        student.save()
        return HttpResponse(f'''
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>Successful!</strong> {student.name} Student has been created.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        ''')
    return render(request, "main/create-student.html", {"departments": Department.objects.all()})

def manage_result(request):
    if request.method == "POST":
        if request.POST.get("type") == "delete":
            print(request.POST)
            Result.objects.get(pk=request.POST.get("result-pk")).delete()
            return HttpResponse("Deleted")
        print(request.POST)
        course = Course.objects.get(pk=int(request.POST.get("course")))
        student = Student.objects.get(pk=int(request.POST.get("student")))
        score = request.POST.get("score")
        result = Result.objects.create(student=student, course=course, score = score)
        return HttpResponse(f'''
        <div class="alert alert-success alert-dismissible fade show" role="alert">
            <strong>Successful!</strong> Result for {student.name} in {course.code}:{course.name} with score {score} has been created.
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        ''')

    return render(request, "main/manage-result.html", {"courses": Course.objects.all(), "students": Student.objects.all(), "results": Result.objects.order_by("course__code","student__name") })

def manage_department(request):
    if request.method == "POST":
        print(request.POST)
        Department.objects.create(name=request.POST.get("department"), total_units=request.POST.get("unit"))

    return render(request, "main/manage-department.html", {"departments": Department.objects.all()})

def manage_student(request):
    if request.method == "POST":
        Student.objects.get(pk=request.POST.get("student-pk")).delete()
        return HttpResponse("Deleted")
    return render(request, "main/manage-student.html", {"students": Student.objects.all()})

def manage_course(request):
    if request.method == "POST":
        Course.objects.get(pk=request.POST.get("course-pk")).delete()
        return HttpResponse("Deleted")
    return render(request, "main/manage-course.html", {"courses": Course.objects.all()})

def show_results(request):
    try:
        student = Student.objects.get(matric_no = request.GET.get("matric_no"))
        results = student.result_set.order_by("course__level","course__semester")
        total_units = results.filter(score__gte=40).aggregate(Sum("course__unit"))
        current_units = list(total_units.values())[0]
        total_units_number = student.department.total_units
        scores_list = list(results.values_list("score",flat=True))
        cgpa = results.count() / gpa_calculator(scores_list)
        cgpa = cgpa / 4
        print(results.count())
        print(cgpa)
        if cgpa < 1.5:
            cgpa_range = "Failure"
        elif cgpa >= 1.5 and cgpa < 2.5:
            cgpa_range = "Pass"
        elif cgpa >= 2.5 and cgpa < 3.5:
            cgpa_range = "Lower Credit"
        elif cgpa >= 3.5 and cgpa < 4.5:
            cgpa_range = "Upper Credit"
        elif cgpa >= 4.5:
            cgpa_range = "Distinction"

        can_print = (current_units >= total_units_number)
        return render(request, "main/showResult.html",{"student":student,"results":results,"total_units": total_units_number, "current_unit": current_units,"can_print": can_print, "cgpa_range": cgpa_range, "cgpa": cgpa})
    except Student.DoesNotExist:
        messages.warning(request, "Invalid Matric Number")
        return redirect("home")
    except:
        messages.warning(request, "An error occured")
        messages.warning(request, "An error occured")
        return redirect("home")

