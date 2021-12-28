from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.module_loading import import_string
from django.urls import reverse
from django.conf import settings
import pdb
import json

from django_esign.hello_sign import webhook_handling as hs_web_handle

from threading import Thread

# Create your views here.

def hello_sign_process(request_body):
    if hasattr(hs_web_handle, request_body['event']['event_type']):
        print(request_body['event']['event_type'])
        getattr(hs_web_handle, request_body['event']['event_type'])(request_body, import_string(settings.HELLO_SIGN_WEBHOOK_PROCESS))

@csrf_exempt
@require_POST
def webhook_hellosign(request):
    context = {"event_message": "Hello API Event Received."}
    params = dict()
    response = dict()
    json_data = request.POST['json']
    request_body = json.loads(json_data)
    print(request_body)
    if 'signature_request' in request_body:
        Thread(target=hello_sign_process, args=(request_body, )).start()
        print("Returing response")
        return JsonResponse(data=context, status=200)
    elif 'event' in request_body and 'event_type' in request_body['event'] and request_body['event']['event_type'] == "callback_test":
        return JsonResponse(data=context, status=200)
    else:
        return JsonResponse(data=context, status=500)