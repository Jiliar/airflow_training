import pandas as pd
import os
import logging
from datetime import datetime
from components.functions.i_transform import IBaseDataTransformer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    fmt='%(asctime)s [%(levelname)s] %(name)s - %(filename)s:%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class SalesDataTransformer(IBaseDataTransformer):
    """Transformador específico para datos de ventas"""
    
    def __init__(
        self,
        input_path_bash: str = '/tmp/sales_db_bash.csv',
        input_path_py: str = '/tmp/sales_db_py.csv',
        output_path: str = '/tmp/sales_data_transformed.csv'
    ):
        self.input_path_bash = input_path_bash
        self.input_path_py = input_path_py
        self.output_path = output_path
        
    def _validate_inputs(self) -> None:
        """Valida que existan los archivos de entrada"""
        if not all(os.path.exists(p) for p in [self.input_path_bash, self.input_path_py]):
            missing = [p for p in [self.input_path_bash, self.input_path_py] if not os.path.exists(p)]
            raise FileNotFoundError(f"Archivos no encontrados: {missing}")
    
    def _process_data(self) -> pd.DataFrame:
        """Procesamiento completo de los datos"""
        # Leer datos
        data_bash = pd.read_csv(self.input_path_bash)
        data_py = pd.read_csv(self.input_path_py)
        
        # Unir datos
        merged = pd.concat([data_bash, data_py], ignore_index=True)

        # Estandarizar columnas
        col_map = {'date': 'ddate', 'day': 'ddate'}
        merged = merged.rename(columns={k: v for k, v in col_map.items() if k in merged.columns})
        
        # Agrupar datos por tienda y fecha, sumando ventas
        grouped = merged.groupby(['store', 'ddate'], as_index=False)['sales'].sum()
        
        # Agregar columna created_at con la hora actual
        grouped['created_at'] = datetime.now().isoformat()
        
        # Reordenar columnas según el orden esperado en el COPY
        cols = sorted(grouped.columns, key=lambda x: ['ddate', 'store', 'sales', 'created_at'].index(x))
        grouped = grouped[cols]

        return grouped
    
    def transform(self, **kwargs) -> str:
        """Ejecuta el pipeline completo"""
        self._validate_inputs()
        result = self._process_data()
        result.to_csv(self.output_path, sep='\t', index=False, header=False)
        
        if 'ti' in kwargs:  # Para compatibilidad con XCom de Airflow
            kwargs['ti'].xcom_push(key='transformed_data_path', value=self.output_path)
            
        return self.output_path