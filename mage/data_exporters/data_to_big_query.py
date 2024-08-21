from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(list_of_args, *args, **kwargs):

    project_name = kwargs['project_name']
    dataset_name = kwargs['dataset']
    latest_record_folder = 0
    for arg in list_of_args:
        df, table_name, latest_record = arg

        if latest_record >= latest_record_folder:
            latest_record_folder = latest_record

        table_id = f'{project_name}.{dataset_name}.{table_name}'
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'default'

        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='append',
        )
    return latest_record_folder
