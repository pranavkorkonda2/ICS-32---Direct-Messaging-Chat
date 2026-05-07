"""This module manages the direct messaging logic and communication with the DS server"""
import socket
import json
import time
import ds_protocol

def cleanup(filename='ds_messenger.py'):
    """Removes trailing white spaces for this file"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    with open(filename, 'w') as f:
        f.writelines(cleaned_lines)
class DirectMessage:
    """Class for a single dm, including sender, recipient, content and timestamp"""
    def __init__(self, recipient=None, message=None, timestamp=None):
        """DM is intialized with optional recipient and timestamp"""
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        self.sender = None


class DirectMessenger:
    """This class handles the authentication and communication with the DS server for sending and receiving messages"""
    def __init__(self, dsuserver=None, username=None, password=None):
        """Initialize the DirectMessenger with server, username, and password."""
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.token = None # token stored here after authentication
        self.sock = None # how else would we send messages?
        self.message_history = [] # history
        self.port = 2021 # added this oops
    
    def send_json(self, json_message:str) -> ds_protocol.DataTuple:
        """Raw json string is sent to DS server, and a parsed datatuple is parsed"""
        return self._send_to_server_json(json_message)
    
    def publish(self, message:str, recipient:str=None) -> bool:
        """Message is sent to the recipient. This is also an alias for the send method for compatibility."""
        if recipient is None:
            raise ValueError("Recipient cannot be None for publish method. Please provide a valid recipient.")
        return self.send(message, recipient)


    def send(self, message:str, recipient:str) -> bool:
        """Message is sent to a specific recipient. Authentication and history tracking are all handled"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._authenticate()
        if not self.token:
            print("Authentication failed. Cannot send message.")
            return False
        timestamp = int(time.time())
        json_message = ds_protocol.send_direct_message_json(self.token, message, recipient, timestamp)
        response = self.send_json(json_message)
        if response.type == "ok":
            dm = DirectMessage(recipient, message, timestamp)
            dm.sender = self.username
            self.message_history.append(dm)
            return True
        else:
            print(f"Failed to send message: {response.message}")
            return False
    
    def retrieve_new(self) -> list:
        """Retrieves only new messages received since last request from ds server"""
        return self._retrieve_messages("new")
    
    def retrieve_all(self) -> list:
        """Retrieves the entire direct message history from the DS server."""
        return self._retrieve_messages("all")
    
    def _authenticate(self) -> bool:
        """User is authenticated with the ds server to obtain session token"""
        if self.token:
            return True

        server_joiner_json = json.dumps({
            "join": {
                "username": self.username,
                "password": self.password,
                "token": ""
            }
        })
        json_response = self.send_json(server_joiner_json)
        if json_response.type is None or json_response.type != "ok":
            self.token = None
            print("Authentication failed. Server response:", json_response.message)
            return False
        else:
            self.token = json_response.token
            return True
                         
            # bascially what we just did is send a json msg to the server with our 
            #user/pass, and the server responds with a json msg  that contains a token 
            #which we store for future use. we will need this token is what we use to
            # authenticate ourselves when sending messages or requesting message history.

    def _retrieve_messages(self, message_type) -> list:
        """Internal helper to request msgs from server based on specific type, like new or all"""
        self._authenticate()
        if not self.token:
            print("Authentication failed. Cannot retrieve messahes")
            return []
        if message_type == "new":
            json_request = ds_protocol.request_new_token_json(self.token)
        elif message_type == "all":
            json_request = ds_protocol.request_message_history_json(self.token)
        else:
            print("Invalid message type. Must be 'new' or 'all'. Please try again.")
            return [] # made this change because a list is expected by the caller
        
        json_response = self.send_json(json_request)

        # now we need to loop through the messages and convert them to DM objects.

        messages = []

        for message in json_response.messages:
            direct_msg = DirectMessage()
            # DS protocol returns direct messages with key "message"
            # plus "from" and "timestamp".
            direct_msg.message = message.get('entry', message.get('message', ''))
            direct_msg.sender = message.get('from', '')
            direct_msg.timestamp = message.get('timestamp', None)
            # Keep original recipient if provided in the response, otherwise use current username.
            direct_msg.recipient = message.get('recipient', self.username)
            messages.append(direct_msg)

        return messages
    
    def _send_to_server_json(self, json_message:str) -> ds_protocol.DataTuple:
        """Here we establish a socket sonnection, send the JSON payload, and receive the response"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(3) # if server is down, we don't want to wait forever
                sock.connect((self.dsuserver, self.port))
                sock.sendall((json_message + '\n').encode('utf-8'))
                recv_data = sock.recv(4096).decode('utf-8')
                return ds_protocol.extract_json(recv_data)
        except (socket.error, socket.timeout) as e:
            print(f"Error communicating with the server: {e}")
            return ds_protocol.DataTuple(type='error', message=str(e), token='', messages=[])
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ds_protocol.DataTuple(type='error', message=str(e), token='', messages=[])
    

