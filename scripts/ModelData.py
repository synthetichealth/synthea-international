from collections import OrderedDict

#
# define types for omop schema
#
class ModelData:
    #
    # Check the model matches
    #
    def __init__(self):
       self.model_schema = self.dataSchema()

    #
    # define schema for various data loads being used
    #
    def dataSchema(self):
        model_schema = OrderedDict([])
        #
        # Standardized vocabulary
        #
        model_schema['openaddress'] = OrderedDict([
            ('LAT', 'object'),
            ('LON', 'object'),
            ('NUMBER', 'category'),
            ('STREET', 'category'),
            ('UNIT', 'category'),
            ('CITY', 'category'),
            ('DISTRICT', 'category'),
            ('REGION', 'category'),
            ('POSTCODE', 'category'),
            ('ID', 'object'),
            ('HASH','object')
        ])

        model_schema['fiaddress'] = OrderedDict([
            ('building_id', 'object'),
            ('region', 'category'),
            ('municipality', 'category'),
            ('street', 'category'),
            ('house_number', 'category'),
            ('postal_code', 'category'),
            ('latitude_wgs84', 'object'),
            ('longitude_wgs84', 'object'),
            ('building_use', 'category')
        ])

        model_schema['postalcodes'] = OrderedDict([
            ('USPS', 'object'),
            ('ST', 'category'),
            ('NAME', 'object'),
            ('ZCTA5', 'category'),
            ('LAT', 'object'),
            ('LON', 'object')
        ])

        model_schema['geoname'] = OrderedDict([
            ('geonameid', 'object'),
            ('name', 'object'),
            ('asciiname', 'object'),
            ('alternatenames', 'object'),
            ('latitude', 'object'),
            ('longitude', 'object'),
            ('feature class', 'object'),
            ('feature code', 'object'),
            ('country code', 'object'),
            ('cc2', 'object'),
            ('admin1 code', 'object'),
            ('admin2 code', 'object'),
            ('admin3 code', 'object'),
            ('admin4 code', 'object'),
            ('population', 'object'),
            ('elevation', 'object'),
            ('dem', 'object'),
            ('timezone', 'object'),
            ('modification date', 'object')
        ])

        return model_schema
