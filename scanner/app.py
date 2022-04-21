#!/usr/bin/env python
import time
from pprint import pprint
from zapv2 import ZAPv2
import requests
apiKey = 'changeme'
target = 'https://rickrolled.com/'
zap = ZAPv2(apikey=apiKey, proxies={'http': 'http://localhost:8080'})

print('Spidering target {}'.format(target))
# The scan returns a scan id to support concurrent scanning
scanID = zap.spider.scan(target)
while int(zap.spider.status(scanID)) < 100:
    # Poll the status until it completes
    print('Spider progress %: {}'.format(zap.spider.status(scanID)))
    time.sleep(1)

print('Spider has completed!')
# Prints the URLs the spider has crawled
print('\n'.join(map(str, zap.spider.results(scanID))))

scanID = zap.ascan.scan(target)
print(scanID)
alert_dict = dict()
while int(zap.ascan.status(scanID)) < 100:
    alerts = zap.core.alerts(baseurl=target)
    for alert in alert:
        if alert.get('alert') in alert_dict:
            continue
        else:
            alert_details = {'title':alert.get('alert'),'description':alert.get('description'),'fixes':alert.get('solution'),'severity':alert.get('risk')}
            requests.post("http://localhost:8000/projects/"+project_id+"/vulnerabilities",json=alert_details)
    print('Scan progress %: {}'.format(zap.ascan.status(scanID)))
    time.sleep(5)

print('Active Scan completed')
# Print vulnerabilities found by the scanning
print('Hosts: {}'.format(', '.join(zap.core.hosts)))
print('Alerts: ')
pprint()
