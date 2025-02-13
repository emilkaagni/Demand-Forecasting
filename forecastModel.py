from prophet import Prophet
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("dataset/fashion_demand_forecasting_dataset.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year

# Function to predict future sales for a selected product
def predict_future_product_sales(df, selected_product):
    # Filter data for the selected product
    product_df = df[df['Category'] == selected_product]

    if product_df.empty:
        print(f"No data available for {selected_product}.")
        return None

    # Group sales data by date
    sales_data = product_df.groupby("Date")["Units_Sold"].sum().reset_index()
    sales_data = sales_data.rename(columns={"Date": "ds", "Units_Sold": "y"})  # Prophet requires "ds" and "y"

    # Train Prophet model
    model = Prophet()
    model.fit(sales_data)

    # Create future dates (next 90 days)
    future = model.make_future_dataframe(periods=90)  # Forecast next 90 days
    forecast = model.predict(future)

    return forecast

# Get unique product categories
product_categories = df["Category"].unique()
print("Available Products:", product_categories)

# Let the user select a product
selected_product = input("Enter the product category for forecasting: ")

# Ensure valid product selection
if selected_product not in product_categories:
    print(f"Invalid product. Please choose from {product_categories}")
else:
    # Predict future sales for the selected product
    forecast_product = predict_future_product_sales(df, selected_product)

    if forecast_product is not None:
        # Plot future sales trend for the selected product
        fig_forecast_product = px.line(forecast_product, x="ds", y="yhat",
                                       title=f"Forecasted Sales for {selected_product} (Next 90 Days)",
                                       labels={"ds": "Date", "yhat": "Predicted Units Sold"},
                                       color_discrete_sequence=["#FF9900"])
        fig_forecast_product.show()
