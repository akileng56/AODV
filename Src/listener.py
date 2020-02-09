# Imports
import threading, socket, sys


# Class Definition
class listener(threading.Thread):

    # Constructor
    def __init__(self):
        threading.Thread.__init__(self)
        self.num_nodes = 0
        self.node_id = ""
        self.sock = 0
        self.port = 0
        self.aodv_listener_port = 0
        self.command = ""

    # Set the Node ID
    def set_node_id(self, id):
        self.node_id = id

    # Set the number of nodes in the network
    def set_node_count(self, count):
        self.num_nodes = count

    # Return the listener port associated with the given node
    def get_listener_port(self, node_id):
        port = {'n1': 1000,
                'n2': 1100,
                'n3': 1200,
                'n4': 1300,
                'n5': 1400,
                'n6': 1500,
                'n7': 1600,
                'n8': 1700,
                'n9': 1800,
                'n10': 1900}[node_id]

        return port

    # Return the listener port associated with the given node
    def get_aodv_listener_port(self, node_id):
        port = {'n1': 2000,
                'n2': 2100,
                'n3': 2200,
                'n4': 2300,
                'n5': 2400,
                'n6': 2500,
                'n7': 2600,
                'n8': 2700,
                'n9': 2800,
                'n10': 2900}[node_id]

        return port

    # Generic routine to send the user request to the protocol handler thread
    def send(self, message):
        self.sock.sendto(message, 0, ('localhost', self.aodv_listener_port))

    # Called when user issues help. Dump the list of available commands.
    def help(self):
        print("\n The following list of commands are available:")
        print("2 - activate_link   : Simulate a link-up event on the current AODV node")
        print("3 - add_neighbors   : Add neighbors to the current AODV node")
        print("4 - deactivate_link : Simulate a link-down event on the current AODV node")
        print("5 - delete_messages : Delete all the messages received so far")
        print("6 - send_message    : Send a message to a peer node")
        print("7 - show_log        : View the contents of the log file")
        print("8 - show_messages   : View the messages received so far")
        print("9 - show_route      : Display the routing table for the AODV node \n")

    # Wait for the response from protocol handler thread
    def wait_for_response(self):
        # Wait for the status
        (msg, _) = self.sock.recvfrom(10)
        status = msg.decode('utf-8')

    # Simulate a link-up event for this node
    def activate(self):
        message_type = "NODE_ACTIVATE"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Take the neighbor set for the current node from the user. This will be handled by the AODV library   
    def add_neighbors(self):
        message_type = "ADD_NEIGHBOR"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Simulate a link-down event for this node
    def deactivate(self):
        message_type = "NODE_DEACTIVATE"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Delete all the messages received so far
    def delete_messages(self):
        message_type = "DELETE_MESSAGES"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Send a message to a peer
    def send_message(self):

        # Get the message details from the user
        node = input("Enter the destination: ")
        message = input("Enter the message to send: ")


        message_type = "SEND_MESSAGE"
        message = message_type + ":" + self.node_id + ":" + node + ":" + message
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Display the contents of the log file. Just invoke the library routine.
    def show_log(self):
        message_type = "VIEW_LOG"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Display the messages sent to this node by other nodes
    def show_messages(self):
        message_type = "VIEW_MESSAGES"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Display the routing table        
    def show_route(self):
        message_type = "SHOW_ROUTE"
        message = message_type + ":" + ""
        message_bytes = bytes(message)
        self.send(message_bytes)
        self.wait_for_response()

    # Default routine called when invalid command is issued. Do nothing.
    def default(self):
        if (len(self.command) == 0):
            pass
        else:
            print("Invalid Command")

    # Thread start routine
    def run(self):

        # Get the listener ports
        self.port = self.get_listener_port(self.node_id)
        self.aodv_listener_port = self.get_aodv_listener_port(self.node_id)

        # Setup socket to communicate with the AODV protocol handler thread
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', self.port))
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Set the prompt
        prompt = "AODV-" + self.node_id + "> "

        # Listen indefinitely for user inputs and pass them to the AODV protocol handler thread
        while (True):
            command = input(prompt)

            try:
                n = int(command)
            except:
                print("Invalid Input")
                sys.exit(0)

            if n == 1:
                self.help()
            elif n == 2:
                self.activate()
            elif n == 3:
                self.add_neighbors()
            elif n == 4:
                self.deactivate()
            elif n == 5:
                self.delete_messages()
            elif n == 6:
                self.send_message()
            elif n == 7:
                self.show_log()
            elif n == 8:
                self.show_messages()
            elif n == 9:
                self.show_route()
            else:
                self.help()

# End of File
