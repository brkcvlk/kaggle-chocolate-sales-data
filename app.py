from dash import Dash,html,dash_table,dcc,Output,Input,callback
import pandas as pd
import plotly.express as px

df = pd.read_csv("chocolate-sales.csv")

app = Dash()



countries = df['Country'].value_counts()
c_table = {
    'Country': list(countries.index),
    'Number of Sales': list(countries),
}
index = [1,2,3,4,5,6]
table = pd.DataFrame(c_table, index=index)
fig = px.pie(names=df[df['Country'].duplicated()==False]['Country'],values=df['Country'].value_counts())
show_total = [float(e[1:]) for e in df["Amount"].str.replace('[A-Za-z]', '').str.replace(',', '.')]
date_chart = px.histogram(df,x='Date',y=show_total, histfunc='sum')
app.layout = [
    html.Div([
        html.H1("Chocolate Sales",style={'display':'flex','justifyContent':'center'}),
        html.Div([
            html.Div([
                html.Div([
                    html.H2(f'{df.size}',style={'marginLeft':20}),
                    html.P('Data collected')
                ],style={'marginRight':50}),
                html.Div([
                    html.H2(f'${int(sum(show_total))}',style={'marginLeft':40}),
                    html.P('Total revenue from the sales')
                ],style={'marginRight':50}),
                html.Div([
                    html.H2(f'{df[df['Product'].duplicated()==False]['Product'].count()}',style={'marginLeft':80}),
                    html.P('Number of chocolate products')
                ],style={'marginRight':50}),
                html.Div([
                    html.H2(f'{sum(df['Boxes Shipped'])}',style={'marginLeft':130}),
                    html.P('Number of chocolate boxes shipped in the order')
                ])
            ],style={'display':'flex','justifyContent':'center'})
        ],style={'display':'flex','justifyContent':'center'}),
        html.Div([
            html.Div([
                dcc.RadioItems(options=['Amount', 'Boxes Shipped'],className="data-radio",id="sales-person-radio", value='Boxes Shipped'),
                dash_table.DataTable(data=df.to_dict('records'),page_size=10),
            ],style={'width':750,'marginTop':20}),
            html.Div([
                dcc.Graph(figure={}, id="sales-person-chart")
            ],style={'width':750,'marginTop':10})
        ],style={'display': 'grid','gridTemplateColumns': 'auto auto auto','marginLeft':10}),
        html.Div([
            html.H2('Number of Sales by Country', style={'marginLeft':30}),
            html.Div([
                    html.Div([
                        dcc.Graph(figure=fig, id='pie-for-countries')
                    ],style={'width':700}),
                    html.Div([
                        dash_table.DataTable(data=table.to_dict('records'), id='countries-table')
                    ],style={'width':700,'marginTop':100})
                ],style={'display': 'grid','gridTemplateColumns': 'auto auto auto','marginLeft':10})
        ],style={'marginTop':100}),
        html.Div([
            html.H2('Total Revenues by Date',style={'marginLeft':30}),
            dcc.Graph(figure=date_chart,id='amount-by-date-chart')
        ])
    ])
]

@callback(
    Output(component_id="sales-person-chart", component_property="figure"),
    Input(component_id="sales-person-radio", component_property="value")
)
def update_chart(chosen_input):
    if chosen_input == "Boxes Shipped":
        fig = px.histogram(df, x='Sales Person', y=chosen_input, histfunc='sum')
        return fig
    else:
        fix_amount = [float(e[1:]) for e in df["Amount"].str.replace('[A-Za-z]', '').str.replace(',', '.')]
        fig = px.histogram(df,x='Sales Person', y=fix_amount, histfunc='sum', )
        return fig
    

if __name__ == "__main__":
    app.run(debug=True) 