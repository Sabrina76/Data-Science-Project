#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

data = pd.read_csv("Motor_Vehicle_Collisions_-_Crashes.csv", low_memory=False)
data['COLLISIONS'] = 1;
data["DATE"] = pd.to_datetime(data["CRASH DATE"], format="%m/%d/%Y")
data = data.rename(columns={"ZIP CODE": "ZIP", "NUMBER OF PERSONS KILLED": "KILLED", "NUMBER OF PERSONS INJURED": "INJURED", "CONTRIBUTING FACTOR VEHICLE 1": "REASON"})
data = data[data.BOROUGH.notnull()]
data = data[data.ZIP.notnull()]
data['YEAR'] = data['DATE'].dt.year
data = data.replace(
    ['BRONX','BROOKLYN', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'], 
    ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
    )

casualty_collision_df = data[["YEAR", "BOROUGH", "KILLED", "INJURED", "COLLISIONS"]].copy()
year = casualty_collision_df.groupby(['YEAR'], as_index = False).sum()
year.to_csv('year.csv', index=False)

borough = casualty_collision_df.groupby(['BOROUGH', 'YEAR'], as_index = False).sum()
bronx = borough[borough['BOROUGH']== 'Bronx']
borough.to_csv('borough.csv', index=False)

reason_before = data[["BOROUGH", "COLLISIONS", "REASON"]].copy()
reason_before = reason_before[reason_before.REASON.notnull()]

reason = reason_before.groupby(['REASON'], as_index = False).sum()
reason = reason.sort_values('COLLISIONS', ascending=False)
reason.to_csv('reason.csv', index = False)

reason_borough = reason_before.groupby(['REASON', 'BOROUGH'], as_index = False).sum()
reason_borough = reason_borough.sort_values('COLLISIONS', ascending=False)
reason_borough.to_csv('reason_borough.csv', index = False)

zip_borough = data[["BOROUGH", "COLLISIONS", "REASON", "ZIP"]].copy()
zip_borough = zip_borough.groupby(['BOROUGH', 'ZIP', 'REASON'], as_index= False).sum()
zip_borough.to_csv('zip_borough.csv', index = False)