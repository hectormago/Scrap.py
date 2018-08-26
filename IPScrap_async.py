# Made with love by Karlpy
import requests, csv, json, asyncio, aiohttp, time
from lxml import etree, html
from concurrent.futures import FIRST_COMPLETED
ips_url = 'http://servicios.ips.gov.py/consulta_asegurado/comprobacion_de_derecho_externo.php'

# Cedula (id) range
start = 1
stop = 11

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
    start = time.time()
    result_html = await aiohttp_post_to_page(param)
    ced = param['nro_cic']
    t = (time.time() - start)
    return t, ced, result_html

async def main():
    futures = [fetch_data(param) for param in param_dict_list]
    # done, pending = await asyncio.wait(futures, timeout=5)

    with open ('500k.csv','w',newline='',encoding='utf-8') as csvfile:
        hp = etree.HTMLParser(encoding='utf-8')
        writer=csv.writer(csvfile)
        writer.writerow(['nro_documento', 'nombres', 'apellidos', 'fecha_nacim', 'sexo', 'tipo_aseg', 'beneficiarios_activos', 'enrolado','vencimiento_de_fe_de_vida','nro_titular', 'titular', 'estado_titular', 'meses_de_aporte_titular','vencimiento_titular','ultimo_periodo_abonado_titular'])
        start = time.time()
        for i, future in enumerate(asyncio.as_completed(futures)):
            #print(future.result())
            try:
                result = await future
                t, ced, result_html = result
                root = html.fromstring(result_html, parser=hp)
                nro_documento = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[2]")[0].text.strip()
                nombres = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[3]")[0].text.strip()
                apellidos = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[4]")[0].text.strip()
                fecha_nacim = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[5]")[0].text.strip()
                sexo = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[6]")[0].text.strip()
                tipo_aseg = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[7]")[0].text.strip()
                beneficiarios_activos = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[8]")[0].text.strip()
                enrolado = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[9]")[0].text.strip()
                vencimiento_de_fe_de_vida = root.xpath(u"/html/body/center[2]/form/table[2]/tr[2]/td[10]")[0].text.strip()

                nro_titular = root.xpath(u"/html/body/center[2]/form/table[3]/tr[2]/td[1]")[0].text.strip()
                titular = root.xpath(u"/html/body/center[2]/form/table[3]/tr[2]/td[2]")[0].text.strip()
                estado_titular = root.xpath(u"/html/body/center[2]/form/table[3]/tr[2]/td[3]")[0].text.strip()
                meses_de_aporte_titular = root.xpath(u"/html/body/center[2]/form/table[3]/tr[2]/td[4]")[0].text.strip()
                vencimiento_titular = root.xpath(u"/html/body/center[2]/form/table[3]/tr[2]/td[5]")[0].text.strip()
                ultimo_periodo_abonado_titular = root.xpath(u"/html/body/center[2]/form/table[3]/tr[2]/td[6]")[0].text.strip()

                print('{}, {}, {} retornado en {:.2f} segundos'.format(nro_documento, nombres, apellidos, t))
                writer.writerow([nro_documento, nombres, apellidos, fecha_nacim, sexo, tipo_aseg, beneficiarios_activos, enrolado, vencimiento_de_fe_de_vida, nro_titular, titular, estado_titular, meses_de_aporte_titular, vencimiento_titular, ultimo_periodo_abonado_titular])

            except Exception as e:
                print("Cedula: %s no existe" %(ced))
                continue
        print("Process took: {:.2f} seconds".format(time.time() - start))

asyncio.run(main())