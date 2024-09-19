import pprint
import pandas as pd
import structlog

from analytics import (
    compare_car_types,
    get_odometers_min_max,
    get_top_100_expensive_cars_count,
)
from general_functions import (
    handle_missing_values,
    get_missing_values_sum,
    drop_columns_with_missing_values,
)

from diagrams import (
    get_fuel_type_diagram,
    create_diagram_dependence_price_of_year,
)  # noqa

logger = structlog.get_logger(__name__)


def read_csv(csv_name):
    df = pd.read_csv(csv_name)
    logger.info(f"Read {csv_name}: {df.shape[0]} rows, {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    df = read_csv("vehicles.csv")  #  some csv file
    handle_missing_values(df)
    sum = get_missing_values_sum(df)
    if sum > 0:
        # есть колонки с пропусками (NaN), но их можно удалить
        df = drop_columns_with_missing_values(df)
        sum = get_missing_values_sum(df)
    pprint.pprint(df)
    # diagrams
    # get_fuel_type_diagram(df)
    # create_diagram_dependence_price_of_year(df)

    compare_car_types(df, car_type_1="bmw", car_type_2="mercedes-benz")
    compare_car_types(df, car_type_1="audi", car_type_2="volvo")
    get_odometers_min_max(df)
    get_top_100_expensive_cars_count(df, "mercedes-benz")
    get_top_100_expensive_cars_count(df, "audi")
