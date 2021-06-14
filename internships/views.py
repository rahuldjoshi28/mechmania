from django.shortcuts import render, redirect
from .models import industry,internship, IndustrialVisit, InternshipRequest, ConfirmedInternships, RequestNotice, Group, IVRequest, UpcomingIV
from django.http import HttpResponse,JsonResponse
from Accounts.models import User,Profile
from internships.models import industry
from django.contrib import messages
from notifications.models import Notice
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from functools import reduce
import os, operator

import json, operator, datetime

def index(request):
    return render(request, 'internships/index.htm',{})

def internshipData(request):
    page=request.POST.get('pageno')
    loc=request.POST.get('location')
    tp=request.POST.get('type')
    print("pageno = ................................................"  + str(page))

    if(loc != 'no'):
        qset = internship.objects.filter(company__city=loc)
    if(tp != 'no'):
        qset = internship.objects.filter(type=tp)
    if(loc=='no' and tp=='no'):
        qset = internship.objects.all()

    try:
        page = int(page)
    except:
        print("Got exception converting page string into int")
        page = 0

    x=page*10
    y=x-10
    data={}
    flg = 0
    li = []

    data.setdefault('internships', [])
    alreadyUndergoing = 0

    if request.user.is_authenticated():
        flg = 1
        if request.user.profile.is_applied_to_internship == 1:
            try:
                alreadyUndergoing = ConfirmedInternships.objects.get(user = request.user.profile).internship.id
            except:
                alreadyUndergoing = 0
        prevApplied = InternshipRequest.objects.filter(user = request.user.profile)
        for a in prevApplied:
            li.append(a.internship.pk)

    for a in qset:
        indata = {}
        indata['pk'] = a.pk
        indata['company'] = a.company.name
        indata['stipend'] = a.stipend
        indata['startdate'] = a.startdate
        indata['enddate'] = a.enddate
        indata['description'] = a.description
        indata['qualification'] = a.qualification
        indata['type'] = a.type
        indata['website'] = a.company.website
        indata['address'] = a.company.address
        indata['logo'] = "/"+a.company.logo.url.split("/",1)[1]
        if alreadyUndergoing == 0:
            indata["allowed"] = 0
            if flg == 1:
                if a.pk in li:
                    indata["applied"] = 1
                else:
                    indata["applied"] = 0
            else:
                indata["applied"] = 0
        else:
            indata["allowed"] = alreadyUndergoing

        data["internships"].append(indata)

    tv=False
    if len(data['internships'][x:])>0:
        tv=True
    data=data['internships'][y:x]
    total = int(len(qset)/10)
    if len(qset)%10 != 0:
        total += 1
    print("total ========== ", total)
    ans={'total': total,
         'data': data,
    }
    print(ans)
    return JsonResponse(ans)


def isApplicable(usr, requset_for, recid):
    print("in isApplicable")
    li = ConfirmedInternships.objects.filter(user = usr)
    print (li)
    if len(li) != 0:
        return False
    li = InternshipRequest.objects.filter(user = usr).filter(internship__id = recid)
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

def applyInternship(req):
    indId = req.GET.get("industry")
    if(checkLogin(req, "apply", indId) == False):
        print("Not applicable")
        #messages.info(req, "Sorry, you cannot apply!")
        return render(req, "internships/index.htm", {"message" : "Sorry, you cannot apply"})
        #return HttpResponse("<h1>Sorry you cant apply</h1>")
    user = req.user.profile
    ish = internship.objects.get(id = indId)

    #check whether registered

    a = InternshipRequest(user = user,internship = ish)
    a.save()
    from notifications.views import sendNotice
    sendNotice(user, "You have successfully registered for "+ish.company.name+" internship");
    return redirect(req.META['HTTP_REFERER'])

