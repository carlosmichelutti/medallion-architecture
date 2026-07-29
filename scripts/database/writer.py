import pandas as pd

from scripts.database.session import engine


def write_dataframe_to_table(
    dataframe: pd.DataFrame,
    table_name: str,
    schema: str = 'public',
    if_exists: str = 'replace',
) -> int:

    insert_rows = dataframe.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists=if_exists,
        index=False
    )

    print(f'DataFrame written {insert_rows} row(s) to table: {schema}.{table_name} (if_exists={if_exists})')
    return insert_rows