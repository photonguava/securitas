#!/bin/sh
nohup owasp-zap -daemon --host 0.0.0.0 --port 8080 -config api.addrs.addr.name=.* -config api.addrs.addr.regex=true -config api.key=changeme >> nohup.out 2>&1 &
python3 app.py $target $project_id