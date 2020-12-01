from django_esign.hello_sign.esign import *

def send_signature_request(params, response):
    try:
        params['hello_sign']
    except KeyError:
        pass
    else:
        response['hello_sign'] = dict()
        hello_sign_send_signature_request(params['hello_sign'], response['hello_sign'])

def send_custom_signature_request(params, response):
    try:
        params['hello_sign']
    except KeyError:
        pass
    else:
        response['hello_sign'] = dict()
        response['hello_sign']['return_value'] = hello_sign_send_custom_signature_request(params['hello_sign'], response['hello_sign'])

def get_embed_url(params, response):
    try:
        params['hello_sign']
    except KeyError:
        pass
    else:
        response['hello_sign'] = dict()
        response['hello_sign']['return_value'] = hello_sign_get_embed_url(params['hello_sign'], response['hello_sign'])