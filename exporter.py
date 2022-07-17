import pandas as pd

def save_to_csv(jobs, word):
    df = pd.DataFrame(jobs)
    df.to_csv(f"SerachResults_{word}.csv", index=False)