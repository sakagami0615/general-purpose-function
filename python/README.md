# general-purpose-function: python

よく使うソースコードを集約したリポジトリ

## Functional document (common)

- [logger_function](./common/logger_function/README.md)
- [progress_bar_function](./common/progress_bar_function/README.md)

## Functional document (kaggle)

- [dataframe_function](./kaggle/dataframe_function/README.md)
- [split_function](./kaggle/split_function/README.md)

## Appendix: code check command

```bash
poetry run ruff check . --fix
poetry run ruff format .
```
