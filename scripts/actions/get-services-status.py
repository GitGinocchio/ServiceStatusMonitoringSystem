from dataclasses import dataclass, field
from datetime import datetime, timezone
from requests import Response
from os import path
from os import makedirs
import requests
import json

def extendavg(avg : float, n : int, element : float): return (avg * n + element) / (n + 1)

session = requests.Session()

@dataclass
class Status:
    name : str
    url : str
    description : str

    response : Response = field(default_factory=lambda : None,init=False)

    timestamp : str = field(default_factory=lambda : datetime.now(timezone.utc).isoformat(), init=False)
    status : str = field(default_factory=lambda: None,init=False)
    code : int = field(default_factory=lambda: None, init=False)
    latency : float = field(default_factory=lambda : None, init=False)

    overall : dict[str, float] = field(default_factory=lambda: {
        "avg-latency" : 0.0,

        "avg-uptime" : 0.0,
        "avg-uptime-percentage" : 0.0,
        
        "avg-downtime" : 0.0,
        "avg-downtime-percentage" : 0.0
    },init=False,repr=False)
    metrics : list[dict] = field(default_factory=lambda: [],init=False,repr=False)
    notes : list[dict] = field(default_factory=lambda: [],init=False,repr=False)
    reports : list[dict] = field(default_factory=lambda: [],init=False,repr=False)

    def __post_init__(self):
        self.response : Response = session.get(self.url,timeout=2.5)

        self.latency = self.response.elapsed.total_seconds()
        self.code = self.response.status_code
        self.status = self.response.reason

    def update(self):
        if (n_metrics:=len(self.metrics)) >= 1:
            uptime_percentage = extendavg(self.metrics[-1]["uptime-percentage"],n_metrics, 100.0 if self.code == 200 else 0.0)
            downtime_percentage = extendavg(self.metrics[-1]["downtime-percentage"],n_metrics, 100.0 if self.code != 200 else 0.0)

            seconds_passed = (datetime.fromisoformat(self.timestamp) - datetime.fromisoformat(self.metrics[-1]['timestamp'])).total_seconds()

            if self.metrics[-1]['code'] == self.code and self.code == 200:
                uptime = float(self.metrics[-1]['uptime']) + seconds_passed
                downtime = 0.0
            elif self.metrics[-1]['code'] == self.code and self.code != 200:
                downtime = float(self.metrics[-1]['downtime']) + seconds_passed
                uptime = 0.0
            else:
                uptime = 0.0
                downtime = 0.0
        else:
            uptime_percentage = 100.0 if self.code == 200 else 0.0
            downtime_percentage = 100.0 if self.code != 200 else 0.0
            
            uptime = 0.0
            downtime = 0.0

        avg_latency = extendavg(self.overall['avg-latency'], n_metrics, self.latency)
        avg_uptime = extendavg(self.overall['avg-uptime'], n_metrics, uptime)
        avg_downtime = extendavg(self.overall['avg-downtime'], n_metrics, downtime)
        avg_uptime_percentage = extendavg(self.overall['avg-uptime-percentage'], n_metrics, uptime_percentage)
        avg_downtime_percentage = extendavg(self.overall['avg-downtime-percentage'], n_metrics, downtime_percentage)

        self.metrics.append({
            "uptime-percentage" : uptime_percentage,
            "downtime-percentage" : downtime_percentage,
            "uptime" : uptime,
            "downtime" : downtime,
            "latency": self.latency,
            "overall" : {
                "avg-latency": avg_latency,
                "avg-uptime" : avg_uptime,
                "avg-downtime" : avg_downtime,
                "avg-uptime-percentage" : avg_uptime_percentage,
                "avg-downtime-percentage": avg_downtime_percentage
            },
            "code" : self.code,
            "status" : self.status,
            "timestamp" : self.timestamp
        })

        self.overall['avg-latency'] = avg_latency
        self.overall['avg-uptime'] = avg_uptime
        self.overall['avg-downtime'] = avg_downtime
        self.overall['avg-uptime-percentage'] = avg_uptime_percentage
        self.overall['avg-downtime-percentage'] = avg_downtime_percentage

    def load(self):
        if not path.exists(service_path:=f'./data/services/{self.name.lower()}/{self.name.lower()}.json'): return
        with open(service_path,'r') as f: content : dict = json.load(f)

        self.metrics = content.get('metrics',self.metrics)
        self.overall = content.get('overall',self.overall)
        self.reports = content.get('reports',self.reports)
        self.notes = content.get('notes',self.notes)

    def add_note(self): pass

    def add_report(self): pass

    def save(self):
        makedirs(f'./data/services/{self.name.lower()}/graphs',exist_ok=True)
        with open(f'./data/services/{self.name.lower()}/{self.name.lower()}.json','w') as f: 
            json.dump({
                'name' : self.name,
                'description' : self.description,
                'url' : self.url,
                'timestamp' : self.timestamp,
                'status' : self.status,
                'code' : self.code,
                'latency' : self.latency,
                'overall' : self.overall,
                'metrics' : self.metrics,
                'reports' : self.reports,
                'notes' : self.notes,
            },f, indent='\t')

with open('./data/services.json','r') as f:
    services : list = json.load(f)['list']

for service in services:
    status = Status(service['name'],service['url'],service['description'])
    status.load()
    status.update()
    status.save()