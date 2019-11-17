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



# print(config())
# config_dict = config()
# print(metaInfo.view_database_tables(config_dict['user'], config_dict['password'], 'electricity'))
# config()