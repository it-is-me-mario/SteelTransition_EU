#%% importing dependencies and defining common properties
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

paths = {
    'GHG footprints': {
        "act":"Results/GHG_Footprints_act.csv",
        "com":"Results/GHG_Footprints_com.csv",
        },
    'Steel prices': "Results/Prices.csv",
    'Plots': "Plots"
    }

template = 'seaborn'
font = {'family':'Helvetica','size':14}

routes_renaming = {
    'option1': {
        'Manufacture of basic iron and steel and of ferro-alloys and first products thereof':'BF-BOF',
        'Steel production BF-BOF + CCUS': 'BF-BOF<br>+CCUS',
        'Steel production with charcoal inj to BF':'CHL-inj',
        'Steel production with charcoal inj to BF + CCUS':'CHL-inj<br>+CCUS',    
        'Steel production with H2 inj to BF':'H2-inj',
        'Steel production through NG-DR':'NG-DR',
        'Steel production through 100%H2-DR':'H2-DR',
        'Re-processing of secondary steel into new steel': 'Secondary<br>steel',
        },
    'option2': {
        'Manufacture of basic iron and steel and of ferro-alloys and first products thereof':'Primary<br>steel',
        'Steel production BF-BOF + CCUS': 'BF-BOF+CCUS',
        'Steel production with charcoal inj to BF':'CHL-inj',
        'Steel production with charcoal inj to BF + CCUS':'CHL-inj+CCUS',    
        'Steel production with H2 inj to BF':'H2-inj',
        'Steel production through NG-DR':'NG-DR',
        'Steel production through 100%H2-DR':'H2-DR',
        'Re-processing of secondary steel into new steel': 'Secondary<br>steel',
        },
    }

activities_renaming = {
    'Agriculture': 'Agriculture & Mining',
    'Mining and extraction activities; metals production':'Agriculture & Mining',
    'Electricity production and transmission':'Electricity',
    'Hydrogen production':'Hydrogen',
    'Manufacturing and processing activities': 'Industry',
    'Steel production':'Primary steel',
    'Re-processing of secondary steel into new steel':'Secondary steel',
    'Services and transport activities':'Services',
    'Waste treatment and recycling activities': 'Services',
    }


#%% parse and concat results
import os 
folders = {
    'Results/Prices.csv': "Results/Prices",
    'Results/GHG_Footprints_act.csv': "Results/GHG_Footprints_act",
    'Results/GHG_Footprints_com.csv': "Results/GHG_Footprints_com",
    }

for final_file,folder in folders.items():
    filenames = next(os.walk(folder), (None, None, []))[2]  # [] if no file

    df = pd.DataFrame()
    for filename in filenames:
        dd = pd.read_csv(f"{folder}/{filename}")
        df = pd.concat([df,dd],axis=0)   

    df.to_csv(final_file,index=False)
            
#%% Fig 3. plotting total steel footprints by region in baseline
data = pd.read_csv(paths['GHG footprints']['act'],index_col=[0]).groupby(['Item','To','Scenario','Year','Sensitivity','Unit']).sum().reset_index()

baseline_routes = [
    'Manufacture of basic iron and steel and of ferro-alloys and first products thereof',
    'Re-processing of secondary steel into new steel',
    ]

data = data.query("Item==@baseline_routes & Scenario=='Baseline' & Sensitivity=='Average'")
data['Item'] = data['Item'].map(routes_renaming['option2'])

colors = {
    'Primary<br>steel':'#219ebc',
    'Secondary<br>steel':'#023047',
    }

fig = px.box(data,y='Item',x='Value',color='Item',color_discrete_map=colors,points='all',hover_name='To',orientation='h')

fig.update_layout(
    template=template,
    font=font,
    yaxis=dict(title=''),
    xaxis=dict(title='ton<sub>CO2eq</sub>/ton<sub>steel</sub>',range=[0,5],dtick=0.5), 
    showlegend=False,
    margin=dict(l=10,r=10,b=10,t=50),
    )
fig.write_html(paths['Plots']+"/GHG_PrimarySecondary_Baseline_by_reg.html",auto_open=True)

#%% Fig. 4 . Baseline footprints by route in the EU
all_data = pd.read_csv(paths['GHG footprints']['act']).groupby(['Activity','Item','To','Scenario','Year','Sensitivity','Unit']).sum().reset_index()
data = all_data.query("To=='EU' & Scenario=='Baseline' & Sensitivity=='Average'")

