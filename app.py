import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/fashion_demand_forecasting_dataset.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year  # Extract year for filtering

# Initialize the app
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

# Layout
app.layout = html.Div(children=[
    html.H1("Fashion Demand Forecasting Dashboard", style={'textAlign': 'center'}),
    
    # Year filter dropdown with 'All Years' option
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': "All Years", 'value': 'all'}] +
                [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
        value='all',
        clearable=False
    ),
    
    dcc.Graph(id='sales-trend', style={'width': '100%', 'height': '400px'}),
    dcc.Graph(id='category-sales', style={'width': '100%', 'height': '400px'}),
    dcc.Graph(id='price-demand', style={'width': '100%', 'height': '400px'}),
    dcc.Graph(id='stock-levels', style={'width': '100%', 'height': '400px'}),
    dcc.Graph(id='revenue-trend', style={'width': '100%', 'height': '400px'}),
])

# Callbacks to update charts based on selected year
@app.callback(
    Output('sales-trend', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_sales_trend(selected_year):
    filtered_df = df if selected_year == 'all' else df[df['Year'] == selected_year]
    fig = px.line(filtered_df.groupby("Date")["Units_Sold"].sum().reset_index(),
                  x="Date", y="Units_Sold", title=f"Sales Trend Over Time ({selected_year if selected_year != 'all' else 'All Years'})",
                  color_discrete_sequence=["#FF5733"])
    return fig

@app.callback(
    Output('category-sales', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_category_sales(selected_year):
    filtered_df = df if selected_year == 'all' else df[df['Year'] == selected_year]
    fig = px.bar(filtered_df.groupby("Category")["Units_Sold"].sum().reset_index(),
                 x="Category", y="Units_Sold", title=f"Sales by Category ({selected_year if selected_year != 'all' else 'All Years'})",
                 color="Category", color_discrete_sequence=px.colors.qualitative.Bold)
    return fig

@app.callback(
    Output('price-demand', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_price_demand(selected_year):
    filtered_df = df if selected_year == 'all' else df[df['Year'] == selected_year]
    fig = px.scatter(filtered_df, x="Price", y="Units_Sold", color="Category",
                     title=f"Price vs Units Sold ({selected_year if selected_year != 'all' else 'All Years'})",
                     color_discrete_sequence=px.colors.qualitative.Dark24)
    return fig

@app.callback(
    Output('stock-levels', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_stock_levels(selected_year):
    filtered_df = df if selected_year == 'all' else df[df['Year'] == selected_year]
    fig = px.line(filtered_df.groupby("Date")["Stock_Levels"].sum().reset_index(),
                  x="Date", y="Stock_Levels", title=f"Stock Levels Over Time ({selected_year if selected_year != 'all' else 'All Years'})",
                  color_discrete_sequence=["#FF5733"])
    return fig

@app.callback(
    Output('revenue-trend', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_revenue_trend(selected_year):
    filtered_df = df if selected_year == 'all' else df[df['Year'] == selected_year]
    fig = px.line(filtered_df.groupby("Date")["Revenue"].sum().reset_index(),
                  x="Date", y="Revenue", title=f"Revenue Trend Over Time ({selected_year if selected_year != 'all' else 'All Years'})",
                  color_discrete_sequence=["#3357FF"])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
