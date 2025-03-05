from hubspot import HubSpot
from hubspot.crm.objects import api as hbAPI

class HubSpotClient():
    
    def __init__(self):
        self.client = HubSpot()
        return self.client
        
    def __init__(self, access_token):
        self.access_token = access_token
        self.client = HubSpot(access_token=access_token)
        return self.client