def intApplications(request, indId):
    #indId = request.GET.get("industry")
    print("industry id ======================== "+ str(indId))
    if checkLogin(request, "admin_access", indId) == False:
        #messages.info(request, "Sorry, you dont have admin rights!")
        return render(request, "internships/index.htm", {"message": "Sorry you dont have admin right"})
        #return HttpResponse("<h1>'Better behave yourself'</h1>")
    qset = InternshipRequest.objects.filter(internship__id = int(str(indId)))
    print("length of qset == "+ str(qset))
    if len(qset) == 0:
        return render(request, "internships/applications.html", {"applicants" : [], "industry": internship.objects.get(id = int(str(indId)))})
    li = []
    for a in qset:
        li.append(a.user.user)
    return render(request, "internships/applications.html", {"applicants" : li, "industry": qset[0].internship})

def confirmInternship(request):
    uid = int(request.POST.get("uid"))
    intId = request.POST.get("internship")
    #print("internship id  "+str(intId))

    user = Profile.objects.get(user__pk = uid)
    user.is_applied_to_internship = 1
    user.save()
    #user = User.objects.get(id = 1)
    intr = internship.objects.get(id = intId)
    ConfirmedInternships(user = user, internship = intr).save()
    InternshipRequest.objects.filter(user = user).delete()

    from notifications.views import sendNotice
    sendNotice(user, "Congratulation, your internship at " + intr.company.name + " is confirmed");

    #return intApplications(request, intId)
    return HttpResponse("Success")

def getInternships(company, user, filter = None):
    data = []
    if filter:
        qset = []
        qset2 = internship.objects.all().filter(reduce(operator.and_, filter))
        for a in qset2:
            if a.company == company:
                qset.append(a)
        if len(qset) == 0:
            return []
    else:
        qset = internship.objects.filter(company = company)
    print("in getinternship")
    try:
        user = user.profile
        confirmedId = 0
        try:
            confirmedId = ConfirmedInternships.objects.get(user = user).internship.id
        except Exception as e:
            print("Exception ++++++++++++++++++++ ", e)
            confirmedId = 0
            try:
                applied = [ a.internship for a in InternshipRequest.objects.filter(user = user)]
            except Exception as e1:
                print("error in exception ", e1)
                applied = []

        for a in qset:
            tmp = {}
            tmp["indname"] = company.name
            tmp["logo"] = "/" + company.logo.url.split("/", 1)[1]
            tmp["pk"] = a.pk
            tmp["description"] = a.description
            tmp["startdate"] = a.startdate
            tmp["enddate"] = a.enddate
            tmp["stipend"] = a.stipend
            tmp["qualification"] = a.qualification
            tmp["type"] = a.type
            tmp["allowed"] = confirmedId
            print("\nconfirmed id = ", confirmedId," \n")
            if confirmedId>0:
                print("(((((((((((((( Yes confirmed id > 0 )))))))))))))))")
                tmp["applied"] = 0
            else:
                if a in applied:
                    tmp["applied"] = 1
                else:
                    tmp["applied"] = 0
            data.append(tmp)
    except:
        for a in qset:
            tmp = {}
            tmp["pk"] = a.pk
            tmp["description"] = a.description
            tmp["startdate"] = a.startdate
            tmp["enddate"] = a.enddate
            tmp["stipend"] = a.stipend
            tmp["qualification"] = a.qualification
            tmp["type"] = a.type
            tmp["allowed"] = 0
            tmp["applied"] = 0
            data.append(tmp)
    return data

def searchInternships(request, query = "#"):
    constrainList = query.split(" ")
    constrin = [Q(type__icontains=a) | Q(description__icontains=a) | Q(company__name__icontains=a) | Q(
        company__address__icontains=a) | Q(qualification__icontains=a) | Q(stipend__icontains=a) for a in
                constrainList]
    inds = industry.objects.all()
    result = []
    for a in inds:
        result = result + getInternships(a, request.user, constrin)
    if len(result) == 0:
        return []
    print("\ninternships message: ",result)
    return result

