from extract_data import (extract_freds, save_raw_data, save_extracted_data)
from transform import transform_extracted_csv
from logger import get_logger
from config import load_config
logger = get_logger("fred-pipeline")
def run_pipeline():
    config = load_config()

    api_key = config["api"]["fred_api_key"]
    series_list = config["api"]["series"]
    observation_start = config["api"]["observation_start"]

    raw_dir = config["paths"]["raw"]
    extracted_dir = config["paths"]["extracted"]
    curated_path = config["paths"]["curated"]

    logger.info("Starting FRED extraction")

    all_rows = []

    for series in series_list:
        logger.info(f"Fetching series: {series}")

        rows, payload = extract_freds(
            series_id=series,
            api_key=api_key,
            observation_start=observation_start
        )

        save_raw_data(payload, raw_dir)
        all_rows.extend(rows)

    extracted_path = save_extracted_data(all_rows, extracted_dir)

    logger.info("Starting transform step")
    transform_extracted_csv(str(extracted_path), curated_path)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    run_pipeline()