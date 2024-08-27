from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(*args, **kwargs) -> None:
    
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    project_name = kwargs['project_name']
    dataset_name = kwargs['dataset']
    
    for arg in args:
        df, table_name = arg
        table_id = f"{project_name}.{dataset_name}.{table_name}"



        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            df,
            table_id,
            if_exists='replace',
        )