def getIVs(request, query = None):
    if(query == None):
        indname = request.POST.get("industry")
        ind = industry.objects.get(name = indname)
        ivs = IndustrialVisit.objects.filter(company = ind)
    else:
        constrainList = query.split(" ")
        constrin = [Q(type__icontains=a) | Q(description__icontains=a) | Q(company__name__icontains=a) | Q(company__address__icontains=a) for a in
                    constrainList]
        ivs = IndustrialVisit.objects.filter(reduce(operator.and_, constrin))
        if len(ivs) == 0:
            return []
    result = {}
    data = []
    try:
        usr = request.user.profile
        confirmed, applied = 0, 0
        try:
            confirmed = UpcomingIV.objects.get(IVRequest__user = usr).IVRequest.IV.pk
        except Exception as e:
            print("in exception ", e)
            confirmed = 0
            try:
                applied = Group.objects.filter(user = usr).IVRequest.IV.pk
            except:
                applied = 0

        for a in ivs:
            tmp = {}
            tmp["indname"] = a.company.name
            tmp["logo"] = "/" + a.company.logo.url.split("/", 1)[1]
            tmp["pk"] = a.pk
            tmp["type"] = a.type
            tmp["duration"] = a.duration
            tmp["description"] = a.description
            tmp["ratings"] = a.ratings
            tmp["is_available"] = a.isavailable
            tmp["mincnt"] = a.minimumCount
            data.append(tmp)
        result["confid"] = confirmed
        result["appliedid"] = applied
        result["data"] = data
    except:
        for a in ivs:
            tmp = {}
            tmp["pk"] = a.pk
            tmp["type"] = a.type
            tmp["duration"] = a.duration
            tmp["description"] = a.description
            tmp["ratings"] = a.ratings
            tmp["is_available"] = a.isavailable
            tmp["mincnt"] = a.minimumCount
            data.append(tmp)
        result["confid"] = 0
        result["appliedid"] = 0
        result["data"] = data
    if query == "#":
        return JsonResponse({"message": result})
    else:
        print("\n\n this is iv result   ", result)
        return result

# Nitin
# industrual Visit
def industrialVisitData(request):
    page = request.POST.get('pageno')
    loc = request.POST.get('location')
    tp = request.POST.get('type')
    if (loc == 'no' and tp == 'no'):
        qset = IndustrialVisit.objects.all()
    elif (loc != 'no' and tp != 'no'):
        qset = IndustrialVisit.objects.filter(company__city=loc, type=tp)
    elif (loc != 'no'):
        qset = IndustrialVisit.objects.filter(company__city=loc)
    elif (tp != 'no'):
        qset = IndustrialVisit.objects.filter(type=tp)
    applied = Group.objects.filter(user=request.user.profile)
    suss = []
    apply = []
    cannotapply = 0
    for b in applied:
        temp = UpcomingIV.objects.filter(IVRequest=b.IVRequest)
        for ab in temp:
            suss += [ab.IVRequest.IV]
            cannotapply = 1
        else:
            apply += [b.IVRequest.IV]
    x = int(page) * 10
    y = x - 10
    data = {}
    data.setdefault('industrialVisit', [])
    for a in qset:
        indata = {}
        indata['company'] = a.company.name
        indata['pk'] = a.pk
        indata['description'] = a.description
        indata['type'] = a.type
        indata['website'] = a.company.website
        indata['address'] = a.company.address
        indata['duration'] = a.duration
        indata['ratings'] = a.ratings
        indata['available'] = a.isavailable
        indata['logo'] = "/" + a.company.logo.url.split("/", 1)[1]
        indata["mincnt"] = a.minimumCount
        if a in apply:
            indata['applied'] = 1
            cannotapply = 1
        else:
            indata['applied'] = 0
        indata['confirmed'] = 0
        if a in suss:
            indata['confirmed'] = 1
        data["industrialVisit"].append(indata)
    tv = False
    if len(data['industrialVisit'][x:]) > 0:
        tv = True
    data = data['industrialVisit'][y:x]

    total = int(len(data) / 10);
    if len(data) % 10 != 0:
        total += 1
    ans = {'total': total,
           'data': data,
           'cannotapply': cannotapply,
           }
    print(ans)
    return JsonResponse(ans)


def RecomandUsers(request):
    intial=str(request.POST.get("initials"))
    print("debug"+intial)
    ivid=str(request.POST.get("IVId"))
    topTen=User.objects.filter(username__startswith=intial)
    topTen = topTen[:10]
    s=""
    xx = str(request.user.username)
    print(xx)
    for x in topTen:
        if(xx!=str(x)):
            s=s+" "+str(x)
    print(s)
    return JsonResponse({'data':s})

