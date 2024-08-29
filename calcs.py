import pandas as pd
import os, logging
from typing import List, Any

logging.basicConfig(level=logging.INFO)

class CalculateUtils:
    # from utils import FileUtils
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def calculate_total_by_date(date: List[List[Any]]) -> List[List[Any]]:
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
    def calculate_total_by_month(data_value_list: List[List[Any]]) -> List[List[Any]]:
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
