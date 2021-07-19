import io
from pathlib import Path

import pandas as pd
from flask import render_template, Response
from pandas import read_excel

from app import app
from config import BASE_DIR


@app.route("/matrix", methods=["GET"])
def correlation_matrix():
    """Эндпоинт возвращающий корреляционные матрицы и сред.кв. отклонение"""
    table = read_excel(Path(BASE_DIR / "test.xlsx"))
    table["Profit"] = table.sort_values(
        ["Ticker", "Date"]
    ).groupby("Ticker")["Price"].apply(lambda x: x - x.shift(1))
    corr_matrix = table.corr()
    ticker_matrix = table.groupby("Ticker").corr()
    std_ticker = table.groupby("Ticker")["Profit"].std()
    response_data = {
        "corr_matrix": pd.DataFrame(corr_matrix).to_html(),
        "ticker_matrix": pd.DataFrame(ticker_matrix).to_html(),
        "std_ticker": pd.DataFrame(std_ticker).to_html()
    }
    return render_template("correlation_matrix.html", **response_data)


@app.route("/graph", methods=["GET"])
def graph():
    """Эндпоинт возвращающий график цен"""
    table = read_excel(Path(BASE_DIR / "test.xlsx"))
    plot = table.pivot(columns="Ticker", index="Date", values="Price").plot()
    output = io.BytesIO()
    plot.get_figure().savefig(output, format="png")
    return Response(output.getvalue(), mimetype="image/png")
