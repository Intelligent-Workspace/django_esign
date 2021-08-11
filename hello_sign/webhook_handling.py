from django.conf import settings
from django_esign.models import *
import pdb

def signature_request_sent(hello_sign_event, callback):
    # hello_sign_event['signature_request']['metadata'] Metadata
    # hello_sign_event['signature_request']['signatures'] Signatures
    service = "hellosign"
    metadata = hello_sign_event['signature_request']['metadata']
    signatures = hello_sign_event['signature_request']['signatures']

    esign_id = int(metadata['esign_id'])
    is_embedded = bool(metadata['embedded_signing'])
    if is_embedded:
        l_signers = list()
        l_signers_status = list()
        creds = dict()
        for sign in signatures:
            email_address = sign['signer_email_address']
            sign_id = sign['signature_id']
            l_signers.append(email_address)
            l_signers_status.append("awaiting_signature")
            creds[email_address] = sign_id
        creds['files_url'] = hello_sign_event['signature_request']['files_url']
        creds['signature_request_id'] = hello_sign_event['signature_request']['signature_request_id']
        try:
            esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
        except EsignCreds.DoesNotExist:
            pass
        else:
            esign_obj.set_signers(l_signers)
            esign_obj.set_creds(creds)
            esign_obj.set_signers_status(l_signers_status)
            esign_obj.save()
        params = dict()
        params['service'] = "hellosign"
        params['esign_id'] = esign_id
        params['signers'] = esign_obj.get_signers()
        params['signer_status'] = esign_obj.get_signers_status()
        params['event'] = "signature_sent"
        callback(params)

def signature_request_signed(hello_sign_event, callback):
    service = "hellosign"
    metadata = hello_sign_event['signature_request']['metadata']
    signatures = hello_sign_event['signature_request']['signatures']
    esign_id = metadata['esign_id']
    """
    signatures is a list
    gives the email of the signer - signatures['signer_email_address']
    status of the signer - signatures['status_code']
    esign_id - metadata['esign_id']
    """
    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        pass
    else:
        for sign in signatures:
            esign_obj.update_signer_status(sign['signer_email_address'], sign['status_code'])
            esign_obj.save()
        params = dict()
        params['service'] = "hellosign"
        params['esign_id'] = esign_id
        params['event'] = "signed"
        params['signers'] = esign_obj.get_signers()
        params['signer_status'] = esign_obj.get_signers_status()
        callback(params)

def signature_request_all_signed(hello_sign_event, callback):
    service = "hellosign"
    metadata = hello_sign_event['signature_request']['metadata']
    esign_id = metadata['esign_id']
    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        pass
    else:
        esign_obj.set_all_signed()
        esign_obj.save()
        params = dict()
        params['service'] = "hellosign"
        params['esign_id'] = esign_id
        params['event'] = "all_signed"
        params['signers'] = esign_obj.get_signers()
        params['signer_status'] = esign_obj.get_signers_status()
        callback(params)

def signature_request_declined(hello_sign_event, callback):
    service = "hellosign"
    metadata = hello_sign_event['signature_request']['metadata']
    esign_id = metadata['esign_id']
    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        pass
    else:
        esign_obj.delete()
        params = dict()
        params['service'] = "hellosign"
        params['esign_id'] = esign_id
        params['event'] = "signature_cancelled"
        callback(params)

def signature_request_canceled(hello_sign_event, callback):
    service = "hellosign"
    metadata = hello_sign_event['signature_request']['metadata']
    esign_id = metadata['esign_id']
    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        pass
    else:
        esign_obj.delete()
        params = dict()
        params['service'] = "hellosign"
        params['esign_id'] = esign_id
        params['event'] = "signature_cancelled"
        callback(params)