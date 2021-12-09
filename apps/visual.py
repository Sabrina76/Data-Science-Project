# -*- coding: utf-8 -*-

#import plot.graph_objects as go
import pandas as pd
import numpy as np

import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

from app import app

year = pd.read_csv("year.csv")
borough = pd.read_csv("borough.csv")
borough_total = borough.groupby(['BOROUGH'], as_index= False).sum()
borough_total = borough_total[['BOROUGH', 'COLLISIONS']]
reason = pd.read_csv("reason.csv")
reason = reason.head(10)
reason = reason.reset_index()
reason_borough = pd.read_csv("reason_borough.csv")
zip_borough = pd.read_csv("zip_borough.csv")


layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children="Collisions Visualizations & Analysis", className="header-title"), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Analyze the behavior between number of \
                            colllisions and the number of caualties and injured \
                                between 2012 and 2021'
                            ), className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(
                html.H3(
                    children='Total Figures From 2012 to 2021',
                                 className="text-center text-light bg-dark"), body=True, color="dark"
                ), className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Collision Total in Each Borough', className="text-center"),
                         width=4, className="mt-4"),
            dbc.Col(html.H5(children='Total Collisions, Injured and Casualties', className="text-center"), width=8, className="mt-4"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                figure = {
                    "data": [
                        {
                            "x": borough_total["BOROUGH"],
                            "y": borough_total["COLLISIONS"],
                            "type": "bar", "name":"Borough_Collisions", 'marker' : { "color" : 'Aquamarine'},
                        }
                    ]
                },
            )),
            dbc.Col(dcc.Graph(
                figure={
                    "data": [
                        {
                            "x": year["YEAR"],
                            "y": year["KILLED"],
                            "type": "line", "name":"Killed", 'line':dict(color='mediumpurple'),
                        },
                        {
                            "x": year["YEAR"],
                            "y": year["INJURED"],
                            "type": "line", "name":"Injured", 'line':dict(color='red'),
                        },
                        {
                            "x": year["YEAR"],
                            "y": year["COLLISIONS"],
                            "type": "bar", "name":"Collisions", 'marker' : { "color" : 'cyan'},
                        },
                    ],
                },
            ), width = 8)
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Top 10 Reason for collision', className="text-center"), className="mt-4"),
        ]),
        dbc.Row([
            dcc.Graph(
                figure = px.pie(reason, values='COLLISIONS', names = 'REASON')
            )
        ]),
        dbc.Row([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Analysis", className="total-analysis"),
                        html.P(
                            "Comparing the last two years against the previous years, we can see that there's a huge drop in the number of collisions.\
                                This is likely due to the cause of COVID 19. In 2012, the number of collisions is low as well due to only having data recorded\
                                    starting from July. To the left is a bar graph of the total amount of collisions in each borough from 2012 to 2021. The highest amount\
                                        collisions happen in Brooklyn, followed by Queens, Manhattan, Bronx, and finally Staten Island. Brooklyn has the highest amount of \
                                            collisions in total at approximately 401k collisions followed by Queens at approximately 341k, Manhattan at approximately 293k, \
                                                Bronx at approximately 185k, and finally Staten Island at approximately 53k.On the bottom is a pie chart of the top 10 reasons \
                                                    for collisions. Around 47% of the top reasons are unspecified. The next reason was 'driver inattention/distraction' which covers \
                                                        around 22% of top reasons. One way this can be prevented is to stop texting while driving. Reasons 3-9 covers around 29% of top reasons. \
                                                            These reasons for collisions can be prevented by paying attention to surroundings and leaving earlier to prevent drivers from rushing. \
                                                                Reason 10 covers around 2% of top reasons. This can be prevented by having someone else drive you, or by pulling to the side and taking a \
                                                                    quick rest to get rid of fatigue/drowsiness before continuing on."

                        )
                    ]
                ), color = "lavender", inverse=False
            )
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        dcc.Dropdown(
            id="borough-filter",
            options=[
                {"label": Borough, "value": Borough}
                for Borough in np.sort(borough.BOROUGH.unique())
            ],
            value="Bronx",
            clearable=False,
            className="dropdown",
        ),
        dbc.Row([
            dbc.Col(dbc.Card(
                html.H3(
                    children='Borough Figures From 2012 to 2021',
                                 className="text-center text-light bg-dark"), body=True, color="dark"
                ), className="mt-4 mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(id='Zip'),width=4, className="mt-4"),
            dbc.Col(html.H5(id='Borough-Total', className="text-center"), width=8, className="mt-4"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Zip-chart'), width = 4),
            dbc.Col(dcc.Graph(id='Borough-chart'), width = 8)
        ]),
        dbc.Row([
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(id='Borough-Title'),
                        html.P(id='Borough-Analysis')
                    ]
                ), color = "LightSkyBlue", inverse=False
            )
        ]),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col(html.H5(id='Zip-pie', className="text-center"), width=12, className="mt-4"),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='Borough-pie'))
        ]),
    ])
])






