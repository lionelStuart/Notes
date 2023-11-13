from time import sleep
import requests
while True:
    requests.get('http://127.0.0.1:8080/resource')
    sleep(0.1)