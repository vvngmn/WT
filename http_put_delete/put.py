import requests
class request:
    def __init__(self,url,value,payload):
        self.url = url
        self.value = value
        self.payload = payload
        self.urlnew = self.url + self.value
    def create(self):
        r = requests.put(self.urlnew, data=self.payload) # params 用于post delete和data用于put和get
        print r.status_code 
       # print r.json()
    def get(self):
        r = requests.get(self.urlnew)
        print r.status_code
        print r.json()

#    def post(post):


if __name__ == "__main__":
    urla = "http://10.17.122.100:8081/mxos/mailbox/v2/"
    payload1 = {'cosId':'default','password':'p' }
    p = request(urla,"uc@openwave.com",payload1)
    p.create()
    p.get()