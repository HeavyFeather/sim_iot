#import jsonHandler
from time import sleep
import asyncio

import coap_client as cli
import coap_server as srv

node_id = 0

nodes = {}

def main():
    
    print("Resource creating...")

    asyncio.run(srv.server_())
    print("Server created [+]")
    print("Performing clients actions")

    # while(True):    
    #     sleep(5)
    #     asyncio.run(cli.client_())

main()