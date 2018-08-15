# Made with love by Karlpy
import requests, csv, json
from lxml import etree, html

ips_url = 'http://servicios.ips.gov.py/consulta_asegurado/comprobacion_de_derecho_externo.php'

# Cedula (id) range
start = 1
stop = 10

param_dict_list = []

for c in range(start, stop):
    param_dict_list.append({'nro_cic':str(c), 'elegir':'', 'envio':'ok','recuperar':'Recuperar'})

with open ('datos_ips.csv','w',newline='') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['nro_documento', 'nombres', 'apellidos', 'fecha_nacim', 'sexo', 'tipo_aseg', 'beneficiarios_activos', 'enrolado','vencimiento_de_fe_de_vida'])

    session = requests.Session()
    for ced in param_dict_list:
        try:
            r = session.post(ips_url, data = ced)
            root = html.fromstring(r.text)
            nro_documento = root.xpath("/html/body/center[2]/form/table[2]/tr[2]/td[2]")[0].text.strip()
            nombres = root.xpath("/html/body/center[2]/form/table[2]/tr[2]/td[3]")[0].text.strip()
            apellidos = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[4]')[0].text.strip()
            fecha_nacim = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[5]')[0].text.strip()
            sexo = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[6]')[0].text.strip()
            tipo_aseg = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[7]')[0].text.strip()
            beneficiarios_activos = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[8]')[0].text.strip()
            enrolado = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[9]')[0].text.strip()
            vencimiento_de_fe_de_vida = root.xpath('/html/body/center[2]/form/table[2]/tr[2]/td[10]')[0].text.strip()

            print(nro_documento, nombres, apellidos)
            writer.writerow([nro_documento, nombres, apellidos, fecha_nacim, sexo, tipo_aseg, beneficiarios_activos, enrolado, vencimiento_de_fe_de_vida])

        except Exception as e:
            print("Cedula %s no existe" %nro_documento)
            continue