# Define tax slabs as a list of tuples (lower_bound, upper_bound, rate)
slabs = [
    (0, 400_000, 0.00),
    (400_000, 800_000, 0.05),
    (800_000, 1_200_000, 0.10),
    (1_200_000, 1_600_000, 0.15),
    (1_600_000, 2_000_000, 0.20),
    (2_000_000, 2_400_000, 0.25),
    (2_400_000, float("inf"), 0.30),
]
threshold = 1_200_000  # Income above this triggers taxation of lower slabs


def calculate_tax(income):
    if income <= threshold:
        return 0
    tax = 0.0
    for lower, upper, rate in slabs:
        if upper <= threshold:
            # Apply full tax for slabs below threshold
            tax += (upper - lower) * rate
        else:
            # Apply tax only on the portion exceeding the threshold
            slab_lower = max(lower, threshold)
            slab_upper = upper
            taxable_amount = max(0, min(income, slab_upper) - slab_lower)
            tax += taxable_amount * rate
    return tax


def main():
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    incomes = range(int(11.5e5), int(13e5), int(1e3))
    take_homes = [income - calculate_tax(income) for income in incomes]

    max_take_home = 0
    take_home_colors = []
    red_income_ranges = []
    current_range_start = None

    for income, take_home in zip(incomes, take_homes):
        if take_home < max_take_home:
            take_home_colors.append("red")
            if current_range_start is None:
                current_range_start = income
        else:
            take_home_colors.append("blue")
            max_take_home = take_home
            if current_range_start is not None:
                red_income_ranges.append((current_range_start, income))
                current_range_start = None

    if current_range_start is not None:
        red_income_ranges.append((current_range_start, incomes[-1]))

    fig, ax = plt.subplots(figsize=(10, 6))

    for start, end in red_income_ranges:
        ax.axvspan(
            start / 1e5,
            end / 1e5,
            color="red",
            alpha=0.3,
            label=f"Decreasing Take Home: {start/1e5}-{end/1e5} lakhs",
        )

    scatter = ax.scatter(
        [income / 1e5 for income in incomes],
        [take_home / 1e5 for take_home in take_homes],
        c=take_home_colors,
        label="Take Home",
        edgecolor="k",
        s=10,
    )

    ax.set_xlabel("Taxable Income (in lakhs)", fontsize=12)
    ax.set_ylabel("Take Home (in lakhs)", fontsize=12)
    ax.set_title("Taxable Income vs Take Home", fontsize=14, fontweight="bold")
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.legend(loc="upper left", fontsize=10)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:.1f}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:.1f}"))

    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
