from django.db import models
from django.utils import timezone
import datetime as dt
import json

# Create your models here.
class Bitmap():
    #Methods
    def setFlag(self, bit):
        self.flag = (self.flag | (0x01 << bit))
        return self.flag

    def resetFlag(self, bit):
        self.flag &= ~(0x01 << bit)
        return self.flag

    def isFlagValid(self, bit):
        flag = (self.flag & (0x01 << bit))
        if flag == 0:
            return False
        else:
            return True

class EsignCreds(models.Model, Bitmap):
    unique_id = models.IntegerField()
    service = models.TextField()
    creds = models.TextField()
    signers = models.TextField() #List of all signers
    signers_role = models.TextField() #List of all signer roles
    signers_status = models.TextField() #List of all signer status
    flag = models.IntegerField(default=0)

    def set_creds(self, creds):
        self.creds = json.dumps(creds)

    def get_creds(self):
        return json.loads(self.creds)

    def set_signers(self, signers):
        self.signers = json.dumps(signers)

    def set_signers_role(self, signer_roles):
        self.signers_role = json.dumps(signer_roles)

    def set_signers_status(self, signer_status):
        self.signers_status = json.dumps(signer_status)

    def set_draft(self):
        self.setFlag(1)

    def reset_draft(self):
        self.resetFlag(1)

    def check_draft(self):
        return self.isFlagValid(1)