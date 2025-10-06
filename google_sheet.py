import gspread, locale
from datetime import datetime
from dateutil.relativedelta import relativedelta

months = {
    'января': 'Январь',
    'февраля': 'Февраль',
    'марта': 'Март',
    'апреля': 'Апрель',
    'мая': 'Май',
    'июня': 'Июнь',
    'июля': 'Июль',
    'августа': 'Август',
    'сентября': 'Сентябрь',
    'октября': 'Октябрь',
    'ноября': 'Ноябрь',
    'декабря': 'Декабрь'
}

def get_tasks_from_the_table(title: str):
    connection = gspread.service_account('credentials.json')
    sheet = connection.open(title)
    worksheets = sheet.worksheets()

    for worksheet in worksheets:
        if worksheet.title == str(datetime.now().year):
            return get_current_data_rows(worksheet)
    else:
        return worksheets


def get_current_data_rows(worksheet):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    today = datetime.now()
    print(today)
    str_today = datetime.strftime(today, '%d.%m')
    print(str_today)
    previous_month = today - relativedelta(months=1)
    print(previous_month)
    cell_previous_month = worksheet.find(months[previous_month.strftime('%B')], in_column=1)
    print(cell_previous_month)
    if cell_previous_month:
        data_rows = worksheet.get_values(f'A3:K{int(cell_previous_month.row) - 1}')
        

        current_data_rows = [el for el in data_rows
                         if not el[2] and el[7] != '' and el[7] != 'Дина' and el[5] != '' and el[8]
                         and datetime.strptime(el[8], '%d.%m') > datetime.strptime(str_today, '%d.%m')]
        for sublist in current_data_rows:
    
            name = sublist[7]
   
            cleaned_name = name.split("(")[0].strip()
                    
            sublist[7] = cleaned_name
        
        return current_data_rows

    else:
        for i in range(11):
            previous_month = today - relativedelta(months=i)
            cell_previous_month = worksheet.find(previous_month.strftime('%B'), in_column=1)
            if cell_previous_month:
                data_rows = worksheet.get_values(f'A3:K{int(cell_previous_month.row) - 1}')

                current_data_rows = [el for el in data_rows
                                     if not el[2] and el[7] != '' and el[7] != 'Дина' and el[5] != '' and el[8]
                                     and datetime.strptime(el[8], '%d.%m') > datetime.strptime(str_today, '%d.%m')]
                for sublist in current_data_rows:
    
                    name = sublist[7]
   
                    cleaned_name = name.split("(")[0].strip()
                    
                    sublist[7] = cleaned_name
                    
                return current_data_rows
        return None
#print(get_tasks_from_the_table('Промо'))