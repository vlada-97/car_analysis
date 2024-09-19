import structlog

logger = structlog.get_logger(__name__)


def get_missing_values_sum(df):
    missing_values = df.isnull().sum()
    logger.info(f"Missing values: {missing_values}, sum:{missing_values.sum()}")
    return missing_values.sum()


def get_columns_with_missing_values(df):
    missing_values = df.isnull().sum()
    columns_with_missing_values = missing_values[missing_values > 0].index
    logger.info(f"Columns with missing values: {columns_with_missing_values}")
    return columns_with_missing_values


def drop_extreme_values(df, col, lower_quantile=0.005, upper_quantile=0.995):
    quantiles = df[col].quantile([lower_quantile, upper_quantile])
    logger.info(f"Quantiles for {col}: {quantiles}")
    rows_to_drop = df[
        (df[col] < quantiles[lower_quantile]) | (df[col] > quantiles[upper_quantile])
    ].index
    logger.info(f"Rows with extreme values in {col}: {len(rows_to_drop)}")
    return df.drop(rows_to_drop)


def handle_missing_values(df):
    columns_with_missing_values = get_columns_with_missing_values(df)
    for col in columns_with_missing_values:
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode().iloc[0])
        else:
            df[col] = df[col].fillna(df[col].median())
    logger.info("Missing values have been handled")


def drop_columns_with_missing_values(df):
    columns_with_missing_values = get_columns_with_missing_values(df)
    df = df.drop(columns=columns_with_missing_values)
    logger.info(f"Columns with missing values dropped: {columns_with_missing_values}")
    df = df.dropna()
    return df
