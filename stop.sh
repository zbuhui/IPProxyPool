ps -ef|grep IPProxy.py | grep -v 'grep' | awk '{print $2}' | xargs kill -9
