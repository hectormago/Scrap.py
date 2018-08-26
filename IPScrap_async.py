# Made with love by Karlpy
import requests, csv, json, asyncio, aiohttp
from lxml import etree, html
from concurrent.futures import FIRST_COMPLETED

ips_url = 'http://servicios.ips.gov.py/consulta_asegurado/comprobacion_de_derecho_externo.php'

# Cedula (id) range
start = 1
stop = 100

param_dict_list = []

for c in range(start, stop):
    param_dict_list.append({'nro_cic':str(c), 'elegir':'', 'envio':'ok','recuperar':'Recuperar'})

async def aiohttp_post_to_page(data):
    connector = aiohttp.TCPConnector(limit_per_host=15)
    client_session = aiohttp.ClientSession(connector=connector)
    async with client_session:
        async with client_session.post(ips_url,data=data) as response:
            return await response.text()

async def fetch_data(param):
    result_html = await aiohttp_post_to_page(param)
    ced = param['nro_cic']
    return ced, result_html

async def main():
    futures = [fetch_data(param) for param in param_dict_list]
    # done, pending = await asyncio.wait(futures, timeout=5)

    with open ('datos_ips_async.csv','w',newline='') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(['nro_documento', 'nombres', 'apellidos', 'fecha_nacim', 'sexo', 'tipo_aseg', 'beneficiarios_activos', 'enrolado','vencimiento_de_fe_de_vida'])

        for i, future in enumerate(asyncio.as_completed(futures)):
            #print(future.result())
            try:
                result = await future
                ced, result_html = result
                root = html.fromstring(result_html)
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
                print("Cedula: %s no existe" %(ced))
                continue

asyncio.run(main())