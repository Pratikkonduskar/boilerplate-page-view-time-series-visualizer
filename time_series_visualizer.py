
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Import data and set date as the index
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    index_col="date",
    parse_dates=True
)

# Clean the data by filtering out the top and bottom 2.5%
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Use a copy of the data
    df_line = df.copy()

    # Create the line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df_line.index, df_line["value"], color="red")

    # Set the title and axis labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save and return the figure
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Use a copy of the data
    df_bar = df.copy()

    # Extract year and month
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    # Calculate average daily page views for each month and year
    df_bar = (
        df_bar.groupby(["year", "month"])["value"]
        .mean()
        .unstack()
    )

    # Replace month numbers with month names
    df_bar.columns = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    # Create the bar plot
    fig = df_bar.plot(kind="bar", figsize=(10, 6)).figure
    ax = fig.axes[0]

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    # Save and return the figure
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Use a copy of the data
    df_box = df.copy()

    # Prepare year and month columns
    df_box.reset_index(inplace=True)
    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    # Create the two box plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))

    # Year-wise box plot: trend
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=ax1
    )
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Page Views")

    # Month-wise box plot: seasonality
    month_order = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        order=month_order,
        ax=ax2
    )
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel("Page Views")

    # Save and return the figure
    fig.savefig("box_plot.png")
    return fig
