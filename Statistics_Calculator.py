# STATISTICS CALCULATOR
# Each numbered section below matches an option on the calculator menu.
# Read the comments above each function to see what that section calculates.
#
# QUICK GUIDE:
# Population standard deviation known -> Z
# Only sample standard deviation known -> T
# Percentage/proportion question -> Proportion options
# Finding how many observations are needed -> Required sample size options


import math
import statistics

try:
    from scipy import stats
except ImportError:
    stats = None


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.")


def get_confidence_level():
    while True:
        confidence = get_float("Confidence level (90, 95, or 99): ")
        if confidence in (90, 95, 99):
            return confidence / 100
        print("Please enter 90, 95, or 99.")


def get_z_critical(confidence):
    z_values = {
        0.90: 1.645,
        0.95: 1.960,
        0.99: 2.576
    }
    return z_values[confidence]


# OPTION 1 - Descriptive statistics
# Calculates mean, median, sample variance, and sample standard deviation.
# Use when the problem gives a list of data values.
def descriptive_statistics():
    print("\nEnter numbers separated by spaces.")
    data = list(map(float, input("Data: ").split()))

    if len(data) < 2:
        print("Please enter at least two values.")
        return

    mean = statistics.mean(data)
    median = statistics.median(data)
    sample_variance = statistics.variance(data)
    sample_std = statistics.stdev(data)

    print("\nResults")
    print(f"Mean: {mean:.4f}")
    print(f"Median: {median:.4f}")
    print(f"Sample variance: {sample_variance:.4f}")
    print(f"Sample standard deviation: {sample_std:.4f}")


# OPTION 2 - Confidence interval for a mean using Z
# Use when the POPULATION standard deviation is known.
# Calculates standard error, margin of error, and the confidence interval.
def confidence_interval_mean_z():
    print("\nConfidence Interval for a Mean - Population Standard Deviation Known")
    mean = get_float("Sample mean: ")
    population_std = get_float("Population standard deviation: ")
    n = get_int("Sample size: ")
    confidence = get_confidence_level()

    z = get_z_critical(confidence)
    standard_error = population_std / math.sqrt(n)
    margin = z * standard_error
    lower = mean - margin
    upper = mean + margin

    print("\nWork")
    print(f"z critical value = {z:.3f}")
    print(f"Standard error = {population_std} / sqrt({n}) = {standard_error:.4f}")
    print(f"Margin of error = {z:.3f} x {standard_error:.4f} = {margin:.4f}")
    print(f"Confidence interval = ({mean:.4f} - {margin:.4f}, {mean:.4f} + {margin:.4f})")
    print(f"Answer: ({lower:.4f}, {upper:.4f})")


# OPTION 3 - Confidence interval for a mean using T
# Use when only the SAMPLE standard deviation is known.
# Uses degrees of freedom (n - 1) and the t-distribution.
def confidence_interval_mean_t():
    print("\nConfidence Interval for a Mean - Sample Standard Deviation")
    if stats is None:
        print("This option requires scipy. Install it with: pip install scipy")
        return

    mean = get_float("Sample mean: ")
    sample_std = get_float("Sample standard deviation: ")
    n = get_int("Sample size: ")
    confidence = get_confidence_level()

    df = n - 1
    alpha = 1 - confidence
    t_critical = stats.t.ppf(1 - alpha / 2, df)
    standard_error = sample_std / math.sqrt(n)
    margin = t_critical * standard_error
    lower = mean - margin
    upper = mean + margin

    print("\nWork")
    print(f"Degrees of freedom = {n} - 1 = {df}")
    print(f"t critical value = {t_critical:.4f}")
    print(f"Standard error = {sample_std} / sqrt({n}) = {standard_error:.4f}")
    print(f"Margin of error = {t_critical:.4f} x {standard_error:.4f} = {margin:.4f}")
    print(f"Answer: ({lower:.4f}, {upper:.4f})")