data['Activity'] = pd.Categorical(data['Activity'], categories=activities_renaming, ordered=True)
data = data.sort_values(by=['Activity'],ascending=False)

data['Activity'] = data['Activity'].map(activities_renaming)
data = data.groupby(['Activity','Item','To','Scenario','Year','Unit']).sum()
data.reset_index(inplace=True)

data['Item'] = pd.Categorical(data['Item'], categories=routes_renaming['option1'].keys(), ordered=True)
data = data.sort_values(by=['Activity','Item'])

data['Item'] = data['Item'].map(routes_renaming['option1'])

colors = {
    'Agriculture & Mining':"#8f2d56",
    'Electricity':"#f25c54",   
    'Hydrogen':"#f7b267",
    'Industry':"#8ecae6",
    'Primary steel':"#219ebc",
    'Secondary steel':"#023047",
    'Services':"#006d77"
    }

data = data.sort_values(by=['Activity','Item'],ascending=[True,True])

# main traces
fig = px.bar(data, x='Item', y='Value', color='Activity',color_discrete_map=colors)

# totals
tot = data.groupby(['Item','To','Scenario','Unit','Year',]).sum().reset_index()
x = tot['Item']
y = tot['Value']
text = [f"<b>{str(round(i,2))}" for i in y]
fig.add_trace(go.Scatter(x=x,y=y,mode='text',text=text,textposition='top center',showlegend=False))

# empty traces
ets = 2
for n in range(ets):
    fig.add_trace(go.Scatter(x=x,y=["" for i in x],mode='markers',name="",marker_color='rgba(250,250,250,0)'))
fig.add_trace(go.Scatter(x=x,y=["" for i in x],mode='markers',name="<b>Sensitivities",marker_color='rgba(250,250,250,0)'))


#sensitivities on hydrogen
pink_h2 = all_data.query("To=='EU' & Scenario=='Baseline' & Sensitivity=='100% pink H2'").groupby(['Item']).sum().loc[:,'Value'].to_frame().reset_index()
green_h2 = all_data.query("To=='EU' & Scenario=='Baseline' & Sensitivity=='100% green H2'").groupby(['Item']).sum().loc[:,'Value'].to_frame().reset_index()
pink_h2['Item'] = pd.Categorical(pink_h2['Item'], categories=routes_renaming['option1'].keys(), ordered=True)
green_h2['Item'] = pd.Categorical(green_h2['Item'], categories=routes_renaming['option1'].keys(), ordered=True)
pink_h2 = pink_h2.sort_values(by=['Item'])
green_h2 = green_h2.sort_values(by=['Item'])
pink_h2['Item'] = pink_h2['Item'].map(routes_renaming['option1'])
green_h2['Item'] = green_h2['Item'].map(routes_renaming['option1'])
pink_h2.set_index('Item',inplace=True)
green_h2.set_index('Item',inplace=True)
non_h2_routes = [i for i in list(pink_h2.index) if i not in ['H2-inj','H2-DR']]
pink_h2.loc[non_h2_routes,:] = ""
green_h2.loc[non_h2_routes,:] = ""

fig.add_trace(go.Scatter(x=pink_h2.index,y=pink_h2['Value'],mode='markers',name='Sensitivity: Pink H2',marker_color='#fbb1bd', marker_line_width=1, marker_size=8))
fig.add_trace(go.Scatter(x=green_h2.index,y=green_h2['Value'],mode='markers',name='Sensitivity: Green H2',marker_color='#96e072', marker_line_width=1, marker_size=8))

fig.update_layout(
    template=template,
    font=font,
    xaxis=dict(title=''),
    yaxis=dict(title='ton<sub>CO2eq</sub>/ton<sub>steel</sub>',range=[0,2.5]), 
    legend=dict(title="<b>         Breakdown by activity"),
    margin=dict(l=10,r=10,b=10,t=50),
    )
fig.update_layout(
    legend_title=dict(font=dict(size=font['size']))
    )

fig.update_traces(marker_line_color='black')
fig.write_html(paths['Plots']+"/GHG_Baseline_EU_by_act.html",auto_open=True)

