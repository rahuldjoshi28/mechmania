from django.shortcuts import render,redirect
import json
from Accounts.models import User,Profile
from django.http import HttpResponse,JsonResponse
from .models import Project,ProjectRequest,ProjectGroup,ProjectNotice,AcceptedGroup
from internships.models import industry
from django.contrib.auth.decorators import login_required
import operator,datetime

from notifications.views import sendNotice

# Create your views here.
@login_required(login_url='/loginsignup.html')
def projects(request,page = 1, query = None):
    page=int(page)
    if page<=0:
        redirect('/')
    x=page*10
    y=x-10
    if query == None:
        pro=Project.objects.all()
    else:
        from django.db.models import Q
        from functools import reduce
        constrainList = query.split(" ")
        constrin = [Q(type__icontains=a) | Q(description__icontains=a) | Q(company__name__icontains=a) | Q(
            company__address__icontains=a) for a in
                    constrainList]
        pro = Project.objects.all().filter(reduce(operator.and_, constrin))
    print(y)
    noOfEntry=industry.objects.filter(pk__in=[pr.company.pk for pr in pro]).count()
    print(noOfEntry)
    if noOfEntry<y:
        page = str(page)
        redirect('projects/'+page+'/')
    ind=industry.objects.filter(pk__in=[pr.company.pk for pr in pro])
    ind=ind[y:x]
    print(ind)
    data=[]
    cannotapply="no"
    for i in ind:
        proj=Project.objects.filter(company=i)
        projectData=[]
        for p in proj:
            strx="apply"
            req=ProjectRequest.objects.filter()
            if len(req)>0:
                strx="applied"
                if AcceptedGroup.objects.filter(ProjectRequest=req).count()>0:
                    strx="confirmed"
                    cannotapply="yes"
            r = ProjectGroup.objects.filter(user=request.user.profile)
            for r1 in r:
                if AcceptedGroup.objects.filter(ProjectRequest=r1.ProjectRequest).count() > 0 and r1.ProjectRequest.project == p:
                    strx = "confirmed"
                    cannotapply = "yes"
            projectData+=[[p,strx]]
        l={}
        l.update({'name':i.name})
        l.update({'pk': i.pk})
        l.update({'description': i.description})
        l.update({'logo': "/"+i.logo.url.split("/",1)[1]})
        data+=[[l,projectData]]
    admin="no"
    if request.user.profile.is_admin:
        admin="yes"
    print(data)
    if query == None:
        return render(request,"project/projects.html",{'projects':data,'admin':admin,'capply':cannotapply})
    else:
        print("Project dtaa is = ", data)
        return {'projects':data,'admin':admin,'capply':cannotapply}

@login_required(login_url='/loginsignup.html')
def RecomandUsers(request):
    intial=str(request.POST.get("initials"))
    print("debug"+intial)
    ivid=str(request.POST.get("ProjectId"))
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

@login_required(login_url='/loginsignup.html')
def apply(request,projectId):
    x = ProjectRequest.objects.filter(project__pk=projectId, user=request.user.profile)
    y = Project.objects.filter(pk=projectId)
    if (len(y) == 0):
        return HttpResponse("<h1>you might have typed wrong url</h1>")
    if (y[0].isavailable == 'na'):
        return HttpResponse("<h1>this IV is curently not available</h1>")
    if (len(x) > 0):
        return HttpResponse("<h1>Are you kidding...</h1>")
    k=Project.objects.filter(pk=projectId)
    cnt=k[0].minimumCnt-1
    return render(request, "project/applyProject.html", {'projectId': str(projectId),'minimumCnt':cnt})

@login_required(login_url='/loginsignup.html')
def CreatingGroup(request,projectId):
    data=request.POST.get('data')
    dt=json.loads(data)
    pro=Project.objects.filter(pk=projectId)
    if len(pro)==0:
        return JsonResponse({'data': "no such iv"})
    y = pro[0].minimumCnt
    dtt=[]
    for i in dt:
        x=User.objects.filter(username=i)
        if x!=None and not(x in dtt) and x != request.user:
            dtt+=[x]
    if((len(dtt)+1)<y):
        return JsonResponse({'data': "you have selected less number of users than required for iv"})
    pr = ProjectRequest.objects.create(project=pro[0], user=request.user.profile)
    print("creategrp")
    print(dtt)
    for i in dtt:
        xx=Profile.objects.filter(user=i)
        print("java")
        print(xx)
        ProjectNotice.objects.create(user=xx[0],ProjectRequest=pr)
    ProjectGroup.objects.create(ProjectRequest=pr,user=request.user.profile)
    return JsonResponse({'data': "Success"})

@login_required(login_url='/loginsignup.html')
def projectNotificationData(request):
    x=ProjectNotice.objects.filter(user=request.user.profile)
    data=[]
    for y in x:
        temp={}
        temp["label"] = "project_request"

        pron = {}

        pron.update({'description':str(y.ProjectRequest.project.description)})
        pron.update({'company': str(y.ProjectRequest.project.company)})
        pron.update({'type': str(y.ProjectRequest.project.type)})
        pron.update({'pk': str(y.pk)})
        pron.update({'user':str(y.ProjectRequest.user.user.username)})
        temp["data"] = pron

        temp["timestamp"] = y.timestamp
        data += [temp]
    print(data)
    return data
    #return JsonResponse({'data':data})

@login_required(login_url='/loginsignup.html')
def notify(request):
    return render(request,"project/notification.html")

