#Author:Jeff Lee

import requests


url = "https://167.4.3.3/tcn2000/security/tologinpage.do"
data = {'userName':'admin',"userPassword1":"xinwei"}


response = requests.post(url,data)

print(response.text)