@login_required
def applyIV(request,IVId):
    x=IVRequest.objects.filter(IV__pk=IVId,user=request.user.profile)
    y=IndustrialVisit.objects.filter(pk=IVId)
    if(len(y)==0):
        return HttpResponse("<h1>you might have typed wrong url</h1>")
    if(y[0].isavailable=='na'):
        return HttpResponse("<h1>this IV is curently not available</h1>")
    if(len(x)>0):
        return HttpResponse("<h1>Are you kidding...</h1>")
    k=str(y[0].minimumCount)
    print(k)
    return render(request,"internships/applyIV.html",{'IVId':str(IVId),'minimumCnt':k})
def CreatingGroup(request,IVId):
    data=request.POST.get('data')
    dt=json.loads(data)
    iv=IndustrialVisit.objects.filter(pk=IVId)
    if len(iv)==0:
        return JsonResponse({'data': "no such iv"})
    y = iv[0].minimumCount
    dtt=[]
    for i in dt:
        x=User.objects.filter(username=i)
        if x!=None and not(x in dtt) and x != request.user:
            dtt+=[x]
    if(len(dtt)<y):
        return JsonResponse({'data': "you have selected less number of users than required for iv"})
    ivr = IVRequest.objects.create(IV=iv[0], user=request.user.profile)
    print("creategrp")
    print(dtt)
    for i in dtt:
        xx=Profile.objects.filter(user=i)
        print("java")
        print(xx)
        RequestNotice.objects.create(user=xx[0],IVRequest=ivr)
    Group.objects.create(IVRequest=ivr,user=request.user.profile)
    return JsonResponse({'data':"Success"})
def listOfApplicants(request,IVId):
    if(request.user.profile.is_admin==False):
        return render(request,"internships/applyIV.html",{'IVId':str(IVId)})
    yy=IndustrialVisit.objects.filter(pk=IVId)
    if(len(yy)==0):
        return HttpResponse("<h1>you might have typed wrong url</h1>")
    x=IVRequest.objects.filter(IV__pk=IVId).order_by('-date')
    y={}
    z={}
    for i in x:
        cnt=UpcomingIV.objects.filter(IVRequest=i)
        if(len(cnt)==0):
            k=Group.objects.filter(IVRequest=i).count()
            if k>i.IV.minimumCount:
                y.update({i:k})
        else:
            temp=[]
            for k in cnt:
                z[str(k.IVRequest.user.user.username)]=str(k.dateConf)
    sorted_x = sorted(y.items(), key=operator.itemgetter(1))
    un=[]
    for key in sorted_x:
        un+=[{'username':key[0].user.user.username,'date':str(key[0].date),'count':str(key[1])}]
    print(un)
    return render(request,"internships/IVListForAdmin.html",{'data':un,'IVId':IVId,'confirmed':z})
def confirmIV(request):
    if (request.user.profile.is_admin == False):
        return render(request, "internships/applyIV.html", {'IVId': str(IVId)})
    x=request.POST.get('data')
    IVId=request.POST.get('IVId')
    now = datetime.datetime.now()
    iv=IndustrialVisit.objects.filter(pk=IVId)
    ivr=IVRequest.objects.filter(IV=iv[0],user__user__username=x)
    cnt=Group.objects.filter(IVRequest=ivr[0])
    usn=[x.user for x in cnt]
    divr=IVRequest.objects.filter(IV=iv)
    for y in divr:
        if y.user in usn and y != ivr[0]:
            y.delete()
    kmp=Group.objects.filter(IVRequest__IV=iv)
    for y in kmp:
        if y.user in usn and y.IVRequest !=ivr:
            y.delete()
    print(usn)
    UpcomingIV.objects.create(IVRequest=ivr[0],dateConf=now)

    return JsonResponse({'data':"success"})
def cancleGroup(request):
    if (request.user.profile.is_admin == False):
        return render(request, "internships/applyIV.html", {'IVId': str(IVId)})
    x=request.POST.get('data')
    IVId=request.POST.get('IVId')
    IVRequest.objects.filter(user__user__username=x,IV__pk=IVId).delete()
    return JsonResponse({'data':"success"})
