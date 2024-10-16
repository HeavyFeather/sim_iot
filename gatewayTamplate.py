import paho.mqtt.client as mqtt
import time
import threading
import jsonHandler

node_id = 0

nodes = {}
broker_address="localhost"


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def on_connect(client, userdata, flags, rc):
    print("[+] Node connected")

def on_subscribe(client, userdata, mid, granted_qos):
    print("[+] Subscribed with QoS: {}".format(granted_qos[0]))

def create_dummy():
    global node_id
    node_id += 1
    print("Creating dummy node...")
    node_name = input(f"[?] Enter name of node {node_id}: ")
    nodes.update({node_id: node_name})

    client = mqtt.Client(f"Dummy_{node_name}") #create new instance

    client.on_message=on_message #attach function to callback
    client.on_connect=on_connect
    client.on_subscribe=on_subscribe

    client.connect(broker_address, 1884)
    client.subscribe("asd")

    client.loop_forever()

# Создание ноды шлюза из конфига json (v1)
def create_gate(host):
    global node_id
    node_id += 1

    print("Creating gateway node...")
    node_name = host["node_name"]

    client = mqtt.Client(f'Gateway "{node_name}"') #create new instance
    nodes.update({node_id: client}) # отправляет инстанс в словарь 

    client.on_message=on_message #attach function to callback
    client.on_connect=on_connect
    client.on_subscribe=on_subscribe

    client.connect(broker_address, 1884)

    if host["is_forever"] != True:
        client.loop_start()

    if host["subscriber_for"] != None:
        client.subscribe(host["subscriber_for"])

    if host["publisher_for"] != None:
        for i in range(10):
            client.publish(host["publisher_for"],"ping")
            time.sleep(3)

    if host["is_forever"] != True:
        client.loop_stop()

    if host["is_forever"] == True:
        client.loop_forever()
    

# Запуск конфига
def deploy_config(config):
    global node_id
    threads = [] # каждый поток - узел

    #config_path = input("Enter config name: ")
    #jsonHandler.import_config(config_path)


    for host in config["hosts"]:
        if host["node_type"] == "gateway":
            threads.append(threading.Thread(target = create_gate, args = host)) # need creating thread of net process

        elif host["node_type"] == "dummy":
            threads.append(threading.Thread(target = create_dummy, args = host))

        else:
            print('[-] Invalid json config: "node_type"')
            raise SystemExit()
    

    for t in threads:
        t.start

    for t in threads:
        t.join

    

def print_topo():
    print(nodes)


def manager():
    current_config = {}

    button = input('1) Change topology\n2) Run topology\n3) Print topo\nTo quit type "exit"\nChoosing: ')
    while(True):
        if button == "1":
            current_config = change_topo()

        elif button == "2":
            deploy_config(current_config) # Добавить аргумент в функцию

        elif button == "3":
            print_topo()

        elif button == "exit":
            raise SystemExit()

def change_topo():
    button = input('1) Import existing json config\n2) Create arbitrage topo\n3) Create test topo\nTo quit type "exit"\nChoosing: ')

    while True:
        if button == "1":
            return jsonHandler.import_config()
        
        elif button == "2":
            return create_arbitrage()
        
        elif button == "exit":
            return 0

        else:
            print("[-] Invalid value")
            return 0
    
def create_arbitrage():
    current_config = {}

    button = input('1) Add node\n2) Delete node\n3) Save config\nTo quit type "exit"\nChoosing: ')

    while True:
        if button == "1":
            a = 1

        elif button == "exit":
            return 0

        else:
            print("[-] Invalid value")
            return 0

    return current_config

if __name__ == "__main__":
    manager()