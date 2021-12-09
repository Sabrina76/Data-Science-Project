# -*- coding: utf-8 -*-

from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        #Talks about the website
        dbc.Row([
            dbc.Col(html.H1("NYC Collisions", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='In NYC, motor vehicle collisions are happening everyday, \
                            To help people get a better idea of how many collisions are happening in NYC, vizualizations were created.\
                                Motor vehicle collision data was taken from NYC Open data to create these visualizations. These dataset used by these \
                                    graphs were first filtered by using pandas, and was created using plotly. This website was created using dash.'
                    , className="mb-5")),
        ]),
        dbc.Row([
             dbc.Col(html.H5(children='Click the explore button up top to view them.'
                    , className="mb-5"))
        ]),
        dbc.Row([
             dbc.Col(html.H5(children='Cick the buttons below to view the original data set and the code used to build the website.'
                    , className="mb-5"))
        ]),

        dbc.Row([
            #Button to original data set
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this website',
                                               className="text-center"),
                                       dbc.Col(dbc.Button("Data", href="https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/data",
                                                                   color="primary"),
                                                                   className="d-grid gap-2 col-6 mx-auto"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=5.5, className="mb-4"),
            #Button to github page
            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this website',
                                               className="text-center"),
                                       dbc.Button("GitHub",
                                                  href="https://github.com/Sabrina76/Data-Science-Project",
                                                  color="primary",
                                                  className="d-grid gap-2 col-6 mx-auto"),
                                       ],
                             body=True, color="dark", outline=True)
                    , width=5.5, className="mb-4"),

        ], align="center", className="mb-5"),
    ])

])
