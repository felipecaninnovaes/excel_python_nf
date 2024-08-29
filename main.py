from typing import List, Any
import openpyxl
import datetime
from utils import FileChecker, FileUtils, GenericUtils

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
        FileUtils().remove_file(sheet_path)
    
    return values

def filter_data_by_date_and_value(file_path: str, table_name: str, init_line: int, date_col: int, value_col: int) -> List[List[Any]]:
    dates: list = extract_sheet_data(file_path, table_name, init_line, date_col, False)
    values: list = extract_sheet_data(file_path, table_name, init_line, value_col, True)
    merged_lists = GenericUtils.merge_lists(dates, values)
    values_summed = sum_values(merged_lists)
    monthly_sums = sum_values_by_month(values_summed)
    return monthly_sums

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

def aggregate_monthly_values(data: list) -> dict:
    # Inicializa um dicionário para armazenar as somas dos valores por mês
    monthly_sums = {}

    # Itera sobre a lista de listas
    for sublist in data:
        # Itera sobre os pares de mês e valor na sublista
        for month_value_pair in sublist:
            if month_value_pair is not None:
                month, value = month_value_pair
                if month in monthly_sums:
                    monthly_sums[month] += value
                else:
                    monthly_sums[month] = value

    return monthly_sums

def entrada(nfe_path: str, nfse_path: str) -> dict:
    # Valores de configuração da planilha de NFE
    NFE_ENTRADA_INIT_ROW: int = 5
    NFE_ENTRADA_DATE_COL: int = 2
    NFE_ENTRADA_VALUE_COL: int = 10
    
    # Valores de configuração da planilha de NFSE
    NFSE_TOMADO_INIT_ROW: int = 5
    NFSE_TOMADO_DATE_COL: int = 1
    NFSE_TOMADO_VALUE_COL: int = 8
    
    total_values_nfe_entrada = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfe_path), 'Notas', NFE_ENTRADA_INIT_ROW, NFE_ENTRADA_DATE_COL, NFE_ENTRADA_VALUE_COL)
    total_values_nfse_tomado = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfse_path), 'Notas', NFSE_TOMADO_INIT_ROW, NFSE_TOMADO_DATE_COL, NFSE_TOMADO_VALUE_COL)

    total_values_nfse_nfe_entrada = GenericUtils.merge_lists(total_values_nfe_entrada, total_values_nfse_tomado)
    total_values_nfse_nfe_entrada = aggregate_monthly_values(total_values_nfse_nfe_entrada)
    return total_values_nfse_nfe_entrada

def saida(nfe_path: str, nfse_path: str, sat_path: str) -> dict:
    # Valores de configuração da planilha de NFE
    NFE_SAIDA_INIT_ROW: int = 5
    NFE_SAIDA_DATE_COL: int = 2
    NFE_SAIDA_VALUE_COL: int = 10
    
    # Valores de configuração da planilha de NFSE
    NFSE_EMITIDO_INIT_ROW: int = 5
    NFSE_EMITIDO_DATE_COL: int = 1
    NFSE_EMITIDO_VALUE_COL: int = 8
    
    # Valores de configuração da planilha de SAT
    SAT_INIT_ROW: int = 5
    SAT_DATE_COL: int = 1
    SAT_VALUE_COL: int = 6
    
    total_values_nfe_saida = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfe_path), 'Notas', NFE_SAIDA_INIT_ROW, NFE_SAIDA_DATE_COL, NFE_SAIDA_VALUE_COL)
    total_values_nfse_emitido = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfse_path), 'Notas', NFSE_EMITIDO_INIT_ROW, NFSE_EMITIDO_DATE_COL, NFSE_EMITIDO_VALUE_COL)
    total_values_sat = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(sat_path), 'CF-e SAT', SAT_INIT_ROW, SAT_DATE_COL, SAT_VALUE_COL)

    total_values_nfse_nfe_saida = GenericUtils.merge_lists(total_values_nfe_saida, total_values_nfse_emitido, total_values_sat)
    total_values_nfse_nfe_saida = aggregate_monthly_values(total_values_nfse_nfe_saida)
    return total_values_nfse_nfe_saida

# Exemplo de uso
nfe_entrada = entrada('/home/felipecn/Downloads/TEMP/NFE-ENTRADA.xls', '/home/felipecn/Downloads/TEMP/NFSE-TOMADO.xls')
nfe_saida = saida('/home/felipecn/Downloads/TEMP/NFE-SAIDA.xls', '/home/felipecn/Downloads/TEMP/NFSE-PRESTADO.xls', '/home/felipecn/Downloads/TEMP/SAT.xls')
print(nfe_entrada)

