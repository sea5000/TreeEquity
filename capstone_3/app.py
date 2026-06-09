import json
from flask import Flask, render_template, jsonify, request
from sql.db_connection import (
    query_all_cities,
    query_top10_tree_pct,
    query_equity_distribution,
    query_countries,
    query_city_detail,
    query_filtered_cities,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("dashboard1.html")


@app.route("/dashboard1")
def dashboard1():
    countries = query_countries()
    return render_template("dashboard1.html", countries=countries)


@app.route("/dashboard2")
def dashboard2():
    countries = query_countries()
    return render_template("dashboard2.html", countries=countries)


@app.route("/api/cities")
def api_cities():
    cities = query_all_cities()
    return jsonify(cities)


@app.route("/api/top10")
def api_top10():
    data = query_top10_tree_pct()
    return jsonify(data)


@app.route("/api/equity-distribution")
def api_equity_distribution():
    data = query_equity_distribution()
    return jsonify(data)


@app.route("/api/countries")
def api_countries():
    data = query_countries()
    return jsonify(data)


@app.route("/api/city-detail")
def api_city_detail():
    name = request.args.get("name", "")
    data = query_city_detail(name)
    return jsonify(data)


@app.route("/api/filtered-cities")
def api_filtered_cities():
    country = request.args.get("country", None)
    min_pop = request.args.get("min_pop", 0, type=int)
    max_pop = request.args.get("max_pop", 10000000, type=int)
    equity_raw = request.args.get("equity", None)
    equity_categories = (
        equity_raw.split(",") if equity_raw else ["Excellent", "Good", "Needs Improvement"]
    )
    data = query_filtered_cities(
        country=country,
        min_pop=min_pop,
        max_pop=max_pop,
        equity_categories=equity_categories,
    )
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
