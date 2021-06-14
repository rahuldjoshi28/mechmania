from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import recruitment, recruitmentRequest, ConfirmedRecruitment
from internships.models import industry
from Accounts.models import Profile
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from functools import reduce
import os, operator

def index(request):
    list = getData(request, "#")
    return render(request, "recruitments.html", {"data": list})
    #return render(request, "recruitments/index.html",{"data":list})

def search(requset):
    query = requset.POST.get("query")
    ans = getData(requset, query)
    print(ans)
    return ans

def getData(request, query):
    indSet  = industry.objects.all()
    applicable = 1
    confirmed_qset = []
    requested_qset = []
    if request.user.is_authenticated():
        user = request.user.profile
        print("============================================")
        confirmed_qset = [a.recruitment for a in ConfirmedRecruitment.objects.filter(user = user)]
        #confirmed = [a for a in confirmed_qset]
        print (confirmed_qset)
        if len(confirmed_qset)>0:
            applicable = 0
        else:
            requested_qset = [a.recruitment for a in recruitmentRequest.objects.filter(user = user)]
            #for a in requested_qset:
            #    requested.append(a)
    else:
        applicable = 1
    answer = {}
    answer.setdefault("data",[])

    answer["applicable"] = applicable

    for a in indSet:
        tmp = {}
        tmp["pk"] = a.pk
        tmp["indname"] = a.name
        tmp["logo"] = "/"+a.logo.url.split("/",1)[1]
        tmp["address"] = a.address
        tmp["website"] = a.website
        tmp["description"] = a.description
        qset = recruitment.objects.filter(industry = a)


        if(query != "#"):
            constrainList = query.split(" ")
            constrin = [Q(type__icontains = a) | Q(salary__icontains = a) | Q(description__icontains = a) | Q(qualifications__icontains = a) | Q(industry__name__icontains = a) | Q(industry__address__icontains = a) for a in constrainList ]
            if(qset):
                qset = qset.filter(reduce(operator.and_ , constrin))
        recruitments = recruitmentEncode(qset, confirmed_qset, requested_qset)
        if recruitments:
            tmp["recruitments"] = recruitments
            answer["data"].append(tmp)
    print("\n\n recruitment result \n", answer)
    if query == "#":
        return JsonResponse({"result":answer})
    else:
        return answer

def getRecruitments(request):
    indname = request.POST.get("industry")
    print("in getrecuitments ",indname)
    ind = industry.objects.get(name = indname)
    applicable = 1
    confirmed_qset = []
    requested_qset = []
    if request.user.is_authenticated():
        user = request.user.profile
        print("============================================")
        confirmed_qset = [a.recruitment for a in ConfirmedRecruitment.objects.filter(user = user)]
        #confirmed = [a for a in confirmed_qset]
        print (confirmed_qset)
        if len(confirmed_qset)>0:
            applicable = 0
        else:
            requested_qset = [a.recruitment for a in recruitmentRequest.objects.filter(user = user)]
            #for a in requested_qset:
            #    requested.append(a)
    else:
        applicable = 1

    return JsonResponse({"result": recruitmentEncode([a for a in recruitment.objects.filter(industry = ind)], confirmed_qset, requested_qset), "applicable":applicable})

def recruitmentEncode(list, confirmed, requested):
    answer = []
    if not list:
        return []
    print("list is +++++++++++ ")
    print(list)
    print("confirmed is ")
    print(confirmed)
    print("requested")
    print(requested)
    for a in list:
        tmp = {}
        tmp["pk"] = a.pk
        tmp["type"] = a.type
        tmp["salary"] = a.salary
        tmp["description"] = a.description
        tmp["qualifications"] = a.qualifications
        """
        if len(requested)>0:
            print("and requested query is ")
            print(requested)
            try :
                #ss = recruitmentRequest.objects.filter(recruitment__pk=int(a.pk))
                ss = requested.filter(recruitment__pk = a.pk)
                #reqList = [a for a in ss]
                if len(ss)>0:
                #if ss in requested:
                    tmp["is_applicable"] = 0
                else:
                    tmp["is_applicable"] = 1
            except:
                tmp["is_applicable"] = 1
        else:
            tmp["is_applicable"] = 1

        if len(confirmed)>0:
            print("and confirmed are ")
            print(confirmed)
            try:
                #ss = ConfirmedRecruitment.objects.filter(recruitment__pk = a.pk)
                #crList = [a for a in ss]
                #print("try complete")
                #print(crList)
                ss = confirmed.filter(recruitment__pk=a.pk)
                if (len(ss) > 0):
                #if crList in confirmed:
                    tmp["confirmed"] = 1
                else:
                    tmp["confirmed"] = 0
            except ObjectDoesNotExist:
                print("in expect")
                tmp['confirmed'] = 0
        else:
            print("length is 0")
            tmp["confirmed"] = 0
        """
        if a in confirmed:
            tmp["confirmed"] = 1
        else:
            if a in requested:
                tmp["applied"] = 1
            else:
                tmp["applied"] = 0
            tmp["confirmed"] = 0

        answer.append(tmp)
    return answer

def isApplicable(usr, requset_for, recid):
    print("in isApplicable")
    li = ConfirmedRecruitment.objects.filter(user = usr)
    print (li)
    if len(li) != 0:
        return False
    li = recruitmentRequest.objects.filter(user = usr).filter(recruitment__id = recid)
    print (li)
    if len(li)>0:
        return False
    print("gonna return true")
    return True

def checkLogin(request, request_for, recid):
    if request.user.is_authenticated():
        user = request.user.profile
        print("its authenticated")
        if request_for == "admin_access":
            return user.is_admin
        else:
            return isApplicable(user, request_for, recid)
    else:
        return False

def applyRec(request):
    recId = int(request.GET.get("recId"))
    if checkLogin(request, "apply", recId) == False:
        return HttpResponse("<script type='text/javascript'>alert('sorry you cant apply');</script>");

    rec = recruitment.objects.get(pk = recId)
    a = recruitmentRequest(user = request.user.profile, recruitment = rec)
    a.save()
    return redirect(request.META['HTTP_REFERER'])

def adminConfirm(request):
    print("in admin confirm")
    recId = int(request.GET.get("recId"))
    print(recId)
    list = recruitmentRequest.objects.filter(recruitment__pk = recId)
    print("recruitment request list is ")
    print(list)
    rec = recruitment.objects.get(pk = recId)
    return render(request, "recruitments/adminConfirmation.html", {"list":list, "recruitment": rec})

def confirmRec(request):
    print(request.POST.get("recId"))
    recId = int(request.POST.get("recId"))
    uid = int(request.POST.get("uid"))

    usr = Profile.objects.get(user__pk = uid)
    rec = recruitment.objects.get(pk = recId)
    recruitmentRequest.objects.filter(user = usr).delete()

    ConfirmedRecruitment(user = usr, recruitment = rec).save()
    return  HttpResponse("<h1>Confirmed</h1>")
