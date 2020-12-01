from django.conf import settings
from django_esign.models import *
import pdb

def signature_request_sent(hello_sign_event):
    # hello_sign_event['signature_request']['metadata'] Metadata
    # hello_sign_event['signature_request']['signatures'] Signatures
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
            esign_obj = EsignCreds.objects.get(unique_id = esign_id)
        except EsignCreds.DoesNotExist:
            pass
        else:
            esign_obj.set_signers(l_signers)
            esign_obj.set_creds(creds)
            esign_obj.set_signers_status(l_signers_status)
            esign_obj.save()

#def 