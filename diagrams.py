import structlog
from matplotlib import pyplot as plt

from general_functions import drop_extreme_values

logger = structlog.get_logger(__name__)


def get_fuel_type_diagram(df):
    if "fuel" not in df.columns:
        logger.error("DataFrame does not have 'fuel' column")
        return
    fuels = df["fuel"].value_counts()
    logger.info(f"Fuel types: {fuels}")
    plt.pie(fuels, autopct="%.1f%%", labels=fuels.index)
    plt.legend(fuels.index)
    plt.title("Fuel Type Distribution")
    plt.show()


def create_diagram_dependence_price_of_year(df):
    df = drop_extreme_values(df, "price")
    df = drop_extreme_values(df, "year")
    if "price" not in df.columns or "year" not in df.columns:
        logger.error(
            "DataFrame does not have necessary columns for price vs. year analysis"
        )
        return
    plt.scatter(df["price"], df["year"])
    plt.title("Dependence of Price on Year of Manufacture")
    plt.xlabel("Price")
    plt.ylabel("Year")
    plt.show()
