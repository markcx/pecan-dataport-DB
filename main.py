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


def run():
    config_dict = config()
    tables = metaInfo.view_database_tables(config_dict['host'], config_dict['user'], config_dict['password'], 'electricity')

    # metaInfo.view_data_window(config_dict['host'], config_dict['user'], config_dict['password'], 'other_datasets.metadata', 'eg_realpower_1min', buildingIDs[0:20])
    # table_name = 'eg_realpower_1hr'
    for j in range(tables.size):

        # try:
        table_name = tables['electricity'][j]
        print('processing table {:d} : {}'.format(j, table_name))
        if '_1s' in table_name:
            print("skip {:d}".format(j))
            continue
        buildingIDs = metaInfo.view_buildings(config_dict['host'], config_dict['user'], config_dict['password'],
                                              'electricity.' + table_name, table_name)

        metaInfo.download_dataport(config_dict['host'],
                                   config_dict['user'],
                                   config_dict['password'],
                                   'data/%s.h5' % (table_name),
                                   'electricity',
                                   table_name,
                                   periods_to_load={ k: ('2012-01-01', '2019-11-17') for k in buildingIDs})
    # except Exception:
        #     print("Some error when parse {}!".format(j))

        # except:
        #     pass


if __name__ == "__main__":
    run()
