from airflow.providers.postgres.hooks.postgres import PostgresHook

from components.functions.i_load import ILoader

class PostgresLoader(ILoader):
    def __init__(self, conn_id='postgresql_docker_conn', table='sales_data', csv_file='/tmp/sales_data_transformed.csv'):
        self.conn_id = conn_id
        self.table = table
        self.csv_file = csv_file

from airflow.providers.postgres.hooks.postgres import PostgresHook

class PostgresLoader:
    def __init__(self, conn_id, table, csv_file, columns=['ddate', 'store', 'sales', 'created_at']):
        self.conn_id = conn_id
        self.table = table
        self.csv_file = csv_file
        self.columns = columns

    def load(self):
        pd_hook = PostgresHook(postgres_conn_id=self.conn_id)

        column_list = f"({', '.join(self.columns)})" if self.columns else ""

        copy_sql = f"""
            COPY {self.table} {column_list}
            FROM STDIN WITH (
                FORMAT csv,
                DELIMITER E'\t',
                NULL '',
                HEADER FALSE
            )
        """

        with open(self.csv_file, "r") as f:
            pd_hook.copy_expert(sql=copy_sql, filename=self.csv_file)