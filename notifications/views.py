from django.shortcuts import render
from .models import Notice
from django.http import JsonResponse
from internships.views import notificationData
from django.contrib.auth.decorators import login_required
from internships.models import RequestNotice
from operator import itemgetter

def get_message(user):
    genNotices = [a for a in Notice.objects.filter(user = user)]
    iv_request = notificationData(user)
    from project.views import projectNotificationData
    projects = projectNotificationData(user)

    messages = []
    for a in genNotices:
        messages.append(a.as_dict())
        a.is_read = True
        a.save(update_fields = ["is_read"])
    genNotices = messages + iv_request + projects
    messages = sorted(genNotices[:5], key=itemgetter("timestamp"), reverse=True)
    print (messages)
    return messages

def sendNotice(user, message, header = "message"):
    Notice(user = user, header = header, message = message).save()

@login_required
def delete_notice(request):
    reqId = request.POST.get("reqId")
    type= request.POST.get("type")
    print("kay challay")
    print("\nheyy in delete ", reqId, " ", type)
    if type == "iv_request":
        RequestNotice.objects.filter(pk = reqId).delete()
    else:
        Notice.objects.filter(pk = reqId).delete()
    return JsonResponse({"message": "success"})

def return_messages(request):
    print ("heyy there")
    return JsonResponse({"messages": get_message(request.user.profile)})

def get_count(user):
    return  len(Notice.objects.filter(user = user, is_read = False))