import os

import _main_path

try:
    from datetime import datetime as dt
    from datetime import timedelta as td
    from os.path import join
    from time import sleep
    from zipfile import ZipFile
    from selenium.common.exceptions import NoSuchElementException

    from Automations.Separador_faturas import invoices_split
    from Objects.Obj_WebAutomation import (Driver, WebElement,
                                           css_selector, xpath)
except ModuleNotFoundError as mnfe:
    os.system(f"pip install {mnfe.name}")
    os.system(f"python \"{__file__}\"")
    quit()

_main_path.__loader__


def __wait_loading__(webdriver: WebElement, wait: float = 1.5):
    sleep(wait)
    while webdriver.find_element(
            xpath,
            '//*[@id="ContentPlaceHolder1_UpdateProgress2"]'
    ).value_of_css_property('display') != "none":
        sleep(1)
    sleep(1.5)


def Download_Invoices(mesref: dt = None):
    if not mesref:
        mesref = dt.now()

    mesref = mesref.strftime('%Y/%m')

    # Define a pasta de download dos arquivos da Spring
    dwl_path = join(os.environ["OneDrive"],
                    r'Clientes\COMERCIAL\ICATU\GESTÃO\02 - AUTOMACOES',
                    'TEMP')

    # Limpa a pasta de downloads antes de iniciar o processo
    for f in os.listdir(dwl_path):
        os.remove(join(dwl_path, f))

    invoices_path = join(os.environ["OneDrive"],
                         r'Clientes\COMERCIAL\ICATU\GESTÃO\02 - AUTOMACOES',
                         'PARA TRATAR',
                         mesref.replace('/', '-'))

    if not os.path.exists(invoices_path):
        os.makedirs(invoices_path)
        print(f"Criado a pasta '{invoices_path}'")

    site_spring_ctrl = 'https://springcontrol.com.br/app/spring/loginGestor'

    # Define os drivers do script
    driver = Driver(download_folder=dwl_path)
    webdriver = driver.new_driver(safe_sites=[site_spring_ctrl])

    # Navega até a página da Spring
    webdriver.get(site_spring_ctrl)

    # Faz o login
    driver.find_by_element(webdriver,
                           '//*[@id="txtLogin"]',
                           wait=3).send_keys('NPIMENTEL@MG8.COM.BR')

    driver.find_by_element(webdriver,
                           '//*[@id="txtSenha"]',
                           wait=3).send_keys('8f6a82')

    driver.click_by_element(webdriver,
                            '//*[@id="btnLogar"]')

    # Acessa a página das faturas
    webdriver.get('https://springcontrol.com.br/app/spring/controleFaturas')

    # Abre a pagina de filtros por mês
    driver.click_by_element(webdriver,
                            '//*[@id="containerClassificacao"]' +
                            '/div/div/div/div[1]/div/div[1]/div')

    sleep(1)
    driver.click_by_element(webdriver,
                            '//*[@id="ContentPlaceHolder1_btnClearAnoMes"]',
                            wait=3)

    sleep(2)
    try:
        driver.click_by_element(webdriver, f'//td/label[contains(text(), "{mesref}")]')
    except NoSuchElementException:
        print("\033[1;31mMês não registrado ou encontrado no SC\033[0m")
        return

    sleep(1)
    driver.click_by_element(webdriver, '//*[@id="ContentPlaceHolder1_btnFiltrar"]')

    __wait_loading__(webdriver)
    sleep(1)

    try:
        # Coleta a tabela com as faturas
        pages = driver.find_by_element(
            webdriver,
            '//*[@id="ContentPlaceHolder1_grvImportacaoFatura"]' +
            '//tr[@class="gridPager"]/td/table/tbody/tr', wait=3)

        # Contabiliza quantas páginas tem disponíveis para abaixar faturas
        pages = pages.find_elements(css_selector, 'td')
        num_pages = len(pages)
    except Exception:
        num_pages = 1

    driver.click_by_element(
        webdriver,
        '//div[@id="divTableDetails"]//button[@title="Export"]',
        wait=3,
        use_js=True)

    driver.click_by_element(
        webdriver,
        '//div[@id="divTableDetails"]//a[contains(text(), "Excel")]',
        wait=3,
        use_js=True
    )

    while len(os.listdir(dwl_path)) == 0:
        sleep(2)

    while not (invoices_excel := os.listdir(dwl_path)[0]).endswith('.xlsx'):
        sleep(2)

    sleep(2)
    now = dt.now().strftime("%d-%m-%y")
    try:
        os.rename(join(dwl_path, invoices_excel),
                  join(invoices_path, f"{now} " + invoices_excel))
    except Exception:
        # Apaga o arquivo caso ele exista
        os.remove(join(invoices_path, f"{now} " + invoices_excel))

        # Tenta mover o arquivo novamente para a pasta
        os.rename(join(dwl_path, invoices_excel),
                  join(invoices_path, f"{now} " + invoices_excel))

    for page in range(num_pages):

        if num_pages != 1 and page != 0:
            # Navega para as próximas páginas
            pages: list[WebElement] = driver.find_by_element(
                webdriver,
                '//*[@id="ContentPlaceHolder1_grvImportacaoFatura"]/tbody' +
                '/tr[53]/td/table/tbody/tr//td',
                multiple=True)

            for num_pg in pages:
                if num_pg.text == str(page + 1):
                    break
            num_pg = num_pg.find_element(xpath, 'a')
            webdriver.execute_script("arguments[0].click()", num_pg)
            sleep(2)

        # Coleta informações sobre as faturas
        driver.click_by_element(
            webdriver,
            '//*[@id="ckbHeaderArquivo"]',
            wait=5,
            use_js=True)

        sleep(1.5)

        # Download da fatura
        driver.click_by_element(
            webdriver,
            '//*[@id="ContentPlaceHolder1_grvImportacao' +
            'Fatura_btnExportarSelect"]',
            wait=3,
            use_js=True)

        sleep(8)

    # Seleciona os arquivos na pasta de download e extrai os mesmos,
    # apagando em seguida os arquivos ZIP
    i = 0
    limit = 60
    while len(os.listdir(dwl_path)) != num_pages:
        sleep(1)
        i += 1
        if i >= limit:
            raise TimeoutError("Limite de tempo excedito à"
                               " espera de um download")

    while True:
        stop = True
        for f in os.listdir(dwl_path):
            if f.endswith('.crdownload'):
                stop = False
        else:
            if stop:
                break

    for file in os.listdir(dwl_path):
        path_file = os.path.join(dwl_path, file)
        with ZipFile(path_file, mode="r") as archive:
            archive.extractall(dwl_path)
        os.remove(path_file)

    # Fecha o navegador
    webdriver.quit()

    # Script que lê e separa as faturas por pastas
    invoices_split(mesref)


if __name__ == "__main__":
    meses = []
    meses.append(dt.now())
    if dt.now().day > 20:
        meses.append(dt.now() + td(weeks=2))

    for mes in meses:
        Download_Invoices(mes)
