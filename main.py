from typing import List, Any
import openpyxl
import pandas as pd
import os
import datetime
from utils import FileChecker

def extract_sheet_data(sheet_path: str, table_name: str, init_row: int, col: int, del_file: bool) -> list:
    # Carregar o arquivo .xlsx
    workbook = openpyxl.load_workbook(sheet_path)
    sheet_table = workbook[table_name]
    values = []
    for linha in sheet_table.iter_rows(min_row=init_row):
        cell_value = linha[col].value
        if cell_value is not None and cell_value != 'N/A':
            if cell_value == 0:
                continue
            elif isinstance(cell_value, datetime.datetime):
                values.append(cell_value.strftime("%d%m%Y"))
            else:
                values.append(cell_value)
    
    if del_file:
        remove_file(sheet_path)
    
    return values

def filter_data_by_date_and_value(file_path: str, table_name: str, init_line: int, date_col: int, value_col: int) -> List[List[Any]]:
    dates: list = extract_sheet_data(file_path, table_name, init_line, date_col, False)
    values: list = extract_sheet_data(file_path, table_name, init_line, value_col, True)
    merged_lists = merge_lists(dates, values)
    values_summed = sum_values(merged_lists)
    monthly_sums = sum_values_by_month(values_summed)
    return monthly_sums

def remove_file(file_path):
    os.remove(file_path)

def merge_lists(*args: List[Any]) -> List[List[Any]]:
    if not args:
        return []
    
    max_length = max(len(lst) for lst in args)
    merged = []
    
    for i in range(max_length):
        row = [lst[i] if i < len(lst) else None for lst in args]
        if None not in row:
            merged.append(row)
    
    return merged

def sum_values(date: List[List[Any]]) -> List[List[Any]]:
    total_by_date = {}
    
    for item in date:
        date, value = item
        if value is None:
            continue
        if date in total_by_date:
            total_by_date[date] += value
        else:
            total_by_date[date] = value
    
    return [[date, round(value, 2)] for date, value in total_by_date.items()]

# TODO: tratar caso a data venha no formato 'yyyy-mm-dd'
def sum_values_by_month(data_value_list: List[List[Any]]) -> List[List[Any]]:
    monthly_sums = {}
    
    for item in data_value_list:
        data, value = item
        month = data[2:4]  # Extrair o mês da data (dois primeiros dígitos)
        if value is not None:
            if month in monthly_sums:
                monthly_sums[month] += value
            else:
                monthly_sums[month] = value
    
    # Arredondar os valores para 2 casas decimais
    return [[month, round(value, 2)] for month, value in monthly_sums.items()]

def aggregate_monthly_values(dados):
    # Inicializa um dicionário para armazenar as somas dos valores por mês
    monthly_sums = {}

    # Itera sobre a lista de listas
    for sublist in dados:
        # Itera sobre os pares de mês e valor na sublista
        for month_value_pair in sublist:
            if month_value_pair is not None:
                month, value = month_value_pair
                if month in monthly_sums:
                    monthly_sums[month] += value
                else:
                    monthly_sums[month] = value

    return monthly_sums

def entrada(nfe_path: str, nfse_path: str):
    total_values_nfe_entrada = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfe_path), 'Notas', 5, 1, 9)
    total_values_nfse_tomado = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfse_path), 'Notas', 5, 0, 7)

    total_values_nfse_nfe_entrada = merge_lists(total_values_nfe_entrada, total_values_nfse_tomado)
    total_values_nfse_nfe_entrada = aggregate_monthly_values(total_values_nfse_nfe_entrada)
    return total_values_nfse_nfe_entrada

def saida(nfe_path: str, nfse_path: str, sat_path):
    total_values_nfe_saida = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfe_path), 'Notas', 5, 1, 9)
    total_values_nfse_emitido = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfse_path), 'Notas', 5, 0, 7)
    total_values_sat = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(sat_path), 'CF-e SAT', 5, 0, 5)

    total_values_nfse_nfe_saida = merge_lists(total_values_nfe_saida, total_values_nfse_emitido, total_values_sat)
    total_values_nfse_nfe_saida = aggregate_monthly_values(total_values_nfse_nfe_saida)
    return total_values_nfse_nfe_saida

# Exemplo de uso
# nfe_entrada = entrada('/home/felipecn/Downloads/TEMP/NFE-ENTRADA.XLS', '/home/felipecn/Downloads/TEMP/NFSE-TOMADO.XLS')
# nfe_saida = saida('/home/felipecn/Downloads/TEMP/NFE-SAIDA.XLS', '/home/felipecn/Downloads/TEMP/NFSE-PRESTADO.XLS', '/home/felipecn/Downloads/TEMP/SAT.XLS')
# print(nfe_saida)

