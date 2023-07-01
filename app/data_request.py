import requests 

url = "https://datos.madrid.es/egob/catalogo/202087-0-trafico-intensidad.xml"
r = requests.get(url)
print(r.text)
