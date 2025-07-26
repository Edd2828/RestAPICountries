import concurrent.futures

from utils.config import get_etls_config
from utils.base import PostgresBase


# extract from api
etls_config = get_etls_config()

def create_extractor(class_name, sort_data, file_name, filters):
    return class_name(sort_data=sort_data, file_name=file_name, filters=filters)

def run_extraction(extractor, file_name):
    extractor.save_to_csv()
    print(f"API Extraction completed: {file_name}")

def run_api_etl():
    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_extraction, create_extractor(etl['class'], etl['sort_data'], etl['file_name'], etl['filters']), etl['file_name']) for etl in etls_config]
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()


# import to postgres
def create_sql_extractor(class_name, etl_stage, table_name):
    return class_name(etl_stage, table_name)

def run_sql_extraction(sql_extractor, table_name):
    sql_extractor.execute_sql()
    print(f"Import to postgres {sql_extractor.etl_stage} {table_name}")

def run_sql_import(etl_stage):
    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_sql_extraction, create_sql_extractor(PostgresBase, etl_stage, etl['file_name']), etl['file_name']) for etl in etls_config]
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":

    # Rest API from source
    print("1. Extracting API data to csv...")
    run_api_etl()

    create_schema = PostgresBase('staging', 'create_schema')
    create_schema.execute_sql('CREATE SCHEMA IF NOT EXISTS staging;')
    print()

    # Import to Staging Tables
    print("2. COPY csv files to Staging...")
    run_sql_import('staging')

    create_schema = PostgresBase('warehouse', 'create_schema')
    create_schema.execute_sql('CREATE SCHEMA IF NOT EXISTS warehouse;')
    print()

    # Upsert to warehouse Tables
    print("3. Merging from Staging to warehouse...")
    run_sql_import('warehouse')

    # staging clear down
    staging_clear_down = PostgresBase('staging', 'staging_clear_down')
    staging_clear_down.execute_sql(staging_clear_down.read_staging_clear_down())