import requests 


# Request the data to the url and save in in an xml file
def request_data():
    url = "https://datos.madrid.es/egob/catalogo/202087-0-trafico-intensidad.xml"
    r = requests.get(url)

    with open("data/traffic_data.xml", 'wb') as file:
        file.write(r._content) 
    r.close()