#%% Fig 5.GHG footprint by scenario
all_data = pd.read_csv(paths['GHG footprints']['com'],index_col=[0]).groupby(['To','Scenario','Year','Sensitivity','Unit']).sum().reset_index()

data_sp1 = all_data.query("Scenario=='Baseline' & Sensitivity=='Average'").groupby("To").sum().loc[:,'Value'].to_frame()
data_sp2 = all_data.query("Scenario!='Baseline' & To=='EU'").groupby(["Scenario","Sensitivity","Year"]).sum().loc[:,'Value'].to_frame().reset_index()
# data_sp2_sns = all_data.query("Scenario!='Baseline' & Sensitivity!='Average'").groupby(["Scenario",'Sensitivity']).sum().loc[:,'Value'].unstack(1).fillna('')

fig = make_subplots(
    rows=1,cols=4,
    subplot_titles=['<b>2022','','<b>2030','<b>2050'],
    # shared_yaxes=True,
    column_widths = [0.225,0.03,0.4225,0.3225],
    horizontal_spacing=0.05,
    x_title = '<b>Scenarios'
    )

box_colors = {
    'GS-Delayed':'#133c55',
    'GS-H2':"#386fa4",
    'GS-Mix':'#59a5d8',
    'GS-Tech':"#f25c54",
    'GS-Scrap':"#8f2d56",
    'REPowerEU':"#ffb703",
    'IEA STEPS':"#fb8500",
    }

#subplot 1
regions_to_plot = ['JP','KR','US','CN','IN','EU','RU']
label_positions = ['right','left']
lp = 0
for region in regions_to_plot:
    if region=='EU':
        line_width=2
        size=12
        color='#219ebc'
    else:
        line_width=0.5
        size=8
        color='#bfc0c0'
        
    fig.add_trace(go.Scatter(
        x=['Baseline'],y=[data_sp1.loc[region,'Value']],
        mode="markers+text",
        marker_color=color,marker_line_color = 'black',marker_line_width = line_width,marker_size = size,
        text = f"{region}   ",textposition = f'middle {label_positions[lp]}',   
        showlegend=False,
        ), row=1, col=1)
    
    lp+=1
    if lp>1:
        lp=0
    
    
#subplot 2
scenarios = sorted(list(set(data_sp2.query("Year==2030")['Scenario'])))
for scenario in scenarios:
    y = data_sp2.query("Scenario==@scenario").set_index('Sensitivity').loc[:,'Value'].to_frame().values.T.tolist()[0]
    info = list(data_sp2.query("Scenario==@scenario").set_index('Sensitivity').index)

    fig.add_trace(go.Box(
        y=y,
        boxpoints='all',
        name=scenario,
        showlegend=False,
        pointpos = 0,
        marker_color=box_colors[scenario],
        line = dict(color ='rgba(0,0,0,0)'),
        fillcolor = 'rgba(0,0,0,0)',
        hovertext=info,
        ),row=1,col=3)

#subplot 3
scenarios = sorted(list(set(data_sp2.query("Year==2050")['Scenario'])))[::-1]
for scenario in scenarios:
    y = data_sp2.query("Scenario==@scenario").set_index('Sensitivity').loc[:,'Value'].to_frame().values.T.tolist()[0]
    info = list(data_sp2.query("Scenario==@scenario").set_index('Sensitivity').index)

    fig.add_trace(go.Box(
        y=y,
        boxpoints='all',
        pointpos = 0,
        name=scenario,
        showlegend=False,
        marker_color=box_colors[scenario],
        line = dict(color = 'rgba(0,0,0,0)'),
        fillcolor = 'rgba(0,0,0,0)',
        hovertext=info,
        ),row=1,col=4)


fig.update_layout(
    template=template,
    font=font,
    xaxis=dict(title=''),
    margin=dict(l=10,r=10,b=10,t=50),
    )
fig.update_yaxes(title='ton<sub>CO2eq</sub>/ton<sub>steel</sub>',range=[0,3.5],row=1,col=1)
fig.update_yaxes(title='',range=[0,1.4],dtick=0.2,row=1,col=3)
fig.update_yaxes(title='',range=[0,1.4],dtick=0.2,row=1,col=4)

fig.write_html(paths['Plots']+"/GHG_by_scenario.html",auto_open=True)


