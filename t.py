def hull_moving_average(values, period):
    """
    Calculate the Hull Moving Average (HMA) for the last value of a list of values.

    :param values: List of numerical values.
    :param period: Integer representing the period for the HMA calculation.
    :return: Hull Moving Average (HMA) for the last value in the list.
    """
    from math import sqrt

    # Weighted moving averages
    def wma(values, n):
        return sum((n - i) * values[-(n - i)] for i in range(n)) / ((n * (n + 1)) / 2)

    # Hull Moving Average Calculation
    wma_short = 2 * wma(values, int(period / 2))
    wma_long = wma(values, period)
    diff = wma_short - wma_long

    # HMA Calculation
    hma_period = int(sqrt(period))
    hma = wma(values, hma_period)
    hma += diff

    return hma


# Example usage:
if __name__ == "__main__":
    values = [28, 29, 30, 31, 32]  # Example values
    period = 5  # Example period

    hma_last_value = hull_moving_average(values, period)
    print("Hull Moving Average (HMA) for the last value:", hma_last_value)
