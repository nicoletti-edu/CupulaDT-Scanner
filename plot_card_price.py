import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a pandas DataFrame
def load_csv(file_path):
    df = pd.read_csv(file_path)
    
    # Convert the 'Timestamp' column to datetime for better plotting and sorting
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Clean the 'Price' column by removing currency symbols and commas, and converting it to a numeric type
    # Using a raw string (r'R\$') to avoid the SyntaxWarning
    df['Price'] = df['Price'].replace({r'R\$': '', ',': '.'}, regex=True)
    
    # Remove rows where 'Price' is non-numeric
    df = df[pd.to_numeric(df['Price'], errors='coerce').notnull()]
    
    # Convert to float
    df['Price'] = df['Price'].astype(float)
    
    return df

# Filter data for a specific card and find the lowest price for each day
def filter_card_data(df, card_name):
    """Filter the DataFrame for a specific card name and get the lowest price for each day."""
    card_data = df[df['Card Name'] == card_name]
    
    # Group by date only (ignore time), and get the minimum price for each day
    card_data['Date'] = card_data['Timestamp'].dt.date
    card_data = card_data.groupby('Date', as_index=False).agg({'Price': 'min'})
    
    return card_data

# Plot the price of a specific card over time
def plot_card_price(card_data, card_name, save=False):
    """Plot the price of a specific card over time and optionally save the plot."""
    if card_data.empty:
        print(f"No data found for card: {card_name}")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(card_data['Date'], card_data['Price'], marker='o', linestyle='-', color='b', label='Price')
    
    plt.title(f'Price Trend for {card_name} (Lowest Price per Day)')
    plt.xlabel('Date')
    plt.ylabel('Price (R$)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    
    if save:
        plt.savefig(f'{card_name}_price_trend.png')
    
    plt.show()

# Main function to load CSV, filter card data, and plot the price
def main():
    file_path = 'price_log.csv'  # Change this to your CSV file path
    df = load_csv(file_path)

    card_name = input("Enter the card name you want to plot: ")
    card_data = filter_card_data(df, card_name)
    
    # Plot the price chart
    plot_card_price(card_data, card_name)

if __name__ == "__main__":
    main()