#%% Fig. 6 Prices
all_data = pd.read_csv(paths['Steel prices'],index_col=[0])
data_sp1a = all_data.query("Scenario=='Baseline' & Sensitivity=='Average'").groupby('Region').sum().loc[:,"Value"].to_frame()
data_sp1b = all_data.query("Scenario!='Baseline' & Sensitivity=='Average' & Region=='EU'").set_index('Scenario').loc[:,'Value'].to_frame()

data_sp2 = all_data.query("Region=='EU'").set_index(['Year','Scenario','Sensitivity'])
data_sp2['dp'] = ''
data_sp2 = data_sp2.loc[:,['Value','dp']]
for s in data_sp2.index:
    data_sp2.loc[s,'dp'] = (data_sp2.loc[s,'Value'] - data_sp2.loc[(2022,'Baseline','Average'),'Value']) /data_sp2.loc[(2022,'Baseline','Average'),'Value']*100
data_sp2 = data_sp2.sort_index()

ghg_data = pd.read_csv(paths['GHG footprints']['com'],index_col=[0]).query("To=='EU'").groupby(['Scenario','Year','Sensitivity']).sum().reset_index().set_index(['Year','Scenario','Sensitivity']).loc[:,"Value"].to_frame()
ghg_data['df'] = ''
ghg_data = ghg_data.loc[:,['Value','df']]
for s in ghg_data.index:
    ghg_data.loc[s,'df'] = -(ghg_data.loc[s,'Value'] - ghg_data.loc[(2022,'Baseline','Average'),'Value']) /ghg_data.loc[(2022,'Baseline','Average'),'Value']*100
ghg_data = ghg_data.sort_index()

data_sp2 = pd.concat([data_sp2,ghg_data],axis=1)
data_sp2 = data_sp2.loc[:,['dp','df']]
data_sp2 = data_sp2.iloc[3:,:]
data_sp2.reset_index(inplace=True)

fig = make_subplots(
    rows=1,cols=4,
    subplot_titles=['<b>a) Steel price by region<br><br> ','','<b>2030','<b>2050'],
    # shared_yaxes=True,
    column_widths = [0.225,0.03,0.3725,0.3725],
    horizontal_spacing=0.035,
    # x_title = '<b>Scenarios'
    )

box_colors = {
    'GS-Delayed':'#133c55',
    'GS-H2':"#386fa4",
    'GS-Mix':'#59a5d8',
    'GS-Tech':"#f25c54",
    'GS-Scrap':"#8f2d56",
    'REPowerEU':"#ffb703",
    'IEA STEPS':"#fb8500",
    }

markers = {
    'Average': {'size':12,'symbol':'diamond',},
    'CCUS max':{'size':10,'symbol':'circle'},
    'CCUS min':{'size':10,'symbol':'circle'},
    'CHL-inj max':{'size':10,'symbol':'circle'},
    'CHL-inj min':{'size':10,'symbol':'circle'},
    'H2-inj min': {'size':10,'symbol':'circle'},
    'H2 100%ELZ': {'size':10,'symbol':'circle'},
    'H2 100%SR':{'size':10,'symbol':'circle'},
    'EE 2022':{'size':10,'symbol':'circle'},
    'EE clean':{'size':10,'symbol':'circle'},
    }


#subplot 1
regions_to_plot = ['JP','KR','US','CN','IN','EU','RU']
label_positions = ['right','left']
lp = 0
for region in regions_to_plot:
    if region=='EU':
        line_width=2
        size=12
        color='#219ebc'
    else:
        line_width=0.5
        size=8
        color='#bfc0c0'
        
    fig.add_trace(go.Scatter(
        x=['Baseline<br>2022'],y=[data_sp1a.loc[region,'Value']],
        mode="markers+text",
        marker_color=color,marker_line_color = 'black',marker_line_width = line_width,marker_size = size,
        text = f"{region}   ",textposition = f'middle {label_positions[lp]}',   
        showlegend=False,
        ), row=1, col=1)
    
    lp+=1
    if lp>1:
        lp=0

for scenario in data_sp1b.index:
    fig.add_trace(go.Scatter(
        x=['Projections<br>in EU'],y=[data_sp1b.loc[scenario,'Value']],
        mode="markers",
        marker_color=box_colors[scenario],marker_line_color='black',marker_line_width=0.5,marker_size=10,
        showlegend=False,
        name=scenario,
        ), row=1, col=1)
    
