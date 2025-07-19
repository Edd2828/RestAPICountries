import concurrent.futures

from utils.config import get_etls_config
from utils.base import PostgresBase


# extract from api
etls_config = get_etls_config()

def create_extractor(class_name, sort_data, file_name, filters):
    return class_name(sort_data=sort_data, file_name=file_name, filters=filters)

def run_extraction(extractor, file_name):
    extractor.save_to_csv()
    print(f"Extraction from api completed: {file_name}")

def run_api_etl():
    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_extraction, create_extractor(etl['class'], etl['sort_data'], etl['file_name'], etl['filters']), etl['file_name']) for etl in etls_config]
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()


# import to postgres
def create_sql_extractor(class_name, table_name):
    return class_name(table_name)

def run_sql_extraction(sql_extractor, table_name):
    sql_extractor.execute_sql()
    print(f"Import to postgres: {table_name}")

def run_sql_import():
    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_sql_extraction, create_sql_extractor(PostgresBase, etl['file_name']), etl['file_name']) for etl in etls_config]
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":

    # Rest API from source
    run_api_etl()

    # Import to Postgres
    run_sql_import()
