from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.core.mail import send_mail
from django.views.decorators.http import require_http_methods

from .models import *

from django.db import IntegrityError

# Create your views here.
def email_test(request):
    email_send = send_mail(
        'Subject',
        'Message.',
        'kyawhtet.today@gmail.com',
        ['cgwlink.combine@gmail.com', 'kfirstthree@gmail.com'],
    )
    return HttpResponse(email_send)


def home(request):
    
    context = {}
    return render(request, 'home.html', context)

@require_http_methods(["POST"])
def contact_us(request):

    status = False
    msg = ''
    invalid_field = ''

    # get all the request 
    rq_name = request.POST['name']
    rq_email = request.POST['email']
    rq_subject = request.POST['subject']
    rq_message = request.POST['message']

    # save in the database 
    contact = Contact(name=rq_name, email=rq_email, subject=rq_subject, message=rq_message)
    
    try:
        contact.save()
        status = True
    except IntegrityError as e:
        status = False
        msg = str(e.__cause__)
        invalid_field = msg.split('.')[1]
        msg = msg.split('.')[1] + ' is already exit'

    if status:
        # send email 
        email_send = send_mail(
            rq_subject,
            rq_message,
            'kyawhtet.today@gmail.com',
            [rq_email],
        )

        if not email_send:
            msg = 'Your email is invalid'
            status = False
        else:
            msg = 'You just send successfully!'
            status = True

    response  = {
        'status': status,
        'msg': msg,
        'invalid_field': invalid_field
    }

    return JsonResponse(response)
