import pandas as pd
import os
from data_process import cities_process
from geopy.geocoders import Nominatim
import time



def extract_date(text):
    if pd.isna(text):
        return pd.NaT

    text = str(text).lower()
    if ',' in text:
        dt = pd.to_datetime(text.split(
            ',')[-1].strip(), dayfirst=True, errors='coerce')
    elif 'от' in text:
        dt = pd.to_datetime(text.split(
            'от')[-1].strip(), dayfirst=True, errors='coerce')
    else:
        return pd.NaT
    return dt.date() if pd.notna(dt) else pd.NaT


folder_path = 'data/'
excel_files = [f for f in os.listdir(
    folder_path) if f.endswith(('.xlsx', '.xls'))]

all_data = []

for file_name in excel_files:
    file_path = os.path.join(folder_path, file_name)
    sheet_names = pd.ExcelFile(file_path).sheet_names

    for sheet in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet, engine='openpyxl')

        df = df.iloc[:, :13]
        df.columns = ['Дата оплаты счета', 'Дата отгрузки', 'Номер счета и дата счета', 'Город',
                      'Название Компании - клиента', 'Фирма поставщик', 'Сумма клиента', 'Сумма поставщика',
                      'Транспортная компания', 'Cумма транспортных расходов', 'Орехи КЛ', 'Cумма Орехов', 'Итог маржа']

        # удаляем строку с итоговой суммой
        df = df[df.iloc[:, 0].astype(str).str.lower().str.strip() != 'итог']

        # удаляем лишние строки
        df['Сумма клиента'] = pd.to_numeric(
            df['Сумма клиента'], errors='coerce')
        df['Сумма поставщика'] = pd.to_numeric(
            df['Сумма поставщика'], errors='coerce')
        df['Cумма транспортных расходов'] = pd.to_numeric(
            df['Cумма транспортных расходов'], errors='coerce')
        df = df[df['Сумма клиента'].notna() & df['Сумма поставщика'].notna()]

        df['Менеджер'] = file_name.split()[0]  # добавляем менеджера
        df['Дата счета'] = df['Номер счета и дата счета'].apply(extract_date)
        df['Итог маржа'] = df['Сумма клиента'] - df['Сумма поставщика'] - \
            df['Cумма транспортных расходов'].fillna(0)

        all_data.append(df)

combined_df = pd.concat(all_data, ignore_index=True)
combined_df = combined_df.drop_duplicates()

# Устанавливаем границы допустимых дат
min_date = pd.Timestamp('2021-01-01')
max_date = pd.Timestamp.today().normalize()

# Преобразуем колонки в datetime
combined_df['Дата оплаты счета'] = pd.to_datetime(
    combined_df['Дата оплаты счета'], dayfirst=True, errors='coerce')

combined_df['Дата отгрузки'] = pd.to_datetime(
    combined_df['Дата отгрузки'], dayfirst=True, errors='coerce')

combined_df['Дата счета'] = pd.to_datetime(
    combined_df['Дата счета'], dayfirst=True, errors='coerce')

# Очищаем некорректные даты вне диапазона
combined_df.loc[
    (combined_df['Дата оплаты счета'] < min_date) |
    (combined_df['Дата оплаты счета'] > max_date),
    'Дата оплаты счета'
] = pd.NaT

combined_df.loc[
    (combined_df['Дата отгрузки'] < min_date) |
    (combined_df['Дата отгрузки'] > max_date),
    'Дата отгрузки'
] = pd.NaT

combined_df.loc[
    (combined_df['Дата счета'] < min_date) |
    (combined_df['Дата счета'] > max_date),
    'Дата счета'
] = pd.NaT

combined_df['Номер счета и дата счета'] = combined_df['Номер счета и дата счета'].astype(
    str)
combined_df['Орехи КЛ'] = combined_df['Орехи КЛ'].astype(str)

combined_df['Город'] = combined_df['Город'].apply(cities_process)

geolocator = Nominatim(user_agent="city_to_region")

def get_region(city):
    pass

unique_cities = combined_df['Город'].dropna().unique()
city_to_region = {}

for city in unique_cities:
    region = get_region(city)
    city_to_region[city] = region
    time.sleep(1)  # важно!

combined_df['Регион'] = combined_df['Город'].map(city_to_region)

combined_df.to_excel('combined_data.xlsx', index=False)
