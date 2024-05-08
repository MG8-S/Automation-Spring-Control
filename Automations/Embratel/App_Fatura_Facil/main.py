import os
import re
import locale

from shutil import rmtree
from datetime import datetime as dt
from os.path import join
from time import sleep

from pywinauto.application import Application

import _main_path
from Automations.Embratel.App_Fatura_Facil.Conn_TRP import get_login
from Objects.Obj_Automation_GUI import AutoGui


def press_ok_btn(app, wait: int = 2, tries: int = 5):
    sleep(wait)
    for i in range(tries):
        window = [x for x in app.windows()
                  if 'OK' in x.children_texts()]

        if len(window) > 0:
            window = window[0]
            try:
                app.window(title=window.texts()[0]).child_window(
                    title="OK", control_type="Button").click()
                return
            except Exception:
                if i > tries - 1:
                    raise
                else:
                    print("Falha ao pressionar botão OK, tentando novamente...")

        else:
            print("Botão não encontrado, procurando novamente...")
            sleep(2)


def get_folder_service(service, mesref: dt):
    mesref = mesref.strftime('%Y-%m')

    path = join(os.environ['OneDrive'],
                'Clientes\\COMERCIAL\\ICATU\\GESTÃO\\02 - AUTOMACOES\\FAT_EBT',
                mesref)

    if not os.path.exists(path):
        os.mkdir(path)

    path = join(path, service)

    if not os.path.exists(path):
        os.mkdir(path)

    return path


def move_file(file, old_path, new_path, faturas, quit_funct: Application.kill):
    fat = re.findall('[0-9]+', file)[0]
    new_filename = [x for x in faturas if fat in x][0]

    old_path_file = join(old_path, file)
    new_path_file = join(new_path, "FAT_"+new_filename+'.TXT')

    if os.path.getsize(old_path_file) < 10:  # Arquivo Vazio
        print("Arquivo vazio ou corrompido, deletando arquivo do sistema")
        sleep(2)

        try:
            os.remove(old_path_file)
        except PermissionError:
            quit_funct()
            sleep(1)
            os.remove(old_path_file)

    else:
        os.replace(old_path_file, new_path_file)


def Download_Fat_Ebt(mesref: dt = dt.now()):
    _main_path.__loader__
    locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')

    cur_dir = os.path.dirname(__file__)
    source_pyag = join(cur_dir, 'src')
    images_auto_path = join('C:\\', "Automations",
                            "SpringControl", "ImagesGUI")

    app_folder = join(cur_dir, 'app')

    os.chdir(app_folder)

    # Caminho do executável do Aplicativo
    ebt_exe = join(app_folder, 'Fatura_Facil_Web.exe')

    mes_download = mesref.strftime('%B/%Y')

    try:
        login, senha, cnpj, cliente = get_login(47)
    except Exception:
        print('ERRO: Não foi possível obter dados do banco de dados, '
              'será utilizado os dados escritos dentro do script')

        login = "EOL3178674"
        senha = "Embratel24"
        cnpj = "42283770000139"
        cliente = "Embratel"

    print(f'{cliente} | Usuário: {login} | Senha: {senha} | Cnpj: {cnpj}')
    print(f'Baixando mês: {mes_download}')

    baixados = []
    baixados_log = []

    # Inicia o aplicativo Fatura Facil
    app = Application(backend="uia").start(ebt_exe)

    quit_funct = app.kill
    # Aguarda um momento para o aplicativo ser iniciado completamente
    app.wait_cpu_usage_lower(threshold=10, timeout=30)

    # Identifica a janela principal do aplicativo
    janela_principal = app.top_window()

    # Clicar botão importar
    autogui = AutoGui(source_pyag, local_path=images_auto_path)
    autogui.go_to_btn_click('init_import.png', sleep_t=2, confidence=0.5)

    # Painel de login
    janela = app.window(title='Importação dos  Dados da Fatura')

    janela.descendants()[1].type_keys(login)
    janela.descendants()[2].type_keys(senha)
    janela.descendants()[0].type_keys(cnpj)

    autogui.go_to_btn_click('ok_btn.png')
    press_ok_btn(app)

    # Painel inferior - Lista cb (Combo Box)
    cb_list = [x for x in janela.descendants(
    ) if "uia_controls.ComboBoxWrapper" in str(x)]

    sleep(2)
    # Painel selecionar CNPJ
    cb_cnpj = cb_list[0]

    # Se apenas 1 CNPJ - não exite combo box
    cb_cnpj.select(cnpj[:8])
    press_ok_btn(app)

    # Painel inferior - MÊS
    cb_list[1].select(mes_download)

    press_ok_btn(app)

    # Painel inferior - SERVIÇO
    combo_serv = [x for x in janela.descendants(
    ) if "uia_controls.ComboBoxWrapper" in str(x)][-1]
    combo_serv.expand()
    items = [str(x) for x in janela.descendants() if "ListItem" in str(x)]
    items = list(set(items))
    items = [x.split("'")[1] for x in items]

    rm_itens = ['<Selecione o serviço>']
    for it in rm_itens:
        if it in items:
            items.remove(it)

    # print(items)

    print([x.split('  ')[0] for x in items])
    print('Quant. serviços: ', len(items))

    # Iteração serviço
    for item in items:
        print(item)
        combo_serv.select(item)  # selecionar serviço atual
        press_ok_btn(app)

        # Baixar FAT fatura
        faturas = [x for x in janela.descendants(
        ) if "uia_controls.ComboBoxWrapper" in str(x)]

        if faturas[0] == cb_cnpj:
            faturas = faturas[1]
        else:
            faturas = faturas[0]
        faturas.expand()
        items = [str(x) for x in janela.descendants() if "ListItem" in str(x)]
        items_fat = list(set(items))
        items_txt = ' '.join(items_fat)
        num_faturas = re.findall('[0-9]*  [0-9]*-[0-9]*', items_txt)

        print('Quant. faturas: ', faturas.item_count()-1)

        for fat in num_faturas:
            print('Baixando a fatura', fat)
            sleep(1)
            try:
                faturas.select(fat)  # baixar fatura atual
            except Exception:
                pass

            baixados.append(fat)
            press_ok_btn(app, tries=50, wait=5)

        baixados = list(set(baixados))
        faturas = [x.split('  ')[0] for x in baixados]
        arquivos = ['FAT_' + x[:-1] + '.TXT' for x in faturas]

        new_dwl_path = get_folder_service(item, mesref)
        files = [f for f in arquivos]
        for f in files:
            move_file(f, app_folder, new_dwl_path, baixados, quit_funct)
            baixados_log += baixados
        baixados = []

    print('Download Concluído!')

    janela.close()
    janela_principal.close()


if __name__ == "__main__":
    Download_Fat_Ebt()
