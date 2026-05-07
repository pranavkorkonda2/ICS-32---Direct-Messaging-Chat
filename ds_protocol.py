# ds_protocol.py

# Starter code for assignment 5 (ICS 32)

# Replace placeholders with your information.

# NAME Pranav Korkonda
# EMAIL pkorkond@uci.edu
# STUDENT ID 20366897
"""Module for handling encoding and decoding of json messages according to the ds protocol"""
import json
from collections import namedtuple


def cleanup(filename='ds_protocol.py'):
    """Removes trailing whitespace"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    with open(filename, 'w') as f:
        f.writelines(cleaned_lines)
# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token', 'messages'])


def extract_json(json_msg: str) -> DataTuple:
    """Namedtuple that stores structured components of a ds server response"""
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        r_type = response['type']
        msg = response.get('message', '')
        token = response.get('token', '') or json_obj.get('token', '')
        messages = response.get('messages', [])
        return DataTuple(type=r_type, message=msg, token=token, messages=messages)
    except (json.JSONDecodeError, KeyError) as e:
        return DataTuple(type='error', message=str(e), token='', messages=[])

def send_direct_message_json(token, message, recipient, timestamp):
    """Encodes a direct message into the JSON format required by the DS server."""
    return json.dumps({
        "token": token,
        "directmessage": {
            "recipient": recipient,
            "entry": message,
            "timestamp": timestamp
        }
    })

def request_new_token_json(token) -> str:
    """Encodes a request to retrieve only new unread messages from the server"""
    return json.dumps({
        "token": token,
        "directmessage": "new"
    })

def request_message_history_json(token) -> str:
    """Encodes a request to retireve full direct message history from the server"""
    return json.dumps({
        "token": token,
        "directmessage": "all"
    })
