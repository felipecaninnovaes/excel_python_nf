from typing import List, Dict, Tuple, Any
import openpyxl
import pandas as pd
import os
import datetime

def check_xlsx_as_valid(file_path: str) -> str:
    # Verificar a extensão do arquivo
    file_base_path = os.path.splitext(file_path)[0]
    file_extension = os.path.splitext(file_path)[1]
    
    
    if file_extension == '.XLS' or 'XLSX':
        new_path = f'{file_base_path}{file_extension.lower()}'
        rename_extension_file(file_path, new_path)
        file_path = new_path
    else:
        pass    
    # Se for .xls, converter para .xlsx
    if file_extension.lower() == '.xls':
        xlsx_path = file_path.replace('.xls', '.xlsx')
        convert_xls_to_xlsx(file_path, xlsx_path)
        file_path = xlsx_path
        return file_path
    else:
        return file_path

def rename_extension_file(old_path: str, new_path: str) -> None:
    try:
        os.rename(old_path, new_path)
        print(f"Arquivo renomeado de {old_path} para {new_path}")
    except FileNotFoundError:
        print(f"Arquivo {old_path} não encontrado.")
    except PermissionError:
        print(f"Permissão negada para renomear {old_path}.")
    except Exception as e:
        print(f"Ocorreu um erro ao renomear o arquivo: {e}")

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

def convert_xls_to_xlsx(xls_path: str, xlsx_path: str):
    # Ler o arquivo .xls
    df = pd.read_excel(xls_path, sheet_name=None)
    
    # Criar um objeto ExcelWriter com o caminho do arquivo .xlsx
    with pd.ExcelWriter(xlsx_path, engine='openpyxl') as writer:
        # Iterar sobre as planilhas e salvar cada uma no novo arquivo .xlsx
        for sheet_name, data in df.items():
            data.to_excel(writer, sheet_name=sheet_name, index=False)

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
    total_values_nfe_entrada = filter_data_by_date_and_value(check_xlsx_as_valid(nfe_path), 'Notas', 5, 1, 9)
    total_values_nfse_tomado = filter_data_by_date_and_value(check_xlsx_as_valid(nfse_path), 'Notas', 5, 0, 7)

    total_values_nfse_nfe_entrada = merge_lists(total_values_nfe_entrada, total_values_nfse_tomado)
    total_values_nfse_nfe_entrada = aggregate_monthly_values(total_values_nfse_nfe_entrada)
    return total_values_nfse_nfe_entrada

def saida(nfe_path: str, nfse_path: str, sat_path):
    total_values_nfe_saida = filter_data_by_date_and_value(check_xlsx_as_valid(nfe_path), 'Notas', 5, 1, 9)
    total_values_nfse_emitido = filter_data_by_date_and_value(check_xlsx_as_valid(nfse_path), 'Notas', 5, 0, 7)
    total_values_sat = filter_data_by_date_and_value(check_xlsx_as_valid(sat_path), 'CF-e SAT', 5, 0, 5)

    total_values_nfse_nfe_saida = merge_lists(total_values_nfe_saida, total_values_nfse_emitido, total_values_sat)
    total_values_nfse_nfe_saida = aggregate_monthly_values(total_values_nfse_nfe_saida)
    return total_values_nfse_nfe_saida

# Exemplo de uso
nfe_entrada = entrada('/home/felipecn/Downloads/TEMP/NFE-ENTRADA.XLS', '/home/felipecn/Downloads/TEMP/NFSE-TOMADO.XLS')
nfe_saida = saida('/home/felipecn/Downloads/TEMP/NFE-SAIDA.XLS', '/home/felipecn/Downloads/TEMP/NFSE-PRESTADO.XLS', '/home/felipecn/Downloads/TEMP/SAT.XLS')
print(nfe_saida)