# OPTION 4 - Confidence interval for a proportion
# Use for percentages or proportions, such as voters who favor something.
# Calculates p-hat, margin of error, and the confidence interval.
def confidence_interval_proportion():
    print("\nConfidence Interval for a Proportion")
    successes = get_int("Number of successes: ")
    n = get_int("Sample size: ")
    confidence = get_confidence_level()

    p_hat = successes / n
    z = get_z_critical(confidence)
    standard_error = math.sqrt((p_hat * (1 - p_hat)) / n)
    margin = z * standard_error
    lower = p_hat - margin
    upper = p_hat + margin

    print("\nWork")
    print(f"Sample proportion = {successes} / {n} = {p_hat:.4f}")
    print(f"z critical value = {z:.3f}")
    print(f"Standard error = {standard_error:.4f}")
    print(f"Margin of error = {margin:.4f}")
    print(f"Answer: [{lower:.4f}, {upper:.4f}]")


# OPTION 5 - Margin of error for a mean
# Calculates only the margin of error for a population mean.
# Uses Z for a known population SD and T for a sample SD.
def margin_error_mean():
    print("\nMargin of Error for a Mean")
    std_type = input("Do you know the population standard deviation? (y/n): ").strip().lower()
    std = get_float("Standard deviation: ")
    n = get_int("Sample size: ")
    confidence = get_confidence_level()

    if std_type == "y":
        critical = get_z_critical(confidence)
        label = "z"
    else:
        if stats is None:
            print("This option requires scipy. Install it with: pip install scipy")
            return
        df = n - 1
        alpha = 1 - confidence
        critical = stats.t.ppf(1 - alpha / 2, df)
        label = "t"

    standard_error = std / math.sqrt(n)
    margin = critical * standard_error

    print("\nWork")
    print(f"{label} critical value = {critical:.4f}")
    print(f"Standard error = {standard_error:.4f}")
    print(f"Margin of error = {margin:.4f}")


# OPTION 6 - Margin of error for a proportion
# Calculates the margin of error for a percentage or proportion.
def margin_error_proportion():
    print("\nMargin of Error for a Proportion")
    successes = get_int("Number of successes: ")
    n = get_int("Sample size: ")
    confidence = get_confidence_level()

    p_hat = successes / n
    z = get_z_critical(confidence)
    margin = z * math.sqrt((p_hat * (1 - p_hat)) / n)

    print("\nWork")
    print(f"Sample proportion = {p_hat:.4f}")
    print(f"z critical value = {z:.3f}")
    print(f"Margin of error = {margin:.4f}")


# OPTION 7 - Required sample size for a mean
# Finds how large a sample is needed for a desired margin of error.
def sample_size_mean():
    print("\nRequired Sample Size for a Mean")
    std = get_float("Estimated standard deviation: ")
    margin = get_float("Desired margin of error: ")
    confidence = get_confidence_level()

    z = get_z_critical(confidence)
    n = (z * std / margin) ** 2

    print("\nWork")
    print(f"Preliminary sample size = ({z:.3f} x {std} / {margin})^2 = {n:.4f}")
    print(f"Required sample size, rounded up = {math.ceil(n)}")


# OPTION 8 - Required sample size for a proportion
# Finds the required sample size for a percentage or proportion.
# If there is no previous estimate, p = 0.50 is used.
def sample_size_proportion():
    print("\nRequired Sample Size for a Proportion")
    has_estimate = input("Do you have a previous estimate for the proportion? (y/n): ").strip().lower()

    if has_estimate == "y":
        p = get_float("Previous proportion estimate as a decimal, for example 0.36: ")
    else:
        p = 0.50
        print("No previous estimate given, so p = 0.50 will be used.")

    margin = get_float("Desired margin of error as a decimal, for example 0.01: ")
    confidence = get_confidence_level()

    z = get_z_critical(confidence)
    n = (z ** 2 * p * (1 - p)) / (margin ** 2)

    print("\nWork")
    print(f"z critical value = {z:.3f}")
    print(f"Estimated proportion = {p:.4f}")
    print(f"Calculated sample size = {n:.4f}")
    print(f"Required sample size, rounded up = {math.ceil(n)}")


