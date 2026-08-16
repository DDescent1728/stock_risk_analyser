import sys
from db import  insert_price , get_price_history, delete_stock, insert_simulation_result
from simulation import compute_log_returns, compute_mu_sigma, run_gbm_simulation, compute_risk_metrics



# Console UI Functions


def main_menu():
    print("\n===== STOCK RISK ANALYZER =====")
    print("1. Add stock price")
    print("2. View price history")
    print("3. Run GBM Monte Carlo simulation")
    print("4. Show risk analysis report")
    print("5. Delete a stock entry")
    print("6. Exit")
    print("===============================")


def add_stock_price_ui():
    print("\n--- Add Stock Price ---")
    symbol = input("Enter stock symbol: ").upper()
    date = input("Enter date (YYYY-MM-DD): ")
    try:
        price = float(input("Enter closing price: "))
    except ValueError:
        print("Invalid price. Please enter a number.")
        return

    # Calling DB function to insert price
    insert_price(symbol, date, price)
    print("Price added successfully.")


def view_history_ui():
    print("\n--- View Stock Price History ---")
    symbol = input("Enter stock symbol: ").upper()

    prices = get_price_history(symbol)
    if not prices:
        print(f"No price history found for {symbol}.")
        return

    print("\nDate\t\tPrice")
    for date, price in prices:
        print(f"{date}\t{price}")


def run_simulation_ui():
    print("\n--- GBM Monte Carlo Simulation ---")
    symbol = input("Enter stock symbol: ").upper()
    try:
        days = int(input("Enter number of future days to simulate: "))
        n_paths = int(input("Enter number of simulation runs: "))
    except ValueError:
        print("Invalid input. Please enter integers.")
        return

    # 1. Fetch historical prices
    prices = get_price_history(symbol)
    if not prices:
        print(f"No price history found for {symbol}. Cannot run simulation.")
        return

    closing_prices = [p for d, p in prices]

    # 2. Compute log returns
    log_returns = compute_log_returns(closing_prices)

    # 3. Compute μ and σ
    mu, sigma = compute_mu_sigma(log_returns)

    # 4. Run GBM simulation
    simulation_results = run_gbm_simulation(closing_prices[-1], mu, sigma, days, n_paths)

    # 5. Store results (optional)
    insert_simulation_result(symbol, simulation_results)

    print(f"Simulation completed for {symbol}.")
    print("Use 'Show risk analysis report' to view expected price, VaR, and worst-case scenario.")


def risk_report_ui():
    print("\n--- Risk Analysis Report ---")
    symbol = input("Enter stock symbol: ").upper()

    # Fetch last simulation results from DB
    simulation_results = get_price_history(symbol) # placeholder, replace with actual function

    if not simulation_results:
        print("No simulation results found. Run a simulation first.")
        return

    metrics = compute_risk_metrics(simulation_results)

    print("\n----- RISK METRICS -----")
    print(f"Expected Price: {metrics['expected_price']:.2f}")
    print(f"Worst Case Price: {metrics['worst_case']:.2f}")
    print(f"95% Value at Risk: {metrics['var_95']:.2f}")
    print("-------------------------")


def delete_price_ui():
    print("\n--- Delete Stock Entry ---")
    symbol = input("Enter stock symbol: ").upper()
    delete_stock(symbol)
    print("Deletion completed.")






# Main Loop


def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            add_stock_price_ui()
        elif choice == '2':
            view_history_ui()
        elif choice == '3':
            run_simulation_ui()
        elif choice == '4':
            risk_report_ui()
        elif choice == '5':
            delete_price_ui()
        elif choice == '6':
            print("Exiting program.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
