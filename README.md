
PROJECT: ICS 32 DISTRIBUTED SOCIAL MESSENGER (ASSIGNMENT 5)

AUTHOR: PRANAV KORKONDA

STUDENT ID: 20366897

GOT QUESTIONS? EMAIL ME: pkorkond@uci.edu

1. OVERVIEW & ENGINEERING SCOPE
This application is a desktop-based Direct Messaging (DM) client that interfaces with a Distributed Social Server using a custom TCP/IP protocol. While the front-end provides a full-featured GUI for users to manage profiles and exchange messages, the back-end is engineered for high-reliability data handling.

As a Computer Engineering (CpE) focused project, it emphasizes the intersection of hardware-software communication, specifically focusing on asynchronous networking protocols and local data persistence—skills directly applicable to satellite avionics and ground-station telemetry.

2. MODULAR ARCHITECTURE
The project is divided into several modules to ensure a strict separation of concerns, mimicking professional systems integration:

GUI (a5.py): A Tkinter-based interface. It handles user input and displays conversations with dynamic left/right message alignment. A background polling mechanism is implemented using the .after() method to check for new server telemetry every 5 seconds without blocking the main UI thread.

LOGIC (ds_messenger.py): This is the "engine" of the app. The DirectMessenger class abstracts the complexity of socket connections and the "Join" authentication flow, mapping raw server data into Python DirectMessage objects.

COMMUNICATION (ds_protocol.py): This layer handles JSON serialization and deserialization. All outgoing requests and incoming responses strictly adhere to the ICS 32 distributed social protocol.

PERSISTENCE (Profile.py): An extension of the DSU profile system. It implements data persistence by storing messages and contacts locally. This ensures that critical user data is preserved across sessions and remains accessible even during network outages.

3. KEY FEATURES
Real-Time Messaging: Uses a retrieve_new protocol command to fetch incoming messages automatically.

Local History & State: All sent/received messages are appended to the .dsu profile, ensuring the local state is always synchronized.

Graceful Error Handling: Developed to handle server timeouts and network interruptions without UI crashes.

Contact Management: Dynamic UI switching based on selected recipients, managing multiple data streams simultaneously.

4. HOW TO USE
Initialize: Run python a5.py in your terminal.

Profile Setup: Go to File -> New Profile and create a .dsu file (or open an existing one).

Configure Server: Go to Settings -> Configure DS server.

IP: clotho.ics.uci.edu

Port: 2021 (hardcoded)

Note: Use the UCI VPN if you are off-campus.

Messaging: Add a contact via Settings -> Add Contact, select them from the list, and hit Send.

5. VERIFICATION & TESTING
This project strictly adheres to the assignment rubric and PEP 8 coding standards. All core logic—specifically the protocol and messenger modules—has been verified using pytest to ensure 100% reliability in data transmission and message processing.
