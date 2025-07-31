from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from datetime import datetime
import matplotlib.dates as mdates

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    start_date = request.form.get("start_date", "2025-01-01")
    end_date = request.form.get("end_date", "2025-01-10")

    try:
        dates = pd.date_range(start=start_date, end=end_date)
        num_days = (dates[-1] - dates[0]).days + 1  # Inclusive
    except Exception as e:
        return render_template("index.html", image=None, error=str(e),
                               start_date=start_date, end_date=end_date, num_days=None)

    if len(dates) == 0:
        return render_template("index.html", image=None, error="Invalid date range",
                               start_date=start_date, end_date=end_date, num_days=None)

    # Simulate data
    np.random.seed(42)
    sales = np.random.uniform(1000, 5000, size=len(dates))
    profit = np.random.uniform(100, 1000, size=len(dates))

    df = pd.DataFrame({
        "Sales": sales,
        "Profit": profit
    }, index=dates)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df["Sales"], label="Sales", marker='o')
    ax.plot(df.index, df["Profit"], label="Profit", marker='s')

    # Averages
    sales_avg = df["Sales"].mean()
    profit_avg = df["Profit"].mean()
    ax.axhline(sales_avg, color='blue', linestyle='--', label=f"Avg Sales (${sales_avg:.2f})")
    ax.axhline(profit_avg, color='orange', linestyle='--', label=f"Avg Profit (${profit_avg:.2f})")

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(len(df)//10, 1)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(rotation=45)

    # Labels and layout
    ax.set_title("Sales and Profit Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render_template("index.html", image=image_base64, start_date=start_date,
                           end_date=end_date, error=None, num_days=num_days)

# This must be outside the function
if __name__ == '__main__':
    app.run(debug=True)
