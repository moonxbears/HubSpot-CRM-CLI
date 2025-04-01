import json
import sys
import argparse
from hubspot import HubSpot
from hubspot.crm.objects import PublicObjectSearchRequest, ApiException
from hubspot.crm.objects.models.collection_response_with_total_simple_public_object_forward_paging import CollectionResponseWithTotalSimplePublicObjectForwardPaging
from hubspot.crm.objects.models.simple_public_object import SimplePublicObject
from prettytable import PrettyTable

class clargs():
    
    def _get_access_token(self):
        with open("C:\\Users\\jnjohnson\\Documents\\dev\\HubSpotCRM\\HubSpot-CRM-CLI\\accessToken", 'r') as file:
            self.access_token = file.readline()

    def _get_format(self, args, response:CollectionResponseWithTotalSimplePublicObjectForwardPaging):
        results:list[SimplePublicObject] = response.results
        table = PrettyTable()
        table.field_names = dict[str, str](results[0].properties).keys()
        for item in results:
            
            pass

        if (args.format_type == "table"):
            pass
        return response


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
                "filters": filters
            }
        ]
        obj_request = PublicObjectSearchRequest(filter_groups=filter_groups)
        try:
            api_response:CollectionResponseWithTotalSimplePublicObjectForwardPaging = self.api_client.crm.objects.search_api.do_search(object_type=args.object, public_object_search_request=obj_request)
            obj = self._get_format(args=args, response=api_response)
            print(obj)

        except ApiException as e:
            print(f"exception when calling search_api->do_search: {e}")

    def update_records(self, args):
        pass
    
    def delete_records(self, args):
        pass
    
    def session_parse(self, args):
        pass
    
    def config_parse(self, args):
        pass



    def __init__(self):
        self._get_access_token()
        self.api_client = HubSpot(access_token=self.access_token)
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
        self.read_parser.add_argument('-f', '--format-type', type=str, required=False, default="table", choices=["table", "csv", "json", "info"], help="the format of the results of the query to return")

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