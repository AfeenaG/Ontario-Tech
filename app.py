from flask import Flask, render_template
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

# Function to fetch data from SQLite
def get_traffic_data():
    db_path = os.path.join(os.path.dirname(__file__), "TrafficCollision.db")

    if not os.path.exists(db_path):
        # Return an error DataFrame if DB is missing
        return pd.DataFrame([["Database not found", db_path]], columns=["Message", "Details"])

    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM Traffic_Collisions LIMIT 10;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        # Return error details if query fails
        return pd.DataFrame([["Query failed", str(e)]], columns=["Message", "Details"])


# Home page route
@app.route("/")
def home():
    df = get_traffic_data()
    return render_template("index.html", table=df.to_html(classes="table table-striped", index=False))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
