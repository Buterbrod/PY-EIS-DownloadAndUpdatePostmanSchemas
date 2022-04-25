import os
import datetime
import requests
import pathlib

server_login = 'qa'
server_password = 'qa'
server = 'nightly.genci0.eisgroup.com'
# server = 'automation.genci0.eisgroup.com'

schemas = ['policy-pnc-motor',  # policy-pnc-motor-policy-pnc-motor-app-vs
           'policy-auto',  # policy-pnc-policy-auto-app-vs
           'policy-fleet',  # policy-pnc-policy-fleet-app-vs
           'policy-property',  # policy-pnc-policy-property-app-vs
           'policy-generic',  # policy-policy-generic-app-vs
           'purchase']  # purchase-purchase-app-vs

# Загрузить схемы postman (postman.json) по указанному ниже пути
#    и подправить в них значение {{url}} на корректное значение для загрузки в postman
# pwd = os.getcwd()  # текущая директория - pwd
pwd = os.path.dirname(os.path.abspath(__file__))  # директория скрипта

# создать директорию для выгружаемых postmen.json файлов
pwd = os.path.join(pwd, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
pathlib.Path(pwd).mkdir(parents=True, exist_ok=True)

for schema in schemas:
    postman_file = os.path.join(pwd, f'{schema}.txt')
    postman_server = f'https://{schema}-app-{server}'
    postman_link = f'{postman_server}/api/common/schema/v1/postman.json'

    # сохранить postman.json на диске с именем схемы
    response = requests.get(postman_link, auth=requests.auth.HTTPBasicAuth(server_login, server_password))
    open(postman_file, 'wb').write(response.content)

    # поменять в файлах {{url}} на нужный линк и сохранить во временном файле
    postman_file_tmp = postman_file + '_'
    with open(postman_file, 'r') as f_src, open(postman_file_tmp, 'w') as f_dst:
        for line in f_src:
            line = line.replace('{{url}}', f'https://{schema}-app-' + '{{namespace.zone}}')
            f_dst.write(line)

    # переименовать временный файл в постоянный
    os.remove(postman_file)
    os.rename(postman_file_tmp, postman_file)
