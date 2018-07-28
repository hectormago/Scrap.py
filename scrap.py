# Made with love by Karlpy
import grequests
import csv
import json

set_url = 'https://servicios.set.gov.py/eset-publico/ciudadano/recuperar?cedula='

# Cedula (id) range
id_range = 8000000

with open ('datos.csv','w',newline='') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['cedula', 'nombres', 'apellidoPaterno', 'apellidoMaterno', 'nombreCompleto'])
    urls = [set_url + str(ced) for ced in range(id_range)]
    requests_unsent = (grequests.get(u) for u in urls)
    requests_iterable = grequests.imap(requests_unsent, size=5)

    # do it asynchronously
    for response in requests_iterable:
        response_json = response.json()
        if(response_json["presente"] == False):
            print("No existe el nro de cedula")
        else:
            print(response_json["resultado"])
            writer.writerow(response_json["resultado"].values())