import sys
import argparse
from hub_client.hubspot_client import HubSpotClient

class clargs():
    
    def __init__(self):
        self.args = sys.argv
        self.parser = argparse.ArgumentParser(
            prog='HubSpot-CRM-CLI',
            description='hubspot cli tool for crm operations',
        )
        self.parser.add_help = True
        self.subparsers = self.parser.add_subparsers(help="subcommand help")
        
        self.arg_query = argparse.ArgumentParser.add_argument('-q', '--query', type=str, help="query argument")
        self.arg_object = argparse.ArgumentParser.add_argument('-o', '--object', type=str, help="the object name for hubspot")
        
        self.create_parser = self.subparsers.add_parser(name='create',prog='create hubspot record(s)', description="create new record(s) for the object")
        self.read_parser = self.subparsers.add_parser(name='read', prog='read hubspot record(s)', help="read record(s) data for the object")
        self.update_parser = self.subparsers.add_parser(name='update', help="update record(s) data for the object")
        self.delete_parser = self.subparsers.add_parser(name='delete', help="delete record(s) for the object")
        
        # settings arguments
        self.session_parser = self.parser.add_argument('session', choices=["start", "stop"])
        self.config_parser = self.parser.add_argument('config')
        
    def get_object(self, obj:str):
        pass
        
    def parse(self):
        pass
            
    def print_intro(self):
        print()
        print("")
        
    def print_help(self):
        pass