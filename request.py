import requests

url = "http://127.0.0.1:8000/api/user/logout/"
refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTQ2ODgwMywiaWF0IjoxNjgxMzgyNDAzLCJqdGkiOiIyYTZiNDhkNjBlNTM0NTM1ODJhMWUzYmM1Y2I0OWU5YSIsInVzZXJfaWQiOjN9.WZZ7idaGfBsVs9dW_HrQ1O8Mm8jb-wdaMxYlXvSe9rs"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjgxMzgyNzAzLCJpYXQiOjE2ODEzODI0MDMsImp0aSI6ImFlMjJmZjgyYWM0NzRlOTA5ZTk2MjQ2ZmVmZjE5NzQzIiwidXNlcl9pZCI6M30.O8_ANlY0iWYrP4MQ6eUjvw9PUTx_cP8dRJzEN6_CN9g"
data = {'refresh_token': refresh_token}
headers = {'Authorization': f'Bearer {token}'}
request = requests.post(url, headers=headers, data=data)

print(request)