def DoneIv(request):
    if (request.user.profile.is_admin == False):
        return render(request, "internships/applyIV.html", {'IVId': str(IVId)})
    x=request.POST.get('data')
    IVId=request.POST.get('IVId')
    iv=IndustrialVisit.objects.filter(pk=IVId)
    d=DoneIV.objects.create(IV=iv[0])
    print('doneiv')
    print(d)
    ivr=IVRequest.objects.filter(user__user__username=x, IV__pk=IVId)
    grp=Group.objects.filter(IVRequest=ivr)
    for g in grp:
        PrevIV.objects.create(IV=d,user=g.user)
    IVRequest.objects.filter(user__user__username=x, IV__pk=IVId).delete()
    return JsonResponse({'data':"success"})

def notificationData(profile):
    x = RequestNotice.objects.filter(user=profile)
    data = []
    for y in x:
        temp = {}
        temp["label"] = "iv_request"
        ivData = {}
        ivData.update({'description': str(y.IVRequest.IV.description)})
        ivData.update({'company': str(y.IVRequest.IV.company)})
        ivData.update({'pk': str(y.pk)})
        ivData.update({'user': str(y.IVRequest.user.user.username)})
        temp["data"] = ivData
        temp["timestamp"] = y.timestamp
        data += [temp]
    print(data)
    return data


def notify(request):
    return render(request, "internships/notification.html")


def notificationResp(request):
    print("Yoo in notification Response")
    x = request.POST.get('response')
    print(x)
    print(request.POST.get('pk'))
    if (x == 'accept'):
        a = RequestNotice.objects.filter(pk=request.POST.get('pk'))
        print(a[0].IVRequest)
        Group.objects.create(IVRequest=a[0].IVRequest, user=request.user.profile)
        RequestNotice.objects.filter(pk=request.POST.get('pk')).delete()
    else:
        reqQset=  RequestNotice.objects.filter(pk=request.POST.get('pk'))
        for req in reqQset:
            Notice(user = req.IVRequest.user, header = "Deleted", message = req.IVRequest.user.user.username+" sent you request for "+req.IVRequest.IV.company.name, link="-", is_read = False, timestamp = req.timestamp).save()
            req.delete()
    return JsonResponse({"message": "success"})

def listOfMembers(request,IVId):
    yy = IndustrialVisit.objects.filter(pk=IVId)
    if (len(yy) == 0):
        return HttpResponse("<h1>you might have typed wrong url</h1>")
    ivid=IVId
    ivr=IVRequest.objects.filter(IV__pk=ivid,user=request.user.profile)
    if(len(ivr)!=1):
        return HttpResponse("<h1>failed...</h1>")
    g=Group.objects.filter(IVRequest=ivr[0])
    nig=RequestNotice.objects.filter(IVRequest=ivr[0])
    acc=[]
    rej=[]
    for i in g:
        acc+=[str(i.user.user.username)]
    for i in nig:
        rej+=[str(i.user.user.username)]
    print(acc)
    print(rej)
    return render(request,"internships/GroupMembers.html",{'acc':acc,'rej':rej,'len1':len(acc),'len2':len(rej)})

def uploadIndustryData(request):
    iid = request.POST.get('id')
    name = request.POST.get('name')
    description = request.POST.get('description')
    address = request.POST.get('address')
    mail = request.POST.get('mail')
    city = request.POST.get('city')
    website = request.POST.get('website')

    fs = request.FILES['file']
    f = open(os.path.abspath(os.path.dirname(__name__))+'/static/CompanyLogos/'+name+'.jpg','wb+')
    for chunks in fs.chunks():
        f.write(chunks)
    f.close()
    if iid!='':
        tmp = industry.objects.filter(pk=iid)
    if len(tmp)==1:
        tmp[0].name = str(name)
        tmp[0].logo = 'CompanyLogos/'+name+'.jpg'
        tmp[0].description = description
        tmp[0].address = address
        tmp[0].city = city
        tmp[0].mail = mail
        tmp[0].website = website
        tmp[0].save()
    else:
        industry(name=str(name),logo='CompanyLogos/'+name+'.jpg',description=description,address=address,city=city,mail=mail,website=website).save()
    return redirect('/adminaccess/')
