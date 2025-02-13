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
    html.H1("Fashion Demand Forecasting - Pie Chart Dashboard", style={'textAlign': 'center'}),
    
    # Year filter dropdown with 'All Years' option
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': "All Years", 'value': 'all'}] +
                [{'label': str(year), 'value': year} for year in sorted(df['Year'].unique())],
        value='all',
        clearable=False
    ),
    
    dcc.Graph(id='category-pie-chart', style={'width': '100%', 'height': '500px'}),
    dcc.Graph(id='brand-pie-chart', style={'width': '100%', 'height': '500px'}),
])

# Callback to update pie charts based on selected year
@app.callback(
    [Output('category-pie-chart', 'figure'),
     Output('brand-pie-chart', 'figure')],
    [Input('year-dropdown', 'value')]
)
def update_pie_charts(selected_year):
    filtered_df = df if selected_year == 'all' else df[df['Year'] == selected_year]
    
    fig_category_pie = px.pie(filtered_df, names='Category', values='Units_Sold',
                              title=f"Sales Distribution by Category ({selected_year if selected_year != 'all' else 'All Years'})",
                              color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig_brand_pie = px.pie(filtered_df, names='Brand', values='Units_Sold',
                            title=f"Sales Distribution by Brand ({selected_year if selected_year != 'all' else 'All Years'})",
                            color_discrete_sequence=px.colors.qualitative.Set3)
    
    return fig_category_pie, fig_brand_pie

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
