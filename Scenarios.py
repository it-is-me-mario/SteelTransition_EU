# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 13:01:59 2024

@author: debor
"""

import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel('data.xlsx')

fig= go.Figure()

fig = go.Figure(data=[
    go.Bar(name='NG-DR', y=[df["Year"], df["Scenario"]], x=df["NG DRI-EAF"], orientation='h', marker_color="#b2b2b2", opacity=0.9),
    go.Bar(name='100% H<sub>2</sub>-DR', y=[df["Year"], df["Scenario"]], x=df["H2 DRI-EAF"], orientation='h', marker_color="#80b918", opacity=0.9),
    go.Bar(name='Charcoal inj', y=[df["Year"], df["Scenario"]], x=df["BF-BOF with charcoal"], orientation='h', marker_color="#f6ae2d", opacity=0.9),
    go.Bar(name='Charcoal inj + CCUS', y=[df["Year"], df["Scenario"]], x=df["BF-BOF with charcoal and CCUS"], orientation='h', marker_color="#f26419", opacity=0.9),
    go.Bar(name='BF-BOF + CCUS', y=[df["Year"], df["Scenario"]], x=df["BF-BOF with CCUS"], orientation='h', marker_color="#00b2ca", opacity=0.9),
    go.Bar(name='H<sub>2</sub> inj', y=[df["Year"], df["Scenario"]], x=df["BF-BOF with H2 injection"], orientation='h', marker_color="#ff4d6d", opacity=0.9),
    go.Bar(name='BF-BOF', y=[df["Year"], df["Scenario"]], x=df["BF-BOF"], orientation='h', marker_color="#0081a7", opacity=0.9),
    go.Bar(name='EAF', y=[df["Year"], df["Scenario"]], x=df["EAF"], orientation='h', marker_pattern_shape="/", marker_color="#dad7cd")
])


fig.update_layout(barmode='stack',
                  legend_traceorder='normal',
                  legend_title='Technology',
                  yaxis_tickangle=0,    
                  xaxis_tickformat=',.0%',
                  template="plotly_white",
                  font_family="Helvetica",
                  font_size=13,    
                  yaxis=dict(categoryorder='total ascending'),
                             
                  )

fig.show(renderer="browser")