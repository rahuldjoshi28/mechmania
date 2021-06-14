from __future__ import unicode_literals
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
from AdminAccess import models
from django.contrib import messages

from notifications.models import Notice
from internships.models import industry as IndustryModel
from internships.views import getInternships
from notifications.views import get_message
from project.views import getProjects

def index(request):
    quotes = models.Quotes.objects.all()
    return render(request, 'index.html', {'Quotes': quotes})

def industry(request, industryName):
    # fetch data of industry here
    ind = IndustryModel.objects.get(name = industryName)
    indData = {}

    indData["name"] = ind.name
    indData["description"] = ind.description
    indData["logo"] = "/"+ind.logo.url.split("/",1)[1]
    indData["internships"] = getInternships(ind, request.user)
    indData["projects"] = getProjects([ind], request.user)
    print(indData)
    return render(request, 'industry.html', {"data": indData})

def internshipsandvisits(request, ):
    return render(request, 'internshipsandvisits.html', {})

def contact_us(request):
    try:
        subject = '' + request.POST.get('fullname') + ' contacted using "Contact Us" form.'
        message = 'Sender\'s mail: ' + request.POST.get('email') + '\n\nMessage:\n\n' + request.POST.get('message')
        frommail = 'rathirohitg1997@gmail.com'
        tomail = 'rathirohitg1997@gmail.com'
        send_mail(
            subject,
            message,
            frommail,
            [tomail],
            fail_silently=False,
        )
    except:
        return HttpResponse("fail")
    return HttpResponse("pass")


def aboutus(request):
    return render(request, 'aboutus.html', {})

def search(request):
    query = request.GET.get("query")
    intData = []
    ivData = []
    qpData = []
    projectData = []
    recData = []
    print("asdasdasdasdasdasdasdasdas\n\n\n\n\n\n\n\n\n")
    from recruitments.views import getData
    recData = getData(request, query)

    from internships.views import getIVs
    ivData = getIVs(request, query)

    from internships.views import searchInternships
    intData = searchInternships(request, query)

    from questionPapers.views import getPaperList2
    qpData = getPaperList2(request, query)

    from project.views import projects
    projectData = projects(request, 1, query)

    print("Here comes search data")
    print("internships ", intData)
    print ("\nIV ", ivData)
    print("\n recruitments ", recData)
    print("\n qpapers ", qpData)

    return render(request, "searchpage.html", {"internships": intData, "ivs": ivData, "recruitments": recData, "qpapers": qpData, "projectData": projectData})
"""
def search(request):
    query = request.GET.get("query")
    intData = []
    ivData = []
    qpData = []
    projectData = []
    recData = []

    from recruitments.views import getData
    recData = getData(request, query)

    from internships.views import getIVs
    ivData = getIVs(request, query)

    from internships.views import searchInternships
    intData = searchInternships(request, query)

    from questionPapers.views import getPaperList2
    qpData = getPaperList2(request, query, "list")
    print("queation papers =========== ", qpData)
    return render(request, "searchpage.html", {"internships": intData , "ivs": ivData, "recruitments": recData, "qpapers": qpData, "li": range(0, len(qpData))})
"""
# Error Pages
def server_error(request):
    return render(request, 'errors/500.html')


def not_found(request):
    return render(request, 'errors/404.html')


def permission_denied(request):
    return render(request, 'errors/403.html')


def bad_request(request):
    return render(request, 'errors/400.html')

def notifications(request):
	if request.user.is_authenticated():
		user = request.user.profile
		genNotices = get_message(user)
		# do same for industrial visit notices
        # merge and sort both list
		print(genNotices)
		return render(request, 'notifications.html', {"notices":genNotices})
	else:
		messages.info(request, "Sorry nedd to log in first")
		return render(request, "index.html", {})
