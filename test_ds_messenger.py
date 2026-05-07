"""
This module contains unit tests for the DirectMessenger class in ds_messenger.py.
Run this file after implementing the DirectMessenger class to check correctness of your implementation!
"""
import ds_protocol
from ds_messenger import DirectMessage, DirectMessenger

def cleanup(filename='test_ds_messenger.py'):
    """Removes trailing whitespace"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    with open(filename, 'w') as f:
        f.writelines(cleaned_lines)
def test_messenger_init():
    """
    Tests init function of direct messenger class.
    Checks everything is initialized correctly, and that the message history is empty.
    """
    dm = DirectMessenger(dsuserver="recipient.name", username="sender", password="password")
    assert dm.dsuserver == "recipient.name"
    assert dm.username == "sender"
    assert dm.password == "password"
    assert dm.token is None
    assert dm.sock is None
    assert dm.message_history == []

def test_send_message_without_authentication():
    """
    If a message was sent w/o authentication, send function should return False.
    Although it's an edge case we should still make sure our code handles it gracefully.
    """
    dm = DirectMessenger(dsuserver="recipient.name", username="sender", password="password")
    result = dm.send("Test message", "recipient")
    assert result is False

def test_authentication_and_send_message():
    """
    Tests that if we set a valid token, messages should be sent successfully.
    This test assumes send_json function is working, so authentication is mocked.
    Also, we check if msg history is updated correctly after sending a msg.
    """
    dm = DirectMessenger(dsuserver="recipient.name", username="sender", password="password")
    dm.token = "valid_token" # we just mock authentication here for testing purposes
    def mock_send(json_msg):
        return ds_protocol.DataTuple(type='ok', message='Direct message sent', token='', messages=[])
    dm.send_json = mock_send
    result = dm.send("Test message", "recipient")
    assert result is True
    assert len(dm.message_history) == 1
    assert dm.message_history[0].recipient == "recipient"
    assert dm.message_history[0].message == "Test message"

def test_retrieve_messages():
    """
    Tests that retrieve_all funct returns the correct msg history.
    """
    dm = DirectMessenger(dsuserver="recipient.name", username="sender", password="password")
    dm.token = "valid_token"
    def mock_send(json_msg):
            return ds_protocol.DataTuple(
                type='ok', message='', token='', messages=[
                    {'recipient': 'recipient1', 'entry': 'Hello!', 'timestamp': 1234567890, 'from':'sender'}
                ]
            )
    dm.send_json = mock_send
    dm.message_history.append(DirectMessage("recipient1", "Hello!", 1234567890))
    messages = dm.retrieve_all()
    assert len(messages) == 1
    assert messages[0].recipient == "recipient1"
    assert messages[0].message == "Hello!"

def test_retrieve_new_messages():
    """
    Tests that retrieve_new funct returns the correct msg history.
    Since we haven't implemented any functionality to clear message 
    history after retrieval, retrieve_new should return the same history 
    as retrieve_all, which is all messages in the history.
    """
    dm = DirectMessenger(dsuserver="recipient.name", username="sender", password="password")
    dm.token = "valid_token"
    # mock send is basically just returning 2 messages for retrieval, but
    # since we haven't implemented message history clearing, both retrieve_all and 
    # retrieve_new will return the same messages.
    def mock_send(json_msg):
        return ds_protocol.DataTuple(
            type='ok', message='', token='', messages=[
                {'recipient': 'recipient1', 'entry': 'Hello!', 'timestamp': 1234567890, 'from':'sender'},
                {'recipient': 'recipient2', 'entry': 'Hi again!', 'timestamp': 1234567891, 'from':'sender'}
            ]
        )
    dm.send_json = mock_send
    new_messages = dm.retrieve_new()
    assert len(new_messages) == 2 # 2 not 1 bc message history hasnt been cleared
    assert new_messages[0].recipient == "recipient1"
    assert new_messages[0].message == "Hello!"
    assert new_messages[1].recipient == "recipient2"
    assert new_messages[1].message == "Hi again!"

# time for edge cases
def test_invalid_dsuserver():
    """
    Edge case #1:
    If the dsuserver is invalid (e.g. server is down or wrong IP), send 
    function should return False and not crash.
    """
    dm = DirectMessenger(dsuserver="127.0.0.1", username="test", password="test")
    result = dm.send("Edge case message", "recipient")
    assert result is False

def test_invalid_retrieval():
    """
    Edge case #2:
    If there are no messages to retrieve, retrieve functions should return an empty list.
    """
    
    # so if retriev is empty
    dm = DirectMessenger(dsuserver="recipient.name", username="sender", password="password")
    dm.token = None
    messages = dm.retrieve_new()
    assert isinstance(messages, list)
    assert len(messages) == 0



if __name__ == "__main__":
    try:
        print("Running tests for ds_messenger.py...")
        test_messenger_init()
        test_send_message_without_authentication()
        test_authentication_and_send_message()
        test_retrieve_messages()
        test_retrieve_new_messages()
        test_invalid_dsuserver()
        test_invalid_retrieval()
        print("YAY! All tests passed successfully!")
    except AssertionError as e:
        print(f"A test failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