@login_required(login_url='/loginsignup.html')
def notificationResp(request):
    x=request.POST.get('response')
    print(x)
    print(request.POST.get('pk'))
    if(x=='accept'):
        a=ProjectNotice.objects.filter(pk=request.POST.get('pk'))
        #print(a[0].ProjectRequest)
        ProjectGroup.objects.create(ProjectRequest=a[0].ProjectRequest,user=request.user.profile)

        ProjectNotice.objects.filter(pk=request.POST.get('pk')).delete()
    else:
        ProjectNotice.objects.filter(pk=request.POST.get('pk')).delete()
    return HttpResponse("<h1>success</h1>")

@login_required(login_url='/loginsignup.html')
def listOfApplicants(request,projectId):
    if(request.user.profile.is_admin==False):
        return redirect('/projects/1/')
    yy=Project.objects.filter(pk=projectId)
    if(len(yy)==0):
        return redirect('/projects/1/')
    x=ProjectRequest.objects.filter(project__pk=projectId).order_by('-date')
    y={}
    z={}
    for i in x:
        cnt=AcceptedGroup.objects.filter(ProjectRequest=i)
        if(len(cnt)==0):
            k=ProjectGroup.objects.filter(ProjectRequest=i).count()
            if k>i.project.minimumCnt:
                y.update({i:k})
        else:
            temp=[]
            for k in cnt:
                z[str(k.ProjectRequest.user.user.username)]=str(k.dateConf)
    sorted_x = sorted(y.items(), key=operator.itemgetter(1))
    un=[]
    for key in sorted_x:
        un+=[{'username':key[0].user.user.username,'date':str(key[0].date),'count':str(key[1])}]
    un.reverse()
    print(un)
    return render(request,"project/ProjectListForAdmin.html",{'data':un,'projectId':projectId,'confirmed':z})
@login_required(login_url='/loginsignup.html')
def confirm(request):
    if (request.user.profile.is_admin == False):
        return redirect('/projects/1/')
    x=request.POST.get('data')
    projectId=request.POST.get('projectId')
    now = datetime.datetime.now()
    pro=Project.objects.filter(pk=projectId)
    pr=ProjectRequest.objects.filter(project=pro[0],user__user__username=x)
    cnt=ProjectGroup.objects.filter(ProjectRequest=pr[0])
    usn=[x.user for x in cnt]
    divr=ProjectRequest.objects.filter(project=pro[0])
    for y in divr:
        if y.user in usn and y != pr[0]:
            y.delete()
    kmp=ProjectGroup.objects.filter(ProjectRequest__project=pro[0])
    for y in kmp:
        if y.user in usn and y.ProjectRequest !=pr[0]:
            sendNotice(usr, "Your project group is confirmed for "+y.ProjectRequest.project.company.name+" industry", "Project Request")
            y.delete()
    print(usn)
    AcceptedGroup.objects.create(ProjectRequest=pr[0],dateConf=now)
    return JsonResponse({'data':"success"})
@login_required(login_url='/loginsignup.html')
def cancleGroup(request):
    if (request.user.profile.is_admin == False):
        return redirect('/projects/1/')
    x=request.POST.get('data')
    projectId=request.POST.get('projectId')

    from Accounts.models import Profile
    usr = Profile.objects.get(user_username = x)

    ProjectRequest.objects.filter(user__user__username=x,project__pk=projectId).delete()


    sendNotice(usr, "Sorry your project request is rejected", "Project Request")

    return JsonResponse({'data':"success"})
@login_required(login_url='/loginsignup.html')
def closeProject(request):
    if (request.user.profile.is_admin == False):
        return redirect('/projects/1/')
    projectId = request.POST.get('projectId')
    ProjectRequest.objects.filter(project__pk=projectId).delete()
    Project.objects.filter(pk=projectId).update(isavailable='no')
    return JsonResponse({'data': "success"})
@login_required(login_url='/loginsignup.html')
def groupInfo(request,projectId):
    yy = Project.objects.filter(pk=projectId)
    if (len(yy) == 0):
        return redirect('/projects/1/')
    proid=projectId
    pr=ProjectRequest.objects.filter(project__pk=proid,user=request.user.profile)
    if(len(pr)!=1):
        return redirect('/projects/1/')
    g=ProjectGroup.objects.filter(ProjectRequest=pr[0])
    nig=ProjectNotice.objects.filter(ProjectRequest=pr[0])
    acc=[]
    rej=[]
    for i in g:
        acc+=[str(i.user.user.username)]
    for i in nig:
        rej+=[str(i.user.user.username)]
    print(acc)
    print(rej)
    return render(request,"project/GroupMembers.html",{'acc':acc,'rej':rej,'len1':len(acc),'len2':len(rej)})
def getProjects(ind,usr):
    data = []
    cannotapply = "no"
    for i in ind:
        proj = Project.objects.filter(company=i)
        projectData = []
        for p in proj:
            strx = "apply"
            req = ProjectRequest.objects.filter(user = usr.profile, project=p)
            print("in loop ", req)
            if len(req) > 0:
                strx = "applied"
                if AcceptedGroup.objects.filter(ProjectRequest=req).count() > 0:
                    strx = "confirmed"
                    cannotapply = "yes"
            r = ProjectGroup.objects.filter(user=usr.profile)
            for r1 in r:
                if AcceptedGroup.objects.filter(ProjectRequest=r1.ProjectRequest).count() > 0 and r1.ProjectRequest.project == p:
                    strx = "confirmed"
                    cannotapply = "yes"
            projectData += [[p, strx]]
        data = projectData
    admin = "no"
    if usr.profile.is_admin:
        admin = "yes"
    print(" projects are ", data)
    return {'data': data, 'admin': admin, 'capply': cannotapply}
