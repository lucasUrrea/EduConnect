import requests, re, os
base = 'http://127.0.0.1:8000'
s = requests.Session()
# Ensure test user exists in DB (we created earlier)
email = 'webtest@example.com'
password = 'testpass'
# Fetch login page
r = s.get(base + '/login/')
if r.status_code != 200:
    print('Login page GET failed', r.status_code)
    raise SystemExit(1)
m = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([0-9a-zA-Z]+)['\"]", r.text)
# get csrf token from form (preferred) or cookie
csrf = s.cookies.get('csrftoken')
m = re.search(r"name=['\"]csrfmiddlewaretoken['\"] value=['\"]([0-9a-zA-Z]+)['\"]", r.text)
if m:
    form_token = m.group(1)
else:
    form_token = None
token_for_post = form_token or csrf
print('csrf cookie=', csrf, 'form token=', form_token)
# Post login (use form token if available)
login_data = {'email': email, 'password': password, 'csrfmiddlewaretoken': token_for_post}
resp = s.post(base + '/login/', data=login_data, headers={'Referer': base + '/login/'})
print('login status', resp.status_code, 'url', resp.url)
# GET crear form
r2 = s.get(base + '/consulta/crear/')
print('GET crear status', r2.status_code)
# get csrf for form
csrf2 = s.cookies.get('csrftoken')
# find asignatura id from page (select options)
m = re.search(r'<select[^>]*name="id_asignatura"[^>]*>(.*?)</select>', r2.text, re.S)
asignatura_id = None
if m:
    options = re.findall(r'<option value="(\d+)"', m.group(1))
    if options:
        asignatura_id = options[0]
print('asignatura_id', asignatura_id)
# post create
post = {'id_asignatura': asignatura_id or '1', 'id_categoria': '', 'titulo': 'Req via requests', 'descripcion':'scripted desc', 'prioridad':'', 'csrfmiddlewaretoken': csrf2}
resp3 = s.post(base + '/consulta/crear/', data=post, headers={'Referer': base + '/consulta/crear/'}, allow_redirects=False)
print('POST crear status', resp3.status_code, 'location', resp3.headers.get('Location'))
# verify in DB via API using Django shell would be easier, but we can ask server to show last consultas page
resp4 = s.get(base + '/mis-consultas/')
print('/mis-consultas status', resp4.status_code)
print('snippet:', resp4.text[:800])
