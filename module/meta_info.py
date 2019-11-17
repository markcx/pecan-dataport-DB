"""
Reference:

https://github.com/nilmtk/nilmtk
"""

"""
MANUAL:

dataport is a large dataset hosted in a remote SQL database. This
file provides a function to download the dataset and save it to disk
as NILMTK-DF. Since downloading the entire dataset will likely take >
24 hours, this function provides some options to allow you to download
only a subset of the data.

'''''''''''''''' Previous Version '''''''''''''''''''''
For example, to only load house 26 for April 2014:
    from nilmtk.dataset_converters.dataport.download_dataport
    import download_dataport
    download_dataport(
        'username',
        'password',
        '/path/output_filename.h5',
        periods_to_load={26: ('2014-04-01', '2014-05-01')}
    )
'''''''''''''''' Previous Version '''''''''''''''''''''

'''''''''''''''' New Version '''''''''''''''''''''

    from nilmtk.dataset_converters.dataport.download_dataport
    import download_dataport,
            _dataport_dataframe_to_hdf,
            view_database_tables,
            view_buildings,
            view_data_window

    # see all available tables in the dataport database.
    view_database_tables(
        'username',
        'password',
        'database_schema'    # electricity
    )

    # show the list of all available buildings
    view_buildings(
        'username',
        'password',
        'database_schema',  # electricity
        'table_name'        # for example 'eg_realpower_1min', 'eg_current_15min'
    )

    # view data collection window of selected buildings
    view_data_window(
        'username',
        'password',
        'database_schema',  # electricity
        'table_name',       # for example 'eg_realpower_1min','eg_current_1hr'
        [18,26,43,44]       # data collection window of building 18,26,43 and 44 respectively
    )

    # download the dataset.
    For example, loading electricity_egauge_hours from 2018-11-17 to
    2019-12-17 of building 26
    download_dataport(
        'username',
        'password',
        '/path/output_filename.h5',
        'electricity',
        'eg_realpower_1hr',
        periods_to_load={ 26: ('2018-11-17', '2019-12-17')})


'''''''''''''''' New Version '''''''''''''''''''''

REQUIREMENTS:

On Ubuntu:
* sudo apt-get install libpq-dev
* sudo pip install psycopg2

TODO:
* intelligently handle queries that fail due to network
* integrate 'grid' (use - gen) and 'gen'

"""

import psycopg2 as db
import pandas as pd

################### table columns ####################

