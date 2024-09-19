import structlog

from general_functions import drop_extreme_values

logger = structlog.get_logger(__name__)


def compare_car_types(df, car_type_1="bmw", car_type_2="mercedes-benz"):
    if "manufacturer" not in df.columns or "year" not in df.columns:
        logger.error("DataFrame does not have 'manufacturer' or 'year' columns")
        return
    all_manufacturers = df["manufacturer"].unique()
    logger.info(f"All manufacturers: {all_manufacturers}")

    df_filtered = df.loc[
        (df["manufacturer"].isin([car_type_1, car_type_2])) & (df["year"] > 2018)
    ]
    df_grouped = (
        df_filtered.groupby(by="manufacturer").agg({"price": "mean"}).reset_index()
    )
    logger.info(
        f"Price comparison between {car_type_1} and {car_type_2}:\n {df_grouped}"
    )
    return df_grouped


def get_odometers_min_max(df):
    df_second = df[["manufacturer", "model", "odometer"]].loc[df["year"] > 2020]
    df_second = drop_extreme_values(df_second, "odometer")

    df_second = df_second.drop_duplicates(subset=["manufacturer"]).reset_index(
        drop=True
    )

    min_odometer = (
        df_second.loc[df_second["odometer"] > 0]
        .sort_values(by="odometer", ascending=True)
        .head(3)
    )
    max_odometer = df_second.sort_values(by="odometer", ascending=False).head(3)

    logger.info(f"Min odometer readings (excluding 0):\n{min_odometer}")
    logger.info(f"Max odometer readings:\n{max_odometer}")

    return min_odometer, max_odometer


def get_top_100_expensive_cars_count(df, car_make="mercedes-benz"):
    df_third = df[["manufacturer", "price"]]
    df_third = df_third.drop_duplicates().reset_index(drop=True)
    df_third = df_third.sort_values(by="price", ascending=False)
    df_top_100 = df_third.head(100)
    logger.info(f"Top 100 most expensive cars:\n{df_top_100}")
    car_count = df_top_100["manufacturer"].value_counts().get(car_make, 0)

    logger.info(f"{car_count} {car_make} cars are in the top 100 most expensive cars.")

    return car_count
