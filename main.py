import os
from datetime import datetime as dt
from datetime import timedelta as td

# Import automation and reader modules
try:
    from Automations.Download_Invoices_Spring_Control import Download_Invoices
    from Automations.Embratel.App_Fatura_Facil.Fat_Converter import Read_fats  # noqa
    from Automations.Embratel.App_Fatura_Facil.main import Download_Fat_Ebt
    from Readers.Embratel.Leitor_Fat import Process_Fat_Ebt
except ModuleNotFoundError as mnfe:
    # Attempt to install missing modules using pip
    os.system(f'pip install {mnfe.name}')
    os.system(f'python "{__file__}"')
    quit()

# Main function execution starts here
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))

    # Initialize list of months to process
    meses = []

    # Add current month to the list
    # meses += list(dt(2024, x, 1) for x in range(1,6))
    meses.append(dt.now())

    # If the current day is the 20th or later,
    # add next month to the list as well
    if dt.now().day >= 20:
        meses.append(dt.now() + td(weeks=2))

    # Process each months
    for mes in meses:
        # Download invoices for the given month
        Download_Invoices(mes)

        # Process detailed billing report for Embratel
        try:
            app_path = os.path.join(
                os.path.dirname(__file__),
                'Automations/Embratel/App_Fatura_Facil/app'
            )
            for file in os.listdir(app_path):
                if file.endswith('.TXT'):
                    os.remove(os.path.join(app_path, file))

            Download_Fat_Ebt(mes)
            Read_fats(mes)
        except Exception as e:
            print(e)

    # Process_Fat_Ebt()
