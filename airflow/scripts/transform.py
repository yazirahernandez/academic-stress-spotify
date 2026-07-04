def transform(df):
    return df[(df["tempo"] > 60) & (df["tempo"] < 200)]
