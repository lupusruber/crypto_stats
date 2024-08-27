from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



def id_to_dict(df):
    return dict(zip(df['id'], df['id_sk']))

@data_loader
def load_data_from_big_query(data, *args, **kwargs):

    project_name = kwargs['project_name']
    dataset_name = kwargs['dataset']

    df, _ = data

    id_dict = id_to_dict(df)

    query = f"SELECT * FROM {project_name}.{dataset_name}.markets"
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    return BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query), id_dict 
   



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
