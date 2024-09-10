from typing import List, Any
import openpyxl
import datetime
from utils import FileChecker, FileUtils, GenericUtils
from calcs import CalculateUtils
from graph import plotar_entrada_saida

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
    values_summed = CalculateUtils.calculate_total_by_date(merged_lists)
    monthly_sums = CalculateUtils.calculate_total_by_month(values_summed)
    return monthly_sums

def entrada(nfe_path: str, nfse_path: str) -> dict:
    # Valores iniciais das listas
    total_values_nfe_entrada: list = []
    total_values_nfse_tomado: list = []
    total_values_nfse_nfe_entrada: dict = {}
    
    # Valores de configuração da planilha de NFE
    NFE_ENTRADA_INIT_ROW: int = 5
    NFE_ENTRADA_DATE_COL: int = 2
    NFE_ENTRADA_VALUE_COL: int = 10
    
    # Valores de configuração da planilha de NFSE
    NFSE_TOMADO_INIT_ROW: int = 5
    NFSE_TOMADO_DATE_COL: int = 1
    NFSE_TOMADO_VALUE_COL: int = 8
    
    if nfe_path is not None:
        total_values_nfe_entrada = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfe_path), 'Notas', NFE_ENTRADA_INIT_ROW, NFE_ENTRADA_DATE_COL, NFE_ENTRADA_VALUE_COL)
    if nfse_path is not None:
        total_values_nfse_tomado = filter_data_by_date_and_value(FileChecker().check_xlsx_as_valid(nfse_path), 'Notas', NFSE_TOMADO_INIT_ROW, NFSE_TOMADO_DATE_COL, NFSE_TOMADO_VALUE_COL)

    if nfe_path is not None and nfse_path is not None:
        total_values_nfse_nfe_entrada = GenericUtils.merge_lists(total_values_nfe_entrada, total_values_nfse_tomado)
        total_values_nfse_nfe_entrada = CalculateUtils.aggregate_monthly_values(total_values_nfse_nfe_entrada)
    elif nfe_path is not None and nfse_path is None:
        total_values_nfe_entrada = CalculateUtils.aggregate_monthly_values(total_values_nfe_entrada)
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
    total_values_nfse_nfe_saida = CalculateUtils.aggregate_monthly_values(total_values_nfse_nfe_saida)
    return total_values_nfse_nfe_saida

# Exemplo de uso
# nfe_entrada = entrada('/home/felipecn/Downloads/TEMP/NFE-ENTRADA.xls', '/home/felipecn/Downloads/TEMP/NFSE-TOMADO.xls')
# nfe_saida = saida('/home/felipecn/Downloads/TEMP/NFE-SAIDA.xls', '/home/felipecn/Downloads/TEMP/NFSE-PRESTADO.xls', '/home/felipecn/Downloads/TEMP/SAT.xls')
# plotar_entrada_saida(nfe_entrada, nfe_saida)
# print(nfe_entrada)
# print(nfe_saida)
