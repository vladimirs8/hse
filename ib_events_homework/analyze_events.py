#!/usr/bin/env python3
"""Load security events from JSON, summarize the `signature` field, and plot it."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


BASE_DIR = Path(__file__).resolve().parent


def load_events(json_path: Path) -> pd.DataFrame:
    """Read a JSON array of event objects into a pandas DataFrame."""
    if not json_path.is_file():
        raise FileNotFoundError(
            f"JSON-файл не найден: {json_path}\n"
            "Положите events.json рядом со скриптом или укажите путь через --input."
        )

    try:
        # В events.json ожидается JSON-массив объектов (orient='records').
        df = pd.read_json(json_path, orient="records")
    except ValueError as exc:
        raise ValueError(
            f"Не удалось прочитать {json_path} как JSON-массив записей. "
            "Проверьте структуру файла."
        ) from exc

    if df.empty:
        raise ValueError("JSON-файл прочитан, но в нём нет событий.")

    if "signature" not in df.columns:
        raise KeyError(
            "В JSON отсутствует обязательное поле 'signature'. "
            f"Найдены поля: {', '.join(map(str, df.columns))}"
        )

    # Удаляем строки без типа события и лишние пробелы в названиях типов.
    df["signature"] = df["signature"].astype("string").str.strip()
    df = df.dropna(subset=["signature"])
    df = df[df["signature"] != ""].copy()

    if df.empty:
        raise ValueError("После проверки поля 'signature' не осталось событий.")

    return df


def analyze_signatures(df: pd.DataFrame) -> pd.DataFrame:
    """Count events for every unique signature, from most to least frequent."""
    counts = (
        df["signature"]
        .value_counts()
        .rename_axis("signature")
        .reset_index(name="count")
    )

    print("\n=== Анализ событий информационной безопасности ===")
    print(f"Всего событий: {len(df)}")
    print(f"Уникальных типов событий: {df['signature'].nunique()}")
    print("\nРаспределение событий по полю 'signature':")
    print(counts.to_string(index=False))

    return counts


def plot_signatures(counts: pd.DataFrame, output_dir: Path) -> Path:
    """Create and save a horizontal bar chart of event counts by signature."""
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_path = output_dir / "signature_distribution.png"

    sns.set_theme(style="whitegrid")
    figure_height = max(5, 0.55 * len(counts))
    fig, ax = plt.subplots(figsize=(11, figure_height))

    sns.barplot(
        data=counts,
        x="count",
        y="signature",
        color="steelblue",
        ax=ax,
    )

    ax.set_title("Распределение событий ИБ по типам", pad=14)
    ax.set_xlabel("Количество событий")
    ax.set_ylabel("Тип события (signature)")
    ax.bar_label(ax.containers[0], padding=4, fmt="%d")
    ax.set_xlim(0, counts["count"].max() * 1.15)

    fig.tight_layout()
    fig.savefig(chart_path, dpi=150, bbox_inches="tight")
    print(f"\nГрафик сохранён: {chart_path}")

    # При наличии графического интерфейса окно с графиком также откроется.
    plt.show()
    plt.close(fig)

    return chart_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Анализ типов событий ИБ из JSON-файла по полю signature."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=BASE_DIR / "events.json",
        help="Путь к JSON-файлу (по умолчанию: events.json рядом со скриптом).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=BASE_DIR / "output",
        help="Каталог для результатов (по умолчанию: output).",
    )
    args = parser.parse_args()

    df = load_events(args.input)
    counts = analyze_signatures(df)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = args.output_dir / "signature_counts.csv"
    counts.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"Таблица с подсчётами сохранена: {csv_path}")

    plot_signatures(counts, args.output_dir)


if __name__ == "__main__":
    main()
