import matplotlib
matplotlib.use('Agg')   # backend-safe rendering

import pandas as pd
import matplotlib.pyplot as plt
import os


def generate_charts(records):

    # SAFETY CHECK
    if not records:
        return None

    df = pd.DataFrame(records)
    charts = {}

    os.makedirs("static/charts", exist_ok=True)

    # ================================
    # 1️⃣ CRIME TYPE PIE CHART
    # ================================
    if "crime" in df and df["crime"].notna().any():
        crime_counts = df["crime"].value_counts()

        plt.figure(figsize=(6, 6))
        crime_counts.plot.pie(
            autopct='%1.1f%%',
            startangle=90
        )
        plt.title("Crime Type Distribution")
        plt.ylabel("")   # remove extra ylabel
        plt.tight_layout()

        pie_path = "static/charts/crime_pie.png"
        plt.savefig(pie_path)
        plt.close()

        charts["pie"] = pie_path

    # ================================
    # 2️⃣ STATE-WISE BAR CHART
    # ================================
    if "state" in df and df["state"].notna().any():
        state_counts = df["state"].value_counts()

        plt.figure(figsize=(8, 5))
        state_counts.plot(kind="bar")

        plt.title("State-wise Crime Count")
        plt.xlabel("State")
        plt.ylabel("Count")

        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        bar_path = "static/charts/state_bar.png"
        plt.savefig(bar_path)
        plt.close()

        charts["state"] = bar_path

    # ================================
    # 3️⃣ REPEAT PHONE NUMBERS BAR
    # ================================
    if "phone" in df and df["phone"].notna().any():
        repeat = df["phone"].value_counts()
        repeat = repeat[repeat > 1]

        if not repeat.empty:
            plt.figure(figsize=(8, 5))
            repeat.plot(kind="bar", color="red")

            plt.title("Repeat Offenders (Phone Numbers)")
            plt.xlabel("Phone Number")
            plt.ylabel("Count")

            plt.xticks(rotation=45, ha="right")

            # 🔹 show count on bars
            for index, value in enumerate(repeat.values):
                plt.text(index, value, str(value),
                         ha='center', va='bottom')

            plt.tight_layout()

            repeat_path = "static/charts/repeat_phone.png"
            plt.savefig(repeat_path)
            plt.close()

            charts["repeat"] = repeat_path

    return charts