#subplot 2
scenarios = sorted(list(set(data_sp2.query("Year==2030")['Scenario'])))[::-1]
for scenario in scenarios:
    sensitivities = sorted(list(set(data_sp2.query("Scenario==@scenario")['Sensitivity'])))[::-1]
    showlegend = True
    for sensitivity in sensitivities:
        
        df = data_sp2.query("Scenario==@scenario & Sensitivity==@sensitivity")
        
        if sensitivity=='Average':
            fig.add_trace(go.Scatter(
                x = df['dp'],
                y = df['df'],
                name=scenario,
                legendgroup=scenario,
                mode='markers',
                marker_color=box_colors[scenario],
                marker_size=markers[sensitivity]['size'],
                marker_symbol=markers[sensitivity]['symbol'],            
                marker_line_color='black',            
                marker_line_width=1.5,            
                showlegend=showlegend,
                hovertext=df['Sensitivity'],
                ),row=1,col=3)
        else:
            fig.add_trace(go.Scatter(
                x = df['dp'],
                y = df['df'],
                name=scenario,
                legendgroup=scenario,
                mode='markers',
                marker_color=box_colors[scenario],
                marker_size=markers[sensitivity]['size'],
                marker_symbol=markers[sensitivity]['symbol'],            
                showlegend=showlegend,
                hovertext=df['Sensitivity'],
                ),row=1,col=3)
            
        showlegend=False

ets = 2
for n in range(ets):
    fig.add_trace(go.Scatter(x=x,y=["" for i in x],mode='markers',name="",marker_color='rgba(250,250,250,0)'),row=1,col=3)
fig.add_trace(go.Scatter(x=x,y=["" for i in x],mode='markers',name="<b>2050",marker_color='rgba(250,250,250,0)'),row=1,col=3)

#subplot 3
scenarios = sorted(list(set(data_sp2.query("Year==2050")['Scenario'])))[::-1]
for scenario in scenarios:
    sensitivities = sorted(list(set(data_sp2.query("Scenario==@scenario")['Sensitivity'])))[::-1]
    showlegend = True
    for sensitivity in sensitivities:
        
        df = data_sp2.query("Scenario==@scenario & Sensitivity==@sensitivity")
        
        if sensitivity=='Average':
            fig.add_trace(go.Scatter(
                x = df['dp'],
                y = df['df'],
                name=scenario,
                legendgroup=scenario,
                mode='markers',
                marker_color=box_colors[scenario],
                marker_size=markers[sensitivity]['size'],
                marker_symbol=markers[sensitivity]['symbol'],            
                marker_line_color='black',            
                marker_line_width=1.5,            
                showlegend=showlegend,
                hovertext=df['Sensitivity'],
                ),row=1,col=4)
        else:
            fig.add_trace(go.Scatter(
                x = df['dp'],
                y = df['df'],
                name=scenario,
                legendgroup=scenario,
                mode='markers',
                marker_color=box_colors[scenario],
                marker_size=markers[sensitivity]['size'],
                marker_symbol=markers[sensitivity]['symbol'],            
                showlegend=showlegend,
                hovertext=df['Sensitivity'],
                ),row=1,col=4)
            
        showlegend=False



fig.update_layout(
    title='<b>                                                  b) Price increase vs GHG footprint reduction<br> ',
    template=template,
    font=font,
    xaxis=dict(title=''),
    legend_tracegroupgap = 0.2,
    legend=dict(title="<b>         2030"),
    margin=dict(l=10,r=10,b=50,t=70),
    )

fig.update_layout(
    title=dict(font=dict(size=16)),
    legend_title=dict(font=dict(size=font['size']))
    )


fig.update_yaxes(title='€/ton<sub>steel</sub>',range=[0,800],row=1,col=1)
fig.update_yaxes(title='€/ton<sub>steel</sub>',range=[-0.01,0.2],dtick=0.03, row=1,col=2)
fig.update_yaxes(title='GHG footprint % reduction',range=[-5,70], row=1,col=3)
fig.update_yaxes(range=[-5,70], row=1,col=4,showticklabels=False)
fig.update_xaxes(title='Price % increase',range=[0,60], row=1,col=3)
fig.update_xaxes(title='Price % increase',range=[0,60], row=1,col=4)

fig.write_html(paths['Plots']+"/Prices_by_scenario.html",auto_open=True)
