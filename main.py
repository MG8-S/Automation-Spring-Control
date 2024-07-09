import os
from datetime import datetime as dt
from datetime import timedelta as td

# Import automation and reader modules
try:
    from Automations.Download_Invoices_Spring_Control import Download_Invoices
    from Embratel_Process import Ebt_Process
    from Oi_Process import Oi_Process

except ModuleNotFoundError as mnfe:
    print(f'\nMODULE: "{mnfe.name}"')
    match mnfe.name:
        case 'fitz':
            # Attempt to install missing modules using pip
            print('Installing missing module fitz / pymupdf...')
            os.system('pip install pymupdf')
        case other:
            # Attempt to install missing modules using pip
            print(f'Installing missing module {mnfe.name}...')
            os.system(f'pip install {mnfe.name}')

    os.system(f'python "{__file__}"')
    quit()


def main(mes: dt):
    print(f'Processando: {mes.strftime("%Y-%m")}')

    # Download invoices for the given month
    print('Fazendo download dos boletos no SC...')
    Download_Invoices(mes)

    # Faz download dos detalhamentos e processa os boletos da Embratel
    print('\n\nFazendo download dos detalhamentos da Embratel...')
    Ebt_Process(mes)

    # Faz download dos detalhamentos e processa os boletos da Oi
    print('\n\nFazendo download dos detalhamentos da Oi...')
    Oi_Process(mes)


# Main function execution starts here
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    # Initialize list of months to process
    meses: list[dt] = []

    # Add current month to the list
    # init = 1
    # end = 2
    # meses += list(dt(2024, x, 1) for x in range(init, end))
    meses.append(dt.now())

    # If the current day is the 20th or later,
    # add next month to the list as well
    if dt.now().day >= 20:
        meses.append(dt.now() + td(weeks=2))

    # Process each months
    for mes in meses:
        main(mes)