feed_mapping = {
                'air1': {'type': 'air conditioner'},
                'air2': {'type': 'air conditioner'},
                'air3': {'type': 'air conditioner'},
                'airwindowunit1': {'type': 'air conditioner'},
                'aquarium1': {'type': 'appliance'},
                'bathroom1': {'type': 'sockets', 'room': 'bathroom'},
                'bathroom2': {'type': 'sockets', 'room': 'bathroom'},
                'bedroom1': {'type': 'sockets', 'room': 'bedroom'},
                'bedroom2': {'type': 'sockets', 'room': 'bedroom'},
                'bedroom3': {'type': 'sockets', 'room': 'bedroom'},
                'bedroom4': {'type': 'sockets', 'room': 'bedroom'},
                'bedroom5': {'type': 'sockets', 'room': 'bedroom'},
                'battery1': {},                       #new field, need mapping
                'car1': {'type': 'electric vehicle'},
                'circpump1': {},                      #new field, need mapping
                'clotheswasher1': {'type': 'washing machine'},
                'clotheswasher_dryg1': {'type': 'washer dryer'},
                'diningroom1': {'type': 'sockets', 'room': 'dining room'},
                'diningroom2': {'type': 'sockets', 'room': 'dining room'},
                'dishwasher1': {'type': 'dish washer'},
                'disposal1': {'type': 'waste disposal unit'},
                'drye1': {'type': 'spin dryer'},
                'dryg1': {'type': 'spin dryer'},
                'freezer1': {'type': 'freezer'},
                'furnace1': {'type': 'electric furnace'},
                'furnace2': {'type': 'electric furnace'},
                'garage1': {'type': 'sockets', 'room': 'dining room'},
                'garage2': {'type': 'sockets', 'room': 'dining room'},
                'grid': {},
                'heater1': {'type': 'electric space heater'},
                'heater2': {'type': 'electric space heater'},
                'heater3': {'type': 'electric space heater'},
                'housefan1': {'type': 'electric space heater'},
                'icemaker1': {'type': 'appliance'},
                'jacuzzi1': {'type': 'electric hot tub heater'},
                'kitchen1': {'type': 'sockets', 'room': 'kitchen'},
                'kitchen2': {'type': 'sockets', 'room': 'kitchen'},
                'kitchenapp1': {'type': 'sockets', 'room': 'kitchen'},
                'kitchenapp2': {'type': 'sockets', 'room': 'kitchen'},
                'lights_plugs1': {'type': 'light'},
                'lights_plugs2': {'type': 'light'},
                'lights_plugs3': {'type': 'light'},
                'lights_plugs4': {'type': 'light'},
                'lights_plugs5': {'type': 'light'},
                'lights_plugs6': {'type': 'light'},
                'livingroom1': {'type': 'sockets', 'room': 'living room'},
                'livingroom2': {'type': 'sockets', 'room': 'living room'},
                'microwave1': {'type': 'microwave'},
                'office1': {'type': 'sockets', 'room': 'office'},
                'outsidelights_plugs1': {'type': 'sockets', 'room': 'outside'},
                'outsidelights_plugs2': {'type': 'sockets', 'room': 'outside'},
                'oven1': {'type': 'oven'},
                'oven2': {'type': 'oven'},
                'pool1': {'type': 'electric swimming pool heater'},
                'pool2': {'type': 'electric swimming pool heater'},
                'poollight1': {'type': 'light'},
                'poolpump1': {'type': 'electric swimming pool heater'},
                'pump1': {'type': 'appliance'},
                'range1': {'type': 'stove'},
                'refrigerator1': {'type': 'fridge'},
                'refrigerator2': {'type': 'fridge'},
                'security1': {'type': 'security alarm'},
                'sewerpump1': {},               #new field, need mapping
                'shed1': {'type': 'sockets', 'room': 'shed'},
                'solar': {},
                'solar2': {},
                'sprinkler1': {'type': 'appliance'},
                'sumppump1': {},                #new field, need mapping
                'utilityroom1': {'type': 'sockets', 'room': 'utility room'},
                'venthood1': {'type': 'appliance'},
                'waterheater1': {'type': 'electric water heating appliance'},
                'waterheater2': {'type': 'electric water heating appliance'},
                'wellpump1': {},                #new field, need mapping
                'winecooler1': {'type': 'appliance'},
                'leg1v':{},
                'leg2v':{}
                }

feed_ignore = ['solar', 'solar2', 'grid', 'leg1v', 'leg2v', 'battery1', 'circpump1',
               'sewerpump1', 'sumppump1', 'wellpump1']


def database_assert(database_table):
    assert (
            database_table == 'eg_angle_15min' or
            database_table == 'eg_angle_1hr' or
            database_table == 'eg_angle_1min' or
            database_table == 'eg_angle_1s' or
            database_table == 'eg_apparentpower_15min' or
            database_table == 'eg_apparentpower_1hr' or
            database_table == 'eg_apparentpower_1min' or
            database_table == 'eg_apparentpower_1s' or
            database_table == 'eg_current_15min' or
            database_table == 'eg_current_1hr' or
            database_table == 'eg_current_1min' or
            database_table == 'eg_current_1s' or
            database_table == 'eg_realpower_15min' or
            database_table == 'eg_realpower_1hr' or
            database_table == 'eg_realpower_1min' or
            database_table == 'eg_realpower_1s' or
            database_table == 'eg_thd_15min' or
            database_table == 'eg_thd_1hr' or
            database_table == 'eg_thd_1min' or
            database_table == 'eg_thd_1s' or
            database_table == 'eg_realpower_1s_40homes_dataset'
            ), "Table not compatible with desired electricity shemas!"


def view_database_tables(
        database_username,
        database_password,
        database_schema
):
    database_host = 'dataport.pecanstreet.org'
    database_port = '5434'
    database_name = 'dataport'

    try:
        conn = db.connect('host=' + database_host +
                          ' port=' + database_port +
                          ' dbname=' + database_name +
                          ' user=' + database_username +
                          ' password=' + database_password)
    except:
        print('Could not connect to remote database')
        raise

    # Loading university schemas
    sql_query = ("SELECT table_name" +
                 " FROM information_schema.views" +
                 " WHERE table_schema ='" + database_schema + "'" +
                 " ORDER BY table_name")
    database_tables = pd.read_sql(sql_query, conn)['table_name'].tolist()

    df = pd.DataFrame({database_schema: database_tables})
    print(df)
    conn.close()







