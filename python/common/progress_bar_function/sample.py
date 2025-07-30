from time import sleep

from custom_progress_bar.progress_bar import ProgressBar

pb = ProgressBar(n_trials=10)

for _ in range(10):
    # 実行ごとに進捗を1つ進める
    pb.process()
    sleep(0.1)
