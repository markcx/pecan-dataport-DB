from configparser import ConfigParser
import module.meta_info as metaInfo

def config(filename='pecan_database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db



config_dict = config()
# metaInfo.view_database_tables(config_dict['host'], config_dict['user'], config_dict['password'], 'electricity')
buildingIDs = metaInfo.view_buildings(config_dict['host'], config_dict['user'], config_dict['password'], 'electricity.eg_angle_15min', 'eg_angle_15min')
metaInfo.view_data_window(config_dict['host'], config_dict['user'], config_dict['password'], 'other_datasets.metadata', 'eg_realpower_1min', buildingIDs[0:20])

