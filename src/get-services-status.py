from status import Status
import json


with open('./data/services.json','r') as f:
    services : list = json.load(f)['services']

for service in services:
    status = Status(service['name'],service['url'],service['description'])
    status.load()
    status.update()
    status.save()