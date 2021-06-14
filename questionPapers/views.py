# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from questionPapers.models import Papers
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .models import College, Subject, Papers
import operator, os
from functools import reduce
from . import models
from AdminAccess import models as Quotes

def index(request):
    #paperQuery = request.POST.get("searchPaper")
    #print(paperQuery)
    #paperList = []
    return render(request, "questionPapers/questionPapers.html", {})

def searchPaper(query):
    list = query.split(" ")
    qset = Papers.objects.all()
    #qset = qset.filter(Q(description__icontains=a) | Q(year__icontains=a) | Q(college__college__icontains=a) | Q(subject__subject__icontains=a) for a in list)
    alist = [Q(term__icontains=a) | Q(description__icontains=a) | Q(year__icontains=a) | Q(college__college__icontains=a) | Q(subject__subject__icontains=a) for a in list]
    if(alist):
        qset = Papers.objects.all().filter(reduce(operator.and_, alist))
    return qset

# search result
def getPaperList2(request, query = None, response = "json"):
    if query == None:
        query = request.POST.get("query")
    print(query)
    data = searchPaper(query)
    print(data)
    if(len(data) == 0):
        print("##################### No result fond ########################")
    paperList = {}
    paperList.setdefault('papers', [])
    idList = {}
    idList.setdefault('id', [])
    for a in data:
        paperName = str(a.college.college)
        if(a.subject.subject != 'na'):
            paperName += '-'+a.subject.subject
        paperName += '-' + str(a.term)
        paperName+= '-' + str(a.year)
        paperList['papers'].append(paperName)
        idList['id'].append(str(a.id))
    fl = {"papers":paperList,"id":idList}
    print(fl)
    if response == "json":
        return JsonResponse(fl)
    else:
        return fl

def getPaperList(request):
    query = request.POST.get("query")
    print(query)
    data = searchPaper(query)
    print(data)
    if (len(data) == 0):
        print("##################### No result found ########################")
    paperList = {}
    paperList.setdefault('papers', [])
    idList = {}
    idList.setdefault('id', [])
    for a in data:
        opaper = {}
        opaper["year"] = a.year

        paperName = str(a.college.college)
        if (a.subject.subject != 'na'):
            paperName += '-' + a.subject.subject
        paperName += '-' + str(a.term)
        paperName += '-' + str(a.year)
        opaper["name"] = paperName

        paperList['papers'].append(opaper)
        idList['id'].append(str(a.id))

    fl = {"papers": paperList, "id": idList}
    print(fl)
    return JsonResponse(fl)

#get file
def getFile(request):
    paper_id = request.POST.get("id")
    a = Papers.objects.get(pk=int(str(paper_id)))
    f = a.paper
    return HttpResponse(f.name)

def uploadsuccess(request):
    sub = request.POST.get('subject').lower()
    yr = request.POST.get('year').lower()
    sch = request.POST.get('school').lower()
    term = request.POST.get('term').lower()
    if term=='-':
        term=''
    try :
        cob=College.objects.get(college=str(sch))
    except College.DoesNotExist:
        cob=None
    if cob==None:
        College(college=str(sch)).save()
    try:
        sob=Subject.objects.get(subject=str(sub))
    except Subject.DoesNotExist:
        sob=None
    if sob==None:
        Subject(subject=str(sub)).save()
    cob = College.objects.get(college=str(sch))
    sob = Subject.objects.get(subject=str(sub))
    print(request.FILES)
    fs = request.FILES['file']
    f = open(os.path.abspath(os.path.dirname(__name__))+'/static/papersDir/'+sch+'-'+sub+'-'+term+'-'+yr+'.pdf','wb+')
    for chunks in fs.chunks():
        f.write(chunks)
    f.close()
    desc=request.POST.get('description')
    Papers(year=str(yr),paper='papersDir/'+sch+'-'+sub+'-'+term+'-'+yr+'.pdf',term=term,college=cob,subject=sob,description=str(desc)).save()
    st=(Papers.objects.filter(year=str(yr)))
    return redirect('/adminaccess/')
