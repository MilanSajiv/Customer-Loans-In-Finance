import yaml
from sqlalchemy import create_engine
import pandas as pd
import psycopg2


class RDSDatabaseConnector:
    def __init__(self, credential) -> None:
        self.loaded_creds = self.load_file(credential)
        self.engine = self.initialise_engine()
    def load_file(self, credential):
        with open(credential, 'r') as file:
            credential = yaml.safe_load(file)
        print(credential)
        return credential
    def initialise_engine(self):
        creds = self.loaded_creds
        DATABASE_TYPE = 'postgresql'
        HOST = creds["RDS_HOST"]
        PASSWORD = creds["RDS_PASSWORD"]
        USER = creds["RDS_USER"]
        DATABASE = creds["RDS_DATABASE"]
        PORT = 5432
        engine = create_engine(f"{DATABASE_TYPE}+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        return engine  
    def extract_data(self, table_name):
        data = pd.read_sql_query(f"SELECT * FROM {table_name}", self.engine)
        return data    
    def save_to_csv(self, data, credential):
        data.to_csv(credential, index=False)
    def load_csv(self, data_csv):
        df = pd.read_csv(data_csv)
        return df

if __name__ == '__main__':
    connector = RDSDatabaseConnector('main\credentials.yaml')
    connector.initialise_engine()
    data = connector.extract_data('loan_payments')  
    connector.save_to_csv(data, 'data.csv')
    df = connector.load_csv('data.csv')
    print(df)
    print(df.shape)