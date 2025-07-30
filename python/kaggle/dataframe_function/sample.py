import pandas as pd
from reducing_dataframe.reducing_dataframe import reduce_mem_usage
from sklearn.datasets import load_iris


def create_sample_dataframe(verbose: bool = True):
    iris = load_iris()
    data_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    target_df = pd.DataFrame(data=iris.target, columns=["target"])
    dataset_df = pd.concat([data_df, target_df], axis=1)

    if verbose:
        print("-" * 100)
        print(dataset_df.describe())
        print("-" * 100)
        print(dataset_df["target"].value_counts())
        print("-" * 100)
        print(dataset_df.shape)
        print("-" * 100)
        print("")

    return dataset_df


if __name__ == "__main__":
    df = create_sample_dataframe()
    mem_df, na = reduce_mem_usage(df)
