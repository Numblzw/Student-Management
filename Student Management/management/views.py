# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from management.models import Student, Teacher, Score,Lesson
# from models import Student, Teacher,Lesson,Score
from django.shortcuts import render
from django.http import HttpResponseRedirect
import csv, codecs
from django.http import HttpResponse
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    return render(request, "login.html")


def change(request):
    lid = int(request.GET['lid'])
    sid = int(request.GET['sid'])
    sscore = request.POST.get("score", None)
    print('将课程id为',lid,'，学生id为',str(sid),'的分数改为',sscore)
    Score.objects.filter(id=sid).update(score=sscore)
    score = Score.objects.filter(lNum=lid)
    teacher = Teacher.objects.get(t_lesson_id=lid)
    return render(request, "teacher.html", {"teacher": teacher, "score": score})

#登陆后端函数
def login(request):
    print(request.POST.get("sid", None))
    if request.method == "POST":
        type = request.POST.get("fruit")
        name = request.POST.get("username", None)
        ps = request.POST.get("password", None)

    print(type)
    if type == "1":
        try:
            s = Student.objects.get(s_number=name)
        except Student.DoesNotExist:
            return HttpResponseRedirect("/loginerror/")
        idnum = int(str(s.ID_number)[-6:])
        print(idnum)
        print("ps=", ps)
        if idnum == int(ps):
            student = Student.objects.get(s_number=name)
            score = Score.objects.filter(sNum=name)
            print(score[0].sName)
            return render(request, "student.html", {"student": student, "score": score})
        else:
            return HttpResponseRedirect("/loginerror/")
    elif type == "2":

        try:
            t = Teacher.objects.get(t_number=name)
        except Teacher.DoesNotExist:
            return HttpResponseRedirect("/loginerror/")
        tps = t.t_pass
        if tps == int(ps):
            teacher = Teacher.objects.get(t_number=name)
            l_num = teacher.t_lesson_id
            score = Score.objects.filter(lNum=l_num)
            return render(request, "teacher.html", {"teacher": teacher, "score": score})
        else:
            return HttpResponseRedirect("/loginerror/")


def register(request):
    return render(request, "Register.html")


# TODO:添加注册去重功能

#注册用户
def adduser(request):
    print('注册用户')
    print(request.POST.get("username", None))
    if request.method == "POST":
        type = request.POST.get("fruit")
        name = request.POST.get("name",None)
        number = request.POST.get("username", None)
        ps = request.POST.get("password", None)
        gender = request.POST.get("gender",None)
        grade = request.POST.get("grade",None)
        place = request.POST.get("place",None)
        subject = request.POST.get("subject",None)
        id = request.POST.get("id",None)
    print(type,number,name,ps,gender,grade,place,subject,id)

    if type == "1":
        if Student.objects.filter(s_number=number).exists():
            return HttpResponseRedirect("/error/")
        #s = Student.objects.get(s_number=name)
        #idnum = int(str(s.ID_number)[-6:])
        # print(idnum)
        # print("ps=", ps)
        # if idnum == int(ps):
        #     student = Student.objects.get(s_number=name)
        #     score = Score.objects.filter(sNum=name)
        #     print(score[0].sName)
        #     return render(request, "student.html", {"student": student, "score": score})
        # else:
        #     return HttpResponseRedirect("/")
        if gender == '1':
            sex='男'
        else:
            sex='女'
        total = Score.objects.count()
        lesson_list = Lesson.objects.all()
        for lesson in lesson_list:
            total += 1
            Score.objects.create(id=total, sName=name, sNum=number, lName=lesson.l_name, lNum=lesson.l_number,
                                 score=0, lCredit=lesson.credit, lTime=lesson.time)
        Student.objects.create(s_number=number, s_name=name, sex=sex, subject=subject,
                               grade=grade, ID_number=id, native_place=place)
        return render(request,'successful.html')
    elif type == "2":

        try:
            t = Teacher.objects.get(t_number=name)
        except Teacher.DoesNotExist:
            return HttpResponseRedirect("/")
        tps = t.t_pass
        if tps == int(ps):
            teacher = Teacher.objects.get(t_number=name)
            l_num = teacher.t_lesson_id
            score = Score.objects.filter(lNum=l_num)
            return render(request, "teacher.html", {"teacher": teacher, "score": score})
        else:
            return HttpResponseRedirect("/")

#导出成绩为csv文件
def export_score_csv(request):
    lid = int(request.GET['lid'])
    print('导出课程id为',str(lid),'的学生成绩信息表')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Score.csv"'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['学生姓名', '学号', '课程名称', '分数'])
    score_list = Score.objects.filter(lNum=lid).values_list('sName', 'sNum', 'lName', 'score')
    for score in score_list:
        writer.writerow(score)
    return response


def error(request):
    return render(request, "error.html")


def loginerror(request):
    return render(request, "loginerror.html")
