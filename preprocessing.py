import pandas as pd


import pandas as pd


def preprocess_data(path):
    df = pd.read_csv(path, encoding="ISO-8859-1")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Remove irrelevant columns
    irrelevant_cols = [
        "url",
        "address",
        "phone",
        "locality_verbose",
        "switch_to_order_menu",
        "rating_color",
        "rating_text",
    ]
    df.drop(columns=[col for col in irrelevant_cols if col in df.columns], inplace=True)

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Drop rows with missing values in important columns
    df.dropna(
        subset=["cuisines", "locality", "average_cost_for_two", "aggregate_rating"],
        inplace=True,
    )

    # Normalize text
    df["cuisines"] = df["cuisines"].str.lower().str.strip()
    df["locality"] = df["locality"].str.lower().str.strip()

    # Extract primary cuisine
    df["primary_cuisine"] = df["cuisines"].apply(
        lambda x: x.split(",")[0].strip() if isinstance(x, str) else x
    )

    # Numeric conversions
    df["average_cost_for_two"] = pd.to_numeric(
        df["average_cost_for_two"], errors="coerce"
    )
    df["aggregate_rating"] = pd.to_numeric(df["aggregate_rating"], errors="coerce")

    # Cost buckets
    def cost_bucket(cost):
        if cost < 300:
            return "low"
        elif cost < 700:
            return "medium"
        else:
            return "high"

    df["price_range"] = df["average_cost_for_two"].apply(cost_bucket)

    # Scale ratings to 1–5
    df["rating_scaled"] = df["aggregate_rating"].clip(lower=1.0, upper=5.0).round(1)

    # Final selection
    keep_cols = [
        "restaurant_name",
        "locality",
        "primary_cuisine",
        "price_range",
        "rating_scaled",
        "votes",
        "currency",
    ]
    df = df[[col for col in keep_cols if col in df.columns]]

    return df
