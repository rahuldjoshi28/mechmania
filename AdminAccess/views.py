# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import itertools
from . import models
from questionPapers import models as Papers
from internships import models as Internships
from recruitments import models as Recruitments
import json
from django.utils.safestring import mark_safe
import os

# Create your views here.
@login_required(login_url='/loginsignup.html')
def index_admin(request):
    if request.user.is_authenticated and request.user.profile.is_admin:
        quotes = models.Quotes.objects.all()
        papers = Papers.Papers.objects.all()
        irequest = Internships.InternshipRequest.objects.all()
        rrequest = Recruitments.recruitmentRequest.objects.all()
        ivrequest = Internships.IVRequest.objects.all()
        industryData = Internships.industry.objects.all()
        return render(request,'index_admin.html',{'Quotes':quotes, 'Papers':papers, 'irequest':irequest, 'rrequest':rrequest, 'ivrequest':ivrequest, 'industryData':industryData})

@login_required(login_url='/loginsignup.html')
def saveQuotes(request):
    if request.method == 'POST':
        try:
            models.Quotes.objects.all().delete();
            quotes = json.loads(request.POST.get('quote'))
            quotedBys = json.loads(request.POST.get('quotedBy'))
            i = 0
            for q in quotes:
                qby = quotedBys[i]
                x = models.Quotes(quote=mark_safe(q),quotedBy=mark_safe(qby))
                x.save()
                i = i+1
            return HttpResponse('pass')
        except:
            return HttpResponse('fail')
    return HttpResponse('fail')

@login_required(login_url='/loginsignup.html')
def deletePaper(request):
    if request.method == 'POST':
        try:
            curPaper = Papers.Papers.objects.get(pk=request.POST.get('id'))
            try:
                curPaper.delete()
                os.remove(str(os.path.abspath(os.path.dirname(__name__)))+'/static/'+str(curPaper.paper))
            except:
                return HttpResponse('fail')
            return HttpResponse('pass')
        except:
            return HttpResponse('fail')
    return HttpResponse('fail')
