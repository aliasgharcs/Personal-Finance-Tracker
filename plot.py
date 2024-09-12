import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_transaction(df, timeframe):
    try:
        if timeframe.lower() == "d":
            # Daily plotting logic
            df.set_index("Date", inplace=True)
            all_year = pd.date_range(start=df.index.min(), end=df.index.max(), freq="D")
            income_df = df[df["Category"] == "Income"].resample("D").sum().reindex(all_year, fill_value=0)
            expense_df = df[df["Category"] == "Expense"].resample("D").sum().reindex(all_year, fill_value=0)

        elif timeframe.lower() == "m":
            # Monthly plotting logic
            df.set_index("Date", inplace=True)
            all_year = pd.date_range(start=df.index.min(), end=df.index.max(), freq="M")
            income_df = df[df["Category"] == "Income"].resample("M").sum().reindex(all_year, fill_value=0)
            expense_df = df[df["Category"] == "Expense"].resample("M").sum().reindex(all_year, fill_value=0)

        elif timeframe.lower() == "y":
            # Yearly plotting logic
            df.set_index("Date", inplace=True)
            all_year = pd.date_range(start=df.index.min(), end=df.index.max(), freq="Y")
            income_df = df[df["Category"] == "Income"].resample("Y").sum().reindex(all_year, fill_value=0)
            expense_df = df[df["Category"] == "Expense"].resample("Y").sum().reindex(all_year, fill_value=0)

        # Plotting code (same as before)
        index = np.arange(len(all_year))
        bar_width = 0.4
        plt.figure(figsize=(12, 6))
        plt.bar(index - bar_width / 2, income_df["Amount"], width=bar_width, label="Income", color="g")
        plt.bar(index + bar_width / 2, expense_df["Amount"], width=bar_width, label="Expense", color="r")
        plt.xticks(index, [date.strftime('%Y-%m-%d') for date in all_year], rotation=45)
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title(f"Income and Expense ({timeframe})")
        plt.legend()
        plt.tight_layout()

        plot_filename = 'plot.png'
        plt.savefig(f'static/{plot_filename}')
        plt.close()

        return plot_filename

    except ValueError:
        return None
