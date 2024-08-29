import pandas as pd
import os, logging
from typing import List, Any

logging.basicConfig(level=logging.INFO)

class FileChecker:
    # from utils import FileUtils
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
            
    def check_xlsx_as_valid(self, file_path: str) -> str:
        # Verificar a existência do arquivo
        if not os.path.exists(file_path):
            logging.error(f"Arquivo {file_path} não encontrado.")
            return file_path
        
        # Verificar a extensão do arquivo
        file_base_path, file_extension = os.path.splitext(file_path)
        
        if file_extension.upper() in ['.XLS', '.XLSX']:
            new_path = f'{file_base_path}{file_extension.lower()}'
            if file_path != new_path:
                FileUtils().rename_extension_file(file_path, new_path)
                file_path = new_path
        
        # Se for .xls, converter para .xlsx
        if file_extension.lower() == '.xls':
            xlsx_path = file_path.replace('.xls', '.xlsx')
            self.convert_xls_to_xlsx(file_path, xlsx_path)
            file_path = xlsx_path
        
        return file_path

    def convert_xls_to_xlsx(self, xls_path: str, xlsx_path: str):
        try:
            # Ler o arquivo .xls
            df = pd.read_excel(xls_path, sheet_name=None)
            # Salvar como .xlsx
            with pd.ExcelWriter(xlsx_path) as writer:
                for sheet_name, data in df.items():
                    data.to_excel(writer, sheet_name=sheet_name)
            logging.info(f"Arquivo convertido de {xls_path} para {xlsx_path}")
        except FileNotFoundError:
            logging.error(f"Arquivo {xls_path} não encontrado.")
        except PermissionError:
            logging.error(f"Permissão negada para ler {xls_path}.")
        except Exception as e:
            logging.error(f"Erro ao converter arquivo: {e}")

class FileUtils:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def rename_extension_file(self, old_path: str, new_path: str) -> None:
        if old_path == new_path:
            logging.info(f"Arquivo já está com a extensão correta: {old_path}")
            return
        
        try:
            os.rename(old_path, new_path)
            logging.info(f"Arquivo renomeado de {old_path} para {new_path}")
        except FileNotFoundError:
            logging.error(f"Arquivo {old_path} não encontrado.")
        except PermissionError:
            logging.error(f"Permissão negada para renomear {old_path}.")
        except Exception as e:
            logging.error(f"Erro ao renomear arquivo: {e}")
    
    def remove_file(self, file_path):
        os.remove(file_path)
class GenericUtils:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
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

# teste = FileChecker().check_xlsx_as_valid('/home/felipecn/Downloads/TEMP/NFE-SAIDA.XLS')
# print(teste)