# OPTION 9 - Z hypothesis test for a mean
# Tests a claim about a population mean when the population SD is known.
# Calculates the Z statistic and p-value.
def z_test_mean():
    print("\nOne-Sample Z Test for a Mean")
    if stats is None:
        print("This option requires scipy. Install it with: pip install scipy")
        return

    sample_mean = get_float("Sample mean: ")
    population_mean = get_float("Hypothesized population mean: ")
    population_std = get_float("Population standard deviation: ")
    n = get_int("Sample size: ")

    z = (sample_mean - population_mean) / (population_std / math.sqrt(n))

    print("Test type:")
    print("1. Two-tailed")
    print("2. Left-tailed")
    print("3. Right-tailed")
    test_type = input("Choice: ").strip()

    if test_type == "1":
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif test_type == "2":
        p_value = stats.norm.cdf(z)
    elif test_type == "3":
        p_value = 1 - stats.norm.cdf(z)
    else:
        print("Invalid test type.")
        return

    print(f"\nz statistic = {z:.4f}")
    print(f"p-value = {p_value:.6f}")


# OPTION 10 - T hypothesis test for a mean
# Tests a claim about a population mean when only the sample SD is known.
# Calculates the T statistic, degrees of freedom, and p-value.
def t_test_mean():
    print("\nOne-Sample T Test for a Mean")
    if stats is None:
        print("This option requires scipy. Install it with: pip install scipy")
        return

    sample_mean = get_float("Sample mean: ")
    population_mean = get_float("Hypothesized population mean: ")
    sample_std = get_float("Sample standard deviation: ")
    n = get_int("Sample size: ")

    df = n - 1
    t_stat = (sample_mean - population_mean) / (sample_std / math.sqrt(n))

    print("Test type:")
    print("1. Two-tailed")
    print("2. Left-tailed")
    print("3. Right-tailed")
    test_type = input("Choice: ").strip()

    if test_type == "1":
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
    elif test_type == "2":
        p_value = stats.t.cdf(t_stat, df)
    elif test_type == "3":
        p_value = 1 - stats.t.cdf(t_stat, df)
    else:
        print("Invalid test type.")
        return

    print(f"\nt statistic = {t_stat:.4f}")
    print(f"Degrees of freedom = {df}")
    print(f"p-value = {p_value:.6f}")


# OPTION 11 - Hypothesis test for a proportion
# Tests a claim about a population percentage or proportion.
# Calculates p-hat, the Z statistic, and the p-value.
def proportion_test():
    print("\nOne-Sample Proportion Z Test")
    if stats is None:
        print("This option requires scipy. Install it with: pip install scipy")
        return

    successes = get_int("Number of successes: ")
    n = get_int("Sample size: ")
    p0 = get_float("Hypothesized population proportion as a decimal: ")

    p_hat = successes / n
    standard_error = math.sqrt(p0 * (1 - p0) / n)
    z = (p_hat - p0) / standard_error

    print("Test type:")
    print("1. Two-tailed")
    print("2. Left-tailed")
    print("3. Right-tailed")
    test_type = input("Choice: ").strip()

    if test_type == "1":
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif test_type == "2":
        p_value = stats.norm.cdf(z)
    elif test_type == "3":
        p_value = 1 - stats.norm.cdf(z)
    else:
        print("Invalid test type.")
        return

    print(f"\nSample proportion = {p_hat:.4f}")
    print(f"z statistic = {z:.4f}")
    print(f"p-value = {p_value:.6f}")


def show_menu():
    print("\n" + "=" * 55)
    print("STATISTICS CALCULATOR")
    print("=" * 55)
    print("1. Mean, median, variance, and standard deviation")
    print("2. Confidence interval for a mean - population SD known")
    print("3. Confidence interval for a mean - sample SD / t-distribution")
    print("4. Confidence interval for a proportion")
    print("5. Margin of error for a mean")
    print("6. Margin of error for a proportion")
    print("7. Required sample size for a mean")
    print("8. Required sample size for a proportion")
    print("9. Z hypothesis test for a mean")
    print("10. T hypothesis test for a mean")
    print("11. Proportion hypothesis test")
    print("0. Exit")


def main():
    while True:
        show_menu()
        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            descriptive_statistics()
        elif choice == "2":
            confidence_interval_mean_z()
        elif choice == "3":
            confidence_interval_mean_t()
        elif choice == "4":
            confidence_interval_proportion()
        elif choice == "5":
            margin_error_mean()
        elif choice == "6":
            margin_error_proportion()
        elif choice == "7":
            sample_size_mean()
        elif choice == "8":
            sample_size_proportion()
        elif choice == "9":
            z_test_mean()
        elif choice == "10":
            t_test_mean()
        elif choice == "11":
            proportion_test()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please select an option from the menu.")


if __name__ == "__main__":
    main()
