import json
import sys
import argparse
from hubspot import HubSpot

class clargs():
    
    def create_records(self, args):
        pass

    def search_records(self, args):
        search_dict:dict = json.loads(args.dict)
        filters:list[dict] = []
        for key, value in search_dict.items():
            filters.append({
                "value": value,
                "propertyName": key,
                "operator": "EQ"
            })

        filter_groups = [
            {
                "filters":filters
            }
        ]
        try:

            
            #
            # TODO:
            #
            api_response = self.api_client.crm.contacts


        except:
            pass

    def update_records(self, args):
        pass
    
    def delete_records(self, args):
        pass
    
    def session_parse(self, args):
        pass
    
    def config_parse(self, args):
        pass

    def __init__(self):
        self.api_client = HubSpot()
        self.args = sys.argv
        self.parser = argparse.ArgumentParser(
            prog='HubSpot-CRM-CLI',
            description='hubspot cli tool for crm operations',
        )
        self.parser.add_help = True
        self.subparsers = self.parser.add_subparsers(help="subcommand help")
        
        #self.arg_query = self.parser.add_argument('-d', '--dict', type=json.loads, help="dictionary argument for filtering, creating or updating records")
        #self.arg_object = self.parser.add_argument('-o', '--object', type=str, help="the object name for hubspot")
        
        # create positional
        self.create_parser = self.subparsers.add_parser(name='create',prog='create hubspot record(s)', help="create new record(s) for the object")
        self.create_parser.set_defaults(func=self.create_records)

        # read positional
        self.read_parser = self.subparsers.add_parser(name='read', prog='read hubspot record(s)', help="read record(s) data for the object")
        self.read_parser.set_defaults(func=self.search_records)
        self.read_parser.add_argument('-o', '--object', type=str, required=True, help="the object name for hubspot")
        self.read_parser.add_argument('-d', '--dict', type=str, required=True, help="dictionary argument for filtering, creating or updating records")
        
        # update positional
        self.update_parser = self.subparsers.add_parser(name='update', help="update record(s) data for the object")
        self.update_parser.set_defaults(func=self.update_records)

        # delete positional
        self.delete_parser = self.subparsers.add_parser(name='delete', help="delete record(s) for the object")
        self.delete_parser.set_defaults(func=self.delete_records)


        # settings arguments
        self.session_parser = self.subparsers.add_parser(name='session', help="start a hubspot cli session")
        self.session_parser.set_defaults(func=self.session_parse)

        self.config_parser = self.subparsers.add_parser(name='config', help="configuration settings for hubspot cli")
        self.config_parser.set_defaults(func=self.config_parse)
        #self.parser.print_help()
        args = self.parser.parse_args()
        args.func(args)


    def get_object(self):
        pass
        
    def parse(self):
        pass
            
    def print_intro(self):
        print()
        print("")
        
    def print_help(self):
        pass