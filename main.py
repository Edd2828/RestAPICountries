import concurrent.futures

from utils.config import get_etls_config


etls_config = get_etls_config()

def create_extractor(class_name, sort_data, file_name, filters):
    return class_name(sort_data=sort_data, file_name=file_name, filters=filters)

def run_extraction(extractor, file_name):
    extractor.save_to_csv()
    print(f"Extraction completed for {file_name}")

def run_api_etl():
    # Execute in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_extraction, create_extractor(etl['class'], etl['sort_data'], etl['file_name'], etl['filters']), etl['file_name']) for etl in etls_config]
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()


if __name__ == "__main__":
    run_api_etl()