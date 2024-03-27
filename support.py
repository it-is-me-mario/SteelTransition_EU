#%%
import pandas as pd

sN=slice(None)

def get_new_sets(set_map,main_sheet,db):
    
    new_activities = list(set(set_map[main_sheet]['Activity']))
    new_commodities = list(set(set_map[main_sheet]['Commodity']))

    # listing parented activities
    parented_activities = []
    for act in new_activities:
        parent = set_map[main_sheet].query("Activity==@act")["Parent"].values[0]
        if type(parent)==str:
            parented_activities += [act]
    
    # excluding already existing activities    
    new_activities = [x for x in new_activities if x not in db.get_index('Activity')]

    # excluding parented activities    
    for act in parented_activities:
        new_activities.remove(act)

    # excluding already existing commodities            
    new_commodities = [x for x in new_commodities if x not in db.get_index('Commodity')]
    
    return new_activities,new_commodities,parented_activities
    

def fill_units(path,item,new_items,set_map,main_sheet):

    template = pd.read_excel(path,sheet_name='units')
    new_units = set_map[main_sheet].query("Commodity==@new_items").loc[:,[item,'FU_unit']].set_index(item).to_dict()
    template['unit'] = template[list(template.columns)[0]].map(new_units['FU_unit'])
    template.set_index(list(template.columns)[0],inplace=True)
    template.index.names = ['']
    
    with pd.ExcelWriter(path, mode='a', engine='openpyxl',if_sheet_exists='replace') as writer:
        template.to_excel(writer,sheet_name='units')

def parent_parented(db,set_map,main_sheet,parented_activities):
    
    z=db.z
    v=db.v
    e=db.e
    
    for pa in parented_activities:
        parent = set_map[main_sheet].query("Activity==@pa")['Parent'].values[0]
        region = set_map[main_sheet].query("Activity==@pa")['Region'].values[0]
        
        z.loc[:,(region,sN,pa)] = z.loc[:,(region,sN,parent)].values
        v.loc[:,(region,sN,pa)] = v.loc[:,(region,sN,parent)].values
        e.loc[:,(region,sN,pa)] = e.loc[:,(region,sN,parent)].values

    db.update_scenarios('baseline',z=z,v=v,e=e)
    db.reset_to_coefficients('baseline')


def fill_u(activities,set_map,main_sheet,db,world,region_maps,sheet_to_fill):
    
    for act in activities:
        print(act)
        act_sheets = set_map[main_sheet].query("Activity==@act")['Sheet_name'].to_list()
        
        for sheet in act_sheets:
            inventory_indices = list(set_map[sheet].columns)
            inventory_indices.remove('quantity') 
    
            inventory = set_map[sheet].loc[set_map[sheet].Item=='Commodity']
            inventory['conv_quantity'] = ""
                    
            # region import share 
            regions_db = list(set(inventory[f"{db} Region"]).intersection(world.get_index('Region')))
            inputs_db = inventory.query(f"`{db} Region` == @regions_db")
            inputs_non_db = inventory.query(f"`{db} Region` != @regions_db")
            
            for i in inputs_non_db.index:
                commodity = inputs_non_db.loc[i,f"{db} Commodity"]
                region = inputs_non_db.loc[i,f"{db} Region"]
                
                com_use = world.U.loc[(region_maps[region],sN,commodity),(set_map[main_sheet].query("Activity==@act & Sheet_name==@sheet")['Region'].values[0],sN,sN)]   # da aggiornare se chenery
                u_share = com_use.sum(1)/com_use.sum().sum()*inputs_non_db.loc[i,'quantity']
                
                idb = {}
                for col in inputs_non_db.columns:
                    idb[col] = [inputs_non_db.loc[i,col] for r in u_share.index]
                    if col == f"{db} Region":
                        idb[col] = list(u_share.index.get_level_values('Region'))
                    if col == 'quantity':
                        idb[col] = u_share.values.tolist()               
                inputs_db = pd.concat([inputs_db,pd.DataFrame(idb)],axis=0)
            
            # append to shock template
            u = {
                'row region': inputs_db[f'{db} Region'],
                'row level': ['Commodity' for r in inputs_db.index],
                'row sector': inputs_db[f'{db} Commodity'],
                'column region': [set_map[main_sheet].query("Activity==@act & Sheet_name==@sheet")['Region'].values[0] for r in inputs_db.index],
                'column level': ['Activity' for r in inputs_db.index],
                'column sector': [act for r in inputs_db.index],
                'type': [inputs_db.iloc[r,list(inputs_db.columns).index('Type')] for r in inputs_db.index],
                'value': inputs_db['quantity'],
                }
            
            sheet_to_fill = pd.concat([sheet_to_fill, pd.DataFrame(u)],axis=0)
        
    return sheet_to_fill

