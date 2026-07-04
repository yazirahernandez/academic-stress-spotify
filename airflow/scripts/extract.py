import pandas as pd
import numpy as np

def extract_dummy():
    np.random.seed(42)
    n = 600

    return pd.DataFrame({
        "track_id": range(n),
        "tempo": np.random.normal(120, 22, n),
        "energy": np.random.uniform(0.2, 1.0, n),
        "week_type": np.random.choice(["normal", "stress"], n, p=[0.6, 0.4])
    })
