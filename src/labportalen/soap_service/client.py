# Python import
from zeep import Client, Transport

# Self import


class WsdlClient(object):
    def __init__(self, wsdl_url):
        self.wsdl_url = wsdl_url
        self.transport = Transport()

    def get_client(self):
        client = Client(wsdl=self.wsdl_url, transport=self.transport)
        return client