def fill_e(activities,set_map,main_sheet,db,world,region_maps,sheet_to_fill):
    
    for act in activities:
        act_sheets = set_map[main_sheet].query("Activity==@act")['Sheet_name'].to_list()
        
        for sheet in act_sheets:
            inventory = set_map[sheet].loc[set_map[sheet].Item=='Satellite account']
                    
            inputs_db = inventory
    
            e = {
                'row sector': inputs_db[f'{db} Commodity'],
                'column region': [set_map[main_sheet].query("Activity==@act & Sheet_name==@sheet")['Region'].values[0] for r in inputs_db.index],
                'column level': ['Activity' for r in inputs_db.index],
                'column sector': [act for r in inputs_db.index],
                'type': inputs_db['Type'].to_list(),
                'value': inputs_db['quantity'],
                }
            print(act)
            
            sheet_to_fill = pd.concat([sheet_to_fill, pd.DataFrame(e)], axis=0)
    
    return sheet_to_fill



#%%
def add_new_supply_chains(
        paths, 
        main_sheet, 
        world, 
        add_sectors_template=False,
        db = 'EXIOBASE',
        scenario='new supply chains',
        ):
    
    # reading map and getting sets
    Add_sectors_map = pd.read_excel(paths['Map'], sheet_name=None)
    region_maps = {k:Add_sectors_map['region_maps'][k].dropna().to_list()  for k in Add_sectors_map['region_maps'].columns}
    new_activities,new_commodities,parented_activities = get_new_sets(Add_sectors_map,main_sheet,world)    
            
    # Getting excel templates to add new activities and commodities
    if add_sectors_template:
        world.get_add_sectors_excel(new_sectors=new_commodities,regions=world.get_index('Region'),path=paths['commodities'], item='Commodity')
        world.get_add_sectors_excel(new_sectors=new_activities+parented_activities,regions=world.get_index('Region'),path=paths['activities'], item='Activity')
        
        # read commodity template and add units
        fill_units(path=paths['commodities'],item='Commodity',new_items=new_commodities,set_map=Add_sectors_map,main_sheet=main_sheet)
        fill_units(path=paths['activities'],item='Activity',new_items=new_activities+parented_activities,set_map=Add_sectors_map,main_sheet=main_sheet)
            
        
    # Adding new commodities and activities    
    world.add_sectors(io=paths['commodities'], new_sectors=new_commodities, regions=world.get_index('Region'), item= 'Commodity', inplace=True)
    world.add_sectors(io=paths['activities'], new_sectors=new_activities+parented_activities, regions=world.get_index('Region'), item= 'Activity', inplace=True )    
           
    # copy parent into parented activities
    parent_parented(world,Add_sectors_map,main_sheet,parented_activities)
    
    # create shock templates
    world.get_shock_excel(path=paths['values'])
    shock_sheets = pd.read_excel(paths['values'], sheet_name=None)
    
    # fill excel sheets
    shock_sheets['z'] = fill_u(
        activities=new_activities+parented_activities,
        set_map=Add_sectors_map, 
        main_sheet=main_sheet, 
        db=db, 
        world=world,
        region_maps=region_maps,
        sheet_to_fill=shock_sheets['z'])
    
    shock_sheets['e'] = fill_e(
        activities=new_activities+parented_activities,
        set_map=Add_sectors_map, 
        main_sheet=main_sheet, 
        db=db, 
        world=world,
        region_maps=region_maps,
        sheet_to_fill=shock_sheets['e'])
    
    # market_shares
    s = {
        'row region': Add_sectors_map[main_sheet]['Region'],
        'row level': ['Activity' for r in Add_sectors_map[main_sheet].index],
        'row sector': Add_sectors_map[main_sheet]['Activity'],
        'column region': Add_sectors_map[main_sheet]['Region'],
        'column level': ['Commodity' for r in Add_sectors_map[main_sheet].index],
        'column sector': Add_sectors_map[main_sheet]['Commodity'],
        'type': ['Update' for r in Add_sectors_map[main_sheet].index],
        'value': Add_sectors_map[main_sheet]['Market share'],     
        }
        
    shock_sheets['z'] = pd.concat([shock_sheets['z'].fillna(0), pd.DataFrame(s)],axis=0) # Sto azzerando settori problematici
    
    with pd.ExcelWriter(paths['values']) as writer:
        for sheet,df in shock_sheets.items():
            df.to_excel(writer,sheet_name=sheet, index=False)
    writer.close()
    
    world.shock_calc(paths['values'],z=True,e=True,scenario=scenario)
        
    world.to_txt(paths['Database']+"/1. Baseline final", flows=False, coefficients=True, scenario=scenario)
        
