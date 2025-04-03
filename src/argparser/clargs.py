import json
from multiprocessing.pool import AsyncResult
import sys
import argparse
from threading import Thread
from hubspot import HubSpot
from hubspot.crm.objects import PublicObjectSearchRequest, ApiException
from hubspot.crm.objects.models.collection_response_with_total_simple_public_object_forward_paging import CollectionResponseWithTotalSimplePublicObjectForwardPaging
from hubspot.crm.objects.models.simple_public_object import SimplePublicObject
from prettytable import PrettyTable
import ast
import os
import math
import time

class clargs():
    
    def _get_access_token(self):
        with open("C:\\Users\\jnjohnson\\Documents\\dev\\HubSpotCRM\\HubSpot-CRM-CLI\\accessToken", 'r') as file:
            self.access_token = file.readline()

    def _output_file(self, args, result):
        path = os.path.dirname(args.output_file)
        abs_path = os.path.abspath(path)    
        os.makedirs(abs_path, exist_ok=True)  # Create the directory if it doesn't exist
        with open(args.output_file, 'w') as f:
            f.write(result)

    def _animate_load(self):
        cols = 0
        
        while self._is_running:
            self.print_load = f"{self.record_after} out of {self.total_records} processed"
            print("\r" + " " * cols, end="", flush=True)
            print(self.print_load, end="", flush=True)
            time.sleep(1)

    def _start_animation(self):
        self._is_running = True
        self._thread.start()

    def _stop_animation(self):
        self._is_running = False

    def _get_format(self, args, filter_groups:list):

        after = None
        results:list[SimplePublicObject] = []
        if (args.limit == 0):
            args.limit = 2000000
        limit = args.limit
        counter = args.limit
        api_calls = 0

        seq_limit = 200
        if (counter <= 200):
            seq_limit = counter

        api_calls += 1
        request = None
        props:list[str] = None
        if (args.properties):
            props = ast.literal_eval(args.properties)
            request = PublicObjectSearchRequest(filter_groups=filter_groups, after=after, limit=seq_limit, properties=props)
        else:
            request = PublicObjectSearchRequest(filter_groups=filter_groups, after=after, limit=seq_limit)
        response:CollectionResponseWithTotalSimplePublicObjectForwardPaging = self.api_client.crm.objects.search_api.do_search(object_type=args.object, public_object_search_request=request)
        results.extend(response.results)
        
        self.total_records:int = response.total
        remainder_records = self.total_records % 200
        total_pages = math.ceil(self.total_records / 200)
        self.record_after = min(response.total, 200, seq_limit)
        current_page = 1

        all_threads:list[AsyncResult] = []
        
        self._thread = Thread(target=self._animate_load, daemon=True)
        self._start_animation()

        for i in range(1, total_pages):
            self.record_after = i*200
            seq_limit = min(self.total_records - self.record_after, 200)
            api_calls += 1
            if (props is None):
                request = PublicObjectSearchRequest(filter_groups=filter_groups, after=i*200, limit=seq_limit)
            else:
                request = PublicObjectSearchRequest(filter_groups=filter_groups, after=i*200, limit=seq_limit, properties=props)
            aresult:AsyncResult = self.api_client.crm.objects.search_api.do_search(object_type=args.object, public_object_search_request=request, async_req=True) 
            all_threads.append(aresult)
            # hubspot restricts api calls / second 
            time.sleep(0.2)
            #print(f"pages: {response.paging}\ntotal: {response.total}")

        for i in range(0, len(all_threads)):
            val = all_threads[i].get()
            response:CollectionResponseWithTotalSimplePublicObjectForwardPaging = val
            results.extend(response.results)

        self._stop_animation()

        if (args.format_type == "info"):
            if (args.output_file):
                str_results = "\n".join([s.to_str() for s in results])
                self._output_file(args, str_results)
            return (results, len(results), api_calls)
        
        search_args:list[tuple] = ast.literal_eval(args.query)
        table = PrettyTable()
        
        fields:set = set()
        if (props is None):
            for field in search_args:
                fields.add(field[0])
            table.field_names = fields
        else:
            table.field_names = set(props)


        if (props is None):
            for item in results:
                row:dict = {}
                for search_item in search_args:
                    row[search_item[0]] = (item.properties[search_item[0]])
                table.add_row([row[field] for field in fields])
        else:
            for item in results:
                row:dict = {}
                for search_item in props:
                    row[search_item] = (item.properties[search_item])
                table.add_row([row[field] for field in props])


        out_string = ""
        if (args.format_type == "table"):
            out_string = table.get_string()
        elif (args.format_type == "csv"):
            out_string = table.get_csv_string(delimiter=',')
        elif (args.format_type == "json"):
            out_string = table.get_json_string(header=False, indent=4)

        if (args.output_file):
            self._output_file(args, out_string)

        return (out_string, len(table.rows), api_calls)


    def create_records(self, args):
        pass

    def search_records(self, args):
        search_args:list[tuple] = ast.literal_eval(args.query)
        filters:list[dict] = []
        
        for item in search_args:
            if (len(item) != 3):
                raise IndexError("tuple needs 3 items for (field, operator, value)")
            filters.append({
                "value": item[2],
                "propertyName": item[0],
                "operator": item[1]
            })

        filter_groups = [
            {
                "filters": filters
            }
        ]
        
        # Fetch records iteratively
    
        try:            
            obj = self._get_format(args=args, filter_groups=filter_groups)
            print(obj[0])
            print(f"\nrecords = {obj[1]}\napi calls = {obj[2]}")

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
        self.read_parser.add_argument('-q', '--query', type=str, required=True, help="A list of 3 item tuple arguments for filtering, creating or updating records. [(field, operator, value)]")
        self.read_parser.add_argument('-f', '--format-type', type=str, required=False, default="table", choices=["table", "csv", "json", "info"], help="the format of the results of the query to return")
        self.read_parser.add_argument('-l', '--limit', type=int, required=False, default=0, help="limit the amount of records retrieved")
        self.read_parser.add_argument('-c', '--output-file', type=str, required=False, default=None, help="output records to a file")
        self.read_parser.add_argument('-p', '--properties', type=str, required=False, help="a string representing a python list[str] of properties to return from the query")

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