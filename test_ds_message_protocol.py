"""Module that contains unit tests for the ds_protocol.py module to ensure correct JSON encoding/decoding"""
import ds_protocol
import json # forgot this oops

def cleanup(filename='test_ds_message_protocol.py'):
    """Removes trailing whitespace"""
    with open(filename, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    with open(filename, 'w') as f:
        f.writelines(cleaned_lines)
def test_extract_json():
    """Tests extraction of a standard success response w/ token and message"""
    json_msg = """
    {
        "response": {
            "type": "success",
            "message": "Token generated",
            "token": "abc123"
            }
    }
    """
    result = ds_protocol.extract_json(json_msg)
    assert result.type == "success"
    assert result.message == "Token generated"
    assert result.token == "abc123"
    assert result.messages == []
    print("Test #1: Extract JSON test passed!")

def test_send_direct_message_json():
    """Verifies that the direct msg JSON is correctly formatted with the required entry and recipient keys"""
    token = 'qwertyuiop'
    message = "HELLO WORLD"
    recipient = "Pranav"
    timestamp = 1234567890
    expected_json = '{"token": "qwertyuiop", "directmessage": {"recipient": "Pranav", "entry": "HELLO WORLD", "timestamp": 1234567890}}'
    result_json = ds_protocol.send_direct_message_json(token, message, recipient, timestamp)
    assert json.loads(result_json) == json.loads(expected_json)
    print("Test #2: Send Direct Message JSON test passed.")

def test_request_new_token_json():
    """Tests request for 'new' messages generates correct JSON structure for the server"""
    token = 'asdfghjkl'
    expected_json = '{"token": "asdfghjkl", "directmessage": "new"}'
    result_json = ds_protocol.request_new_token_json(token)
    assert json.loads(result_json) == json.loads(expected_json)
    print("Test #3: Request New Token JSON test passed.")

def test_request_message_history_json():
    """Tests the request for all message history generates the correct jSON structure for the server"""
    token = 'zxcvbnm'
    expected_json = '{"token": "zxcvbnm", "directmessage": "all"}'
    result_json = ds_protocol.request_message_history_json(token)
    assert json.loads(result_json) == json.loads(expected_json)
    print("Test #4: Request Message History JSON test passed.")

def test_extract_json_all_messages():
    """Tests the successful extraction for all objects in a list of message obj"""
    json_msg = """{
        "response": {
            "type": "ok",
            "messages": [
                {"message": "Hello", "from": "pranav", "timestamp": "1"}
            ]
        }
    }"""

    result = ds_protocol.extract_json(json_msg)
    assert result.type == "ok"
    assert result.messages[0]["from"] == "pranav"
    assert result.messages[0]["message"] == "Hello"
    assert result.messages[0]["timestamp"] == "1"
    print("Test #5: Extract JSON with messages test passed.")

def test_extract_json_directmessage_history():
    """Validates that a condensed JSON string containing message history is parsed correctly inside a datatuple"""
    json_msg = '{"response":{"type":"ok","messages":[{"message":"Hello","from":"korkonda","timestamp":"1.23"}]}}'
    result = ds_protocol.extract_json(json_msg)
    assert result.type == "ok"
    assert len(result.messages) == 1
    assert result.messages[0]["from"] == "korkonda"
    assert result.messages[0]["message"] == "Hello"
    assert result.messages[0]["timestamp"] == "1.23"
    print("Test #6: Extract JSON with direct message history test passed.")


if __name__ == "__main__":
    try:
        print("Running tests for ds_protocol.py...")
        test_extract_json()
        test_send_direct_message_json()
        test_request_new_token_json()
        test_request_message_history_json()
        test_extract_json_all_messages()
        test_extract_json_directmessage_history()
        print("YAY! All tests passed successfully!")
    except AssertionError as e:
        print(f"A test failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