#%% scenarios functions

def update_mix_u(world,new_mix,scenario,region):

    z = world.get_data('z',scenarios=scenario)[scenario][0]
    u = world.get_data('u',scenarios=scenario)[scenario][0]
    Y = world.get_data('Y',scenarios=scenario)[scenario][0]

    # update u
    u_ee = u.loc[(region,slice(None),list(new_mix.index)),:]
    u_ee.sort_index(level=-1,inplace=True) 
    u_ee_sum = u_ee.sum().to_frame().T
    new_u_ee = pd.DataFrame(new_mix.values @ u_ee_sum.values, index=u_ee.index, columns=u_ee.columns)
    u.update(new_u_ee)

    # update Y
    Y_ee = Y.loc[(region,'Commodity',list(new_mix.index)),:]
    Y_ee.sort_index(level=-1,inplace=True) 
    Y_ee_sum = Y_ee.sum().to_frame().T
    new_Y_ee = pd.DataFrame(new_mix.values @ Y_ee_sum.values, index=Y_ee.index, columns=Y_ee.columns)
    Y.update(new_Y_ee)

    z.update(u)

    # update mario database  
    world.update_scenarios(scenario,z=z,Y=Y)
    world.reset_to_coefficients(scenario)
    
#%%
def CCUS(world,route,value,region,scenario,sat='CO2'):
    
    e = world.get_data('e',scenarios=scenario)[scenario][0]
    e.loc[sat,(region,'Activity',route)] *= value
                
    world.update_scenarios(scenario,e=e)
    world.reset_to_coefficients(scenario)

#%%
def H2inj_mix(world,h2_from,h2_to,route,region,scenario):
    
    z = world.get_data('z',scenarios=scenario)[scenario][0]
    sumH2 = z.loc[(region,'Commodity',[h2_from,h2_to]),(region,'Activity',route)].sum().sum()
    z.loc[(region,'Commodity',h2_from),(region,'Activity',route)] = 0
    z.loc[(region,'Commodity',h2_to),(region,'Activity',route)] = sumH2
    
    world.update_scenarios(scenario,z=z)
    world.reset_to_coefficients(scenario)
    
#%%
def inj_change(world,commodities,values,routes,region,scenario):

    z = world.get_data('z',scenarios=scenario)[scenario][0]
    for route in routes:
        for commodity in commodities:
            z.loc[(region,'Commodity',commodity),(region,'Activity',route)] = values[commodities.index(commodity)]
    
    world.update_scenarios(scenario,z=z)
    world.reset_to_coefficients(scenario)
    