@app.callback(
    [
     Output("Borough-pie", "figure"),
     Output("Borough-chart", "figure"),
     Output("Zip-chart", "figure"),
    ],
    [
        Input("borough-filter", "value"),
    ],
)
def update_chart(Borough):
    df4 = reason_borough[reason_borough['BOROUGH'] == Borough]
    df4 = df4.head(10)
    df4 = df4.reset_index()
    Borough_pie_figure = go.Figure(
        data=[
            go.Pie(
                labels=df4['REASON'],
                values=df4['COLLISIONS']
            )
        ]
    )
    
    filtered_data = borough[borough['BOROUGH'] == Borough]
    Borough_chart_figure = {
        "data": [
            {
                "x": filtered_data["YEAR"],
                "y": filtered_data["COLLISIONS"],
                 "type": "bar", "name":"Collisions", 'marker' : { "color" : 'PowderBlue'},
                "hovertemplate": "%{y:}<extra></extra>",
            },
            {
                "x": filtered_data["YEAR"],
                "y": filtered_data["INJURED"],
                "type": "line", "name":"Injured", 'line':dict(color='black'),
                "hovertemplate": "%{y:}<extra></extra>",
            },
            {
                "x": filtered_data["YEAR"],
                "y": filtered_data["KILLED"],
                "type": "line", "name":"Killed", 'line':dict(color='blue'),
                "hovertemplate": "%{y:}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": Borough,
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"],
        },
    }
    
    zip_filtered = zip_borough[zip_borough['BOROUGH'] == Borough]
    zip_filtered = zip_filtered.groupby(['ZIP'], as_index= False).sum().sort_values('COLLISIONS', ascending=False).head(15)
    
    
    Zip_chart_figure = go.Figure(go.Bar(
        x = zip_filtered['COLLISIONS'],
        y = zip_filtered['ZIP'],
        orientation = 'h',
        marker=dict(
        color='Turquoise',
        line=dict(color='Turquoise', width=3)
    )
    ))
    Zip_chart_figure.update_layout(
        height = 700,
    )

    return Borough_pie_figure, Borough_chart_figure, Zip_chart_figure 

@app.callback(
    [
     Output('Zip', 'children'),
     Output('Borough-Total', 'children'),
     Output('Zip-pie', 'children'),
     Output('Borough-Title', 'children'),
     Output('Borough-Analysis', 'children'),
    ],
    [
        Input("borough-filter", "value"),
    ],
)
def update_card(Borough):
    if (Borough == 'Bronx'):
        analysis = 'The top reason for collisions in the Bronx is still unspecified. \
            The second top reason for collision is still ‘Driver Inattention/Distraction’.\
                For reasons 3-9, the reasons remain the same, though the ranking may differ. \
                    In the Bronx, the tenth reason for top collision is ‘Traffic Control Disregard’. \
                        This reason can cover many things such as driving into a crowded intersection, \
                            speeding past a red light, turning on stop without checking for other vehicles, etc... \
                                One way to prevent that is to not rush while driving. Always check your surroundings and \
                                    don’t rush while driving. For drivers driving in the Bronx, they should be extra careful \
                                        in the area with the zip code 10467 where the most collisions happen. Compared to the \
                                            second highest collision area with zip code 10466, approximately two thousand more collisions happened in 10467.'
    elif(Borough == 'Brooklyn'):
        analysis = 'The percentage and rankings may vary but the top ten reasons for collisions \
            in Brooklyn are the same as the top ten reasons for collisions in general. For drivers \
                driving in Brooklyn, they should be extra careful in the area with the zip code 11207 \
                    where the most collisions happen. Compared to the second highest collision area with \
                        zip code 11236, approximately seven thousand more collisions happened in 11236.'
    elif(Borough == 'Manhattan'):
        analysis = 'The percentage and rankings may vary but the top ten reasons for collisions in \
            Manhattan are the same as the top ten reasons for collisions in general. For drivers driving \
                in Manhattan, they should be extra careful in the areas with the zip code 10019, 10016, \
                    and 10036 where the most collisions happen. These three areas are where most of the \
                        collisions are happening in Manhattan. The total amount of collision difference between \
                            the areas is less than five hundred.'
    elif(Borough == 'Queens'):
        analysis = 'The percentage and rankings may vary but the top ten reasons for collisions in Queens\
            are the same as the top ten reasons for collisions in general. For drivers driving in Queens,\
                they should be extra careful in the area with the zip code 11101 where the most collisions\
                    happen. Compared to the second highest collision area with zip code 11385, approximately \
                        two thousand more collisions happened in 11101.'
    else:
        analysis = 'The percentage and rankings may vary but most of the top ten reasons for collisions \
            in Staten Island are the same as the top ten reasons for collisions in general. The only \
                difference is the new reason ‘Pavement Slippery’. Drivers should be more cautious while \
                    driving in the winter to prevent that from happening. For drivers driving in Staten \
                        Island, they should be extra careful in the area with the zip code 10306 where the \
                            most collisions happen. Compared to the second highest collision area with zip code 10304, \
                                approximately two thousand more collisions happened in 10306.'
    return ['TOP AREA OF COLLISIONS IN '+ Borough], ['TOTAL COLLISIONS, INJURED AND CASUALTIES IN '+ Borough],['Top 10 Reason for collision in '+ Borough],[Borough +" Analysis"], [analysis]
        
    