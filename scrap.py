# Made with love by Karlpy
import grequests, json
import unicodecsv as csv

set_url = 'https://servicios.set.gov.py/eset-publico/ciudadano/recuperar?cedula='

# Cedula (id) range
id_range = 10
urls = [set_url + str(ced) for ced in range(id_range)]

with open ('datos.csv','wb') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['cedula', 'nombres', 'apellidoPaterno', 'apellidoMaterno', 'nombreCompleto'])

    # grequests automatically creates a session to avoid TCP overhead. Let's create the requests generator
    requests_unsent = (grequests.get(u) for u in urls)
    # imap concurrently converts a generator object of Requests to a generator of Responses.
    requests_iterable = grequests.imap(requests_unsent, size=10)
    # iterate over the responses generator
    for response in requests_iterable:
        response_json = json.loads(response.text)
        if(response_json["presente"] == False):
            print("No existe el nro de cedula")
        else:
            print(response_json["resultado"])
            writer.writerow(response_json["resultado"].values())
