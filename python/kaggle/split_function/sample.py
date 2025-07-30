from calendar import month_name

import pandas as pd
import seaborn as sns
from custom_split.custom_timeseries_split import SlideWindowTimeSeriesSplit
from matplotlib import pyplot as plt


def create_sample_dataframe(is_shuffle: bool = False, verbose: bool = True):
    # 航空機の旅客数を記録したデータセットを読み込む
    data_df = sns.load_dataset("flights")

    # 時系列のカラムを用意する
    month_name_mappings = {name[:3]: str(n).zfill(2) for n, name in enumerate(month_name)}

    data_df["month"] = data_df["month"].apply(lambda x: month_name_mappings[x])
    data_df["year-month"] = data_df.year.astype(str) + "-" + data_df.month.astype(str)
    data_df["year-month"] = pd.to_datetime(data_df["year-month"], format="%Y-%m")

    if verbose:
        print("-" * 100)
        print(data_df.describe())
        print("-" * 100)
        print(data_df.shape)
        print("-" * 100)
        print(data_df.head(3))
        print("-" * 100)
        print("")

    if is_shuffle:
        data_df = data_df.sample(frac=1)

    return data_df


def plt_train_test_index(
    df: pd.DataFrame,
    x_label: str,
    y_label: str,
    train_index_list: list[list[int]],
    test_index_list: list[list[int]],
    title: str | None = None,
    figsize: tuple = (12, 8),
):
    if len(train_index_list) != len(test_index_list):
        raise ValueError("[train_index_list] and [test_index_list] sizes do not match")

    fig, axes = plt.subplots(len(train_index_list), 1, figsize=figsize)

    for i, (train_index, test_index) in enumerate(zip(train_index_list, test_index_list, strict=False)):
        # 元のデータを描く
        sns.lineplot(data=df, x=x_label, y=y_label, ax=axes[i], label="original")
        # 学習用データを描く
        sns.lineplot(data=df.iloc[train_index], x=x_label, y=y_label, ax=axes[i], label="train")
        # テスト用データを描く
        sns.lineplot(data=df.iloc[test_index], x=x_label, y=y_label, ax=axes[i], label="test")

        axes[i].grid()

    # グラフを表示する
    if title:
        fig.suptitle(title)
    plt.legend()
    plt.show()


def sample_slide_window_split(verbose: bool = True):
    n_splits = 3
    train_ratio = 0.8

    dataset_df = create_sample_dataframe(is_shuffle=True, verbose=verbose)

    if verbose:
        print("SlideWindowSplit")
        print(f"data size: {len(dataset_df)}, n_split{n_splits}")
        print("-" * 100)

    cv = SlideWindowTimeSeriesSplit("year-month", n_splits=n_splits, train_ratio=train_ratio)

    train_index_list, test_index_list = [], []
    for train_index, valid_index in cv.split(dataset_df):
        train = dataset_df.iloc[train_index]
        valid = dataset_df.iloc[valid_index]

        if verbose:
            print(f"train shape: {train.shape}, valid shape: {valid.shape}")
            print(f"train index: {train_index}, valid index: {valid_index}")

        train_index_list.append(train_index)
        test_index_list.append(valid_index)

    if verbose:
        print("-" * 100)
        print()

    # 描画
    plt_train_test_index(
        dataset_df, "year-month", "passengers", train_index_list, test_index_list, "SlideWindowTimeSeriesSplit"
    )


if __name__ == "__main__":
    sample_slide_window_split(False)
