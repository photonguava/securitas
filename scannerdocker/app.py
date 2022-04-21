#!/usr/bin/env python
import time
from pprint import pprint
from zapv2 import ZAPv2
import sys
import requests

project_id = sys.argv[2]
apiKey = 'changeme'
target = str(sys.argv[1])
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://localhost:8080'})

print('Spidering target {}'.format(target))
# The scan returns a scan id to support concurrent scanning
while True:
    try:
        scanID = zap.spider.scan(target)
        break
    except:
        pass
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))


print('Active Scanning target {}'.format(target))
scanID = zap.ascan.scan(target)
print(scanID)
alert_dict = dict()
while int(zap.ascan.status(scanID)) < 100:
    alerts = zap.core.alerts(baseurl=target)
    for alert in alerts:
        if alert.get('alert') in alert_dict:
            continue
        else:
            alert_details = {'title':alert.get('alert'),'description':alert.get('description'),'fixes':alert.get('solution'),'severity':alert.get('risk'),'refs':alert.get('reference'),'url':alert.get('url')}
            requests.post("http://host.docker.internal:8000/projects/"+project_id+"/vulnerabilities",json=alert_details)
            alert_dict[alert.get('alert')] = True
    time.sleep(5)