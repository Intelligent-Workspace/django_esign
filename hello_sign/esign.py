from django.conf import settings
from django_esign.models import *
import pdb

client = settings.HELLO_SIGN_CLIENT
test_mode = settings.HELLO_SIGN_ENVIRONMENT
client_id = settings.HELLO_SIGN_CLIENT_ID

def hello_sign_send_signature_request(params, response):
    #These are required arguments
    is_embedded = params['is_embedded']
    signers = params['signers']
    title = params['title']
    subject = params['subject']
    message = params['message']
    esign_id = params['esign_id']
    has_file_parameter = False
    file_type = None
    service = "hellosign"

    #This is to check and configure whether the file is specificed by path or url
    try:
        params['files']
        has_file_parameter = True
        file_type = "path"
    except KeyError:
        pass
    try:
        params['files_url']
        has_file_parameter = True
        file_type = "url"
    except KeyError:
        pass
    if has_file_parameter == True:
        #Based on whether the signature is embedded or not, this is setting the caller api to call
        if is_embedded:
            caller_name = "send_signature_request_embedded"
        else:
            caller_name = "send_signature_request"
        #This dictionary are the arguments that are being passed into the api call
        arguments = dict()
        arguments['test_mode'] = test_mode 
        arguments['client_id'] = client_id 
        arguments['title'] = title
        arguments['subject'] = subject
        arguments['message'] = message
        arguments['signers'] = signers
        arguments['metadata'] = {'esign_id': esign_id}
        if file_type == "path":
            arguments['files'] = params['files']
        else:
            arguments['file_urls'] = params['files_url']

        signature_request = getattr(client, caller_name)(**arguments)
        if is_embedded:
            #If the signature is embedded, then for each signer a dictionary is being compiled where the key is the email and the value is the signature_id
            d_response = dict()
            l_signers = list()
            l_signers_status = list()
            for signature in signature_request.signatures:
                email_address = signature.signer_email_address
                d_response[email_address] = signature.signature_id
                l_signers.append(email_address)
                l_signers_status.append("awaiting_signature")
            try:
                esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
            except EsignCreds.DoesNotExist:
                esign_obj = EsignCreds(unique_id=esign_id, service=service)
                esign_obj.set_signers(l_signers)
                esign_obj.set_creds(d_response)
                esign_obj.set_signers_status(l_signers_status)
                esign_obj.save()
            response['signer_response'] = d_response
    else:
        response['error'] = "No file parameters."

def hello_sign_send_custom_signature_request(params, response):
    #These are required arguments
    signers = params['signers']
    is_embedded = params['is_embedded']
    requester_email = params['requester_email']
    skip_requester = params['skip_requester']
    subject = params['subject']
    message = params['message']
    esign_id = params['esign_id']
    has_file_parameter = False
    file_type = None
    service = "hellosign"

    #This is to check and configure whether the file is specificed by path or url
    try:
        params['files']
        has_file_parameter = True
        file_type = "path"
    except KeyError:
        pass
    try:
        params['files_url']
        has_file_parameter = True
        file_type = "url"
    except KeyError:
        pass
    if has_file_parameter == True:
        #Based on whether the signature is embedded or not, this is setting the caller api to call
        caller_name = "create_embedded_unclaimed_draft"
        l_signers = list()
        for signer in signers:
            l_signers.append(signer['email_address'])
        #This dictionary are the arguments that are being passed into the api call
        arguments = dict()
        arguments['test_mode'] = test_mode 
        arguments['client_id'] = client_id
        arguments['draft_type'] = "request_signature"
        arguments['subject'] = subject
        arguments['message'] = message
        arguments['signers'] = signers
        arguments['requester_email_address'] = requester_email
        arguments['is_for_embedded_signing'] = is_embedded
        arguments['skip_me_now'] = skip_requester
        arguments['metadata'] = {'esign_id': esign_id, 'embedded_signing': is_embedded}
        if file_type == "path":
            arguments['files'] = params['files']
        else:
            arguments['file_urls'] = params['files_url']

        signature_request = getattr(client, caller_name)(**arguments)
        try:
            esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
        except EsignCreds.DoesNotExist:
            esign_obj = EsignCreds(unique_id=esign_id, service=service, service_document_id=signature_request.signature_request_id)
            esign_obj.set_signers(l_signers)
            esign_obj.set_draft()
            esign_obj.save()
            response['claim_url'] = signature_request.claim_url
            return True
        else:
            response['error'] = "EsignCreds with this unique id exists"
            return False
    else:
        response['error'] = "No file parameters."
        return False

def hello_sign_cancel_signature_request(params, response):
    esign_id = params['esign_id']
    service = "hellosign"

    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        response['error'] = "This signature does not exist in sign request"
        return False
    else:
        try:
            test = client.cancel_signature_request(esign_obj.get_creds()["signature_request_id"])
        except Exception:
            response['error'] = "There seems to be something wrong with this cancel request"
            return False
        else:
            return True

def hello_sign_get_embed_url(params, response):
    esign_id = params['esign_id']
    email = params['email']
    service = "hellosign"

    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        response['error'] = "This signature is not stored in db"
        return False
    else:
        try:
            signature_id = esign_obj.get_creds()[email]
        except KeyError:
            response['error'] = "This signer does not exist in sign request"
            return False
        else:
            response['embed_url'] = client.get_embedded_object(signature_id).sign_url
            return True

def hello_sign_get_current_file(params, response):
    esign_id = params['esign_id']
    service = "hellosign"

    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        response['error'] = "This signature is not stored in db"
        return False
    else:
        response['file_url'] = client.get_signature_request_file(esign_obj.get_creds()["signature_request_id"], file_type="pdf", response_type="url")["file_url"]
        return True

def hello_sign_get_signers_status(params, response):
    esign_id = params['esign_id']
    service = "hellosign"

    try:
        esign_obj = EsignCreds.objects.get(unique_id=esign_id, service=service)
    except EsignCreds.DoesNotExist:
        response['error'] = "This signature is not stored in db"
        return False
    else:
        response['emails'] = esign_obj.get_signers()
        response['statuss'] = esign_obj.get_signers_status()
        return True