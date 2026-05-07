"""
MAIN UI interface for a5.
This module provides a graphical interface for a distributed social messenger app
by using Tkinter. It allows for profile management, contact addiction,
as well as direct messaging.
"""
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Text
import time
from Profile import Profile, DsuFileError, DsuProfileError

def cleanup(filename='a5.py'):
    """
    Removes trailing whitespacing in the file.
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    cleaned_lines = [line.rstrip() + '\n' for line in lines]
    with open(filename, 'w') as f:
        f.writelines(cleaned_lines)

class Body(tk.Frame):
    """
    A subclass of the tk.Frame that contains the main UI elements for displaying
    contacts and the conversation history.
    """
    def __init__(self, root, recipient_selected_callback=None):
        """
        Body frame is initialized and widgets are drawn
        """
        tk.Frame.__init__(self, root)
        self.root = root
        self._contacts = []
        self._select_callback = recipient_selected_callback
        # After all initialization is complete,
        # call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    def node_select(self, event):
        """Callback for when a contact is selected in the Treeview."""
        post_selection_tree = self.posts_tree.selection()
        if not post_selection_tree:
            return
        item_id = post_selection_tree[0]
        entry = self.posts_tree.item(item_id, 'text')
        if self._select_callback is not None:
            self._select_callback(entry)

    def insert_contact(self, contact: str):
        """Adds a new contact to the internal list, and the Treeview is updated."""
        self._contacts.append(contact)
        contact_id = len(self._contacts) - 1
        self._insert_contact_tree(contact_id, contact)

        if self._select_callback is not None:
            self._select_callback(contact)

    def _insert_contact_tree(self, id, contact: str):
        """Inserts a contact name into the Treeview widget (truncated of course)"""
        if len(contact) > 25:
            contact_display = contact[:24] + "..."
        else:
            contact_display = contact
        self.posts_tree.insert('', 'end', iid=str(id), text=contact_display)

    def insert_user_message(self, message:str):
        """A message sent by the user is inserted into conversation editor"""
        self.entry_editor.config(state=tk.NORMAL)
        self.entry_editor.insert('end', message + '\n', 'entry-right')
        self.entry_editor.config(state=tk.DISABLED)


    def insert_contact_message(self, message:str):
        """A message sent by the contact is inserted into conversation editor"""
        self.entry_editor.config(state=tk.NORMAL)
        self.entry_editor.insert('end', message + '\n', 'entry-left')
        self.entry_editor.config(state=tk.DISABLED)

    def get_text_entry(self) -> str:
        """Returns text currently in the message entry editor"""
        return self.message_editor.get('1.0', 'end').rstrip()

    def set_text_entry(self, text:str):
        """Text is set in the message entry"""
        self.message_editor.delete(1.0, tk.END)
        self.message_editor.insert(1.0, text)

    def _draw(self):
        """Widgets are created and packed for Body frame"""
        instructions_label = tk.Label(self, text="Select a contact on the left, type your message below, and click Send",
                                     bg='#e8efff', fg='#333', font=('Arial', 10, 'bold'))
        instructions_label.pack(fill=tk.X, pady=5)

        posts_frame = tk.Frame(master=self, width=250, bg='#dde6f2')
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        contacts_label = tk.Label(posts_frame, text="Contacts", bg='#dde6f2')
        contacts_label.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)
        self.posts_tree.pack(fill=tk.BOTH, expand=True)

        editor_frame = tk.Frame(master=self, bg="#f5f5f5")
        editor_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        convo_label = tk.Label(editor_frame, text="Conversation", bg='#f5f5f5')
        convo_label.pack(fill=tk.X, side=tk.TOP)

        scroll_frame = tk.Frame(master=editor_frame, bg="gray")
        scroll_frame.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        self.entry_editor = tk.Text(editor_frame, width=0, height=5, state=tk.DISABLED, bg="#f5f5f5",  font=("Segoe UI Emoji", 10))
        self.entry_editor.tag_configure('entry-right', justify='right', foreground='#203A92', rmargin=20)
        self.entry_editor.tag_configure('entry-left', justify='left', foreground='#1C9DD5', lmargin1=10, lmargin2=10)
        self.entry_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=8, pady=8)

        entry_editor_scroll = tk.Scrollbar(master=scroll_frame, command=self.entry_editor.yview)
        entry_editor_scroll.pack(fill=tk.Y, side=tk.LEFT)

        msg_frame = tk.Frame(master=self, bg="#e8efff")
        msg_frame.pack(fill=tk.X, side=tk.TOP, expand=False)

        entry_label = tk.Label(msg_frame, text="Message Entry Here", bg="#f0f0f0")
        entry_label.pack(fill=tk.X, side=tk.TOP)

        self.message_editor = tk.Text(msg_frame, width=0, height=5)
        self.message_editor.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)


class Footer(tk.Frame):
    """A subclass of tk.Frame; status label and send button live here"""
    def __init__(self, root, send_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._send_callback = send_callback
        self._draw()

    def send_click(self):
        """Footer frame is initialized here"""
        if self._send_callback is not None:
            self._send_callback()

    def _draw(self):
        """Send callback is triggered here whenever an event like the send button is clicked"""
        save_button = tk.Button(master=self, text="Send", width=20, command=self.send_click)
        # You must implement this.
        # Here you must configure the button to bind its click to
        # the send_click() function.
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


class NewContactDialog(tk.simpledialog.Dialog):
    """Dialog window for server and user credential configuration"""
    def __init__(self, root, title=None, user=None, pwd=None, server=None):
        """Dialogue is initialized with existing credentials"""
        self.root = root
        self.server = server
        self.user = user
        self.pwd = pwd
        super().__init__(root, title)

    def body(self, frame):
        """Dialog body is built using Entry Widgets"""
        tk.Label(frame, text="DS Server:").grid(row=0, column=0)
        self.server_entry = tk.Entry(frame, width=30)
        self.server_entry.insert(0, self.server if self.server else "")
        self.server_entry.grid(row=0, column=1)

        tk.Label(frame, text="Username:").grid(row=1, column=0)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.insert(0, self.user if self.user else "")
        self.username_entry.grid(row=1, column=1)

        tk.Label(frame, text="Password:").grid(row=2, column=0)
        self.password_entry = tk.Entry(frame, width=30, show="*") # password is hidden. good luck hacking lol
        self.password_entry.insert(0, self.pwd if self.pwd else "")
        self.password_entry.grid(row=2, column=1)

        return self.server_entry # initial focus on server entry

    def apply(self):
        """Entry values are saved whenever the dialogue is accepted"""
        self.server = self.server_entry.get()
        self.user = self.username_entry.get()
        self.pwd = self.password_entry.get()


class MainApp(tk.Frame):
    """Main application class for the UI and messenger logic"""
    def __init__(self, root):
        """Initialized the main application state and draws the UI"""
        tk.Frame.__init__(self, root)
        self.root = root
        self.username = None
        self.password = None
        self.server = None
        self.recipient = None
        self.profile = Profile() # forgot this
        self.profile_path = None
        self.direct_messenger = None

        self._draw()
        # No default contact shown before profile/server setup to avoid confusion.
        # Contacts should come from loaded profile or Add Contact.
        self.footer.footer_label.config(text="No profile loaded. Use File->Open Profile or file->New Profile to begin.")

    def send_message(self):
        """Local history gets updated as the selected recepient is sent the message"""
        msg = self.body.get_text_entry()
        recipient = self.recipient
        if not recipient:
            print("No recipient selected!")
            self.footer.footer_label.config(text="Select a recipient before sending a message.")
            return

        if not self.direct_messenger:
            print("DirectMessenger not configured. configure server first.")
            self.footer.footer_label.config(text="DirectMessenger not configured. Use Settings->Configure DS Server.")
            return

        if not msg:
            print("Message entry is empty.")
            self.footer.footer_label.config(text="Message entry is empty. Please enter a message to send.")
            return

        print(f"Sending message to recipient {recipient}: {msg}")
        result = self.direct_messenger.send(msg, recipient)

        if result:
            new_direct_message = {
                "from": self.username,
                "to": recipient,
                "message": msg,
                "timestamp": int(time.time())
            }
            self.profile.messages.append(new_direct_message)
            if self.profile_path:
                try:
                    self.profile.save_profile(self.profile_path)
                except Exception as e:
                    print(f"Failed to save profile after send: {e}")
            self.body.insert_user_message(f"You: {msg}")
            self.body.set_text_entry("")
            self.footer.footer_label.config(text="Message sent.")
        else:
            print(f"Failed to send message to {recipient}.")
            self.footer.footer_label.config(text="Failed to send message; check network/server.")

    def add_contact(self):
        """Username is prompted and added to contact list"""
        import tkinter.simpledialog
        contact = tk.simpledialog.askstring("Add Contact", "Enter the username of the contact")

        if contact:
            if contact not in self.body._contacts:
                self.profile.contacts.append(contact)

                if self.profile_path:
                    self.profile.save_profile(self.profile_path) # save the updated profile with the new contact list

                self.body.insert_contact(contact) # also add to the contact list on the left side of the UI
                print(f"Contact '{contact}' added successfully.")
                print(f"Updated contact list: {self.profile.contacts}")
            else:
                print(f"Contact '{contact}' already exists in the contact list.")
        else:
            print("No contact entered. Operation cancelled.")

    def recipient_selected(self, recipient):
        """Conversation view is updated whenever a contact is selected"""
        if not self.profile:
            print("You need to load or create a profile before selecting a recipient.")
            return
        self.recipient = recipient
        print(f"Recipient selected: {recipient}")

        # clear the entry editor before showing new messages for the selected recipient
        self.body.entry_editor.config(state=tk.NORMAL)
        self.body.entry_editor.delete(1.0, tk.END)
        self.body.entry_editor.config(state=tk.DISABLED)
        # now we loop thru msg history and filter msgs for the selected recipient, then display them in the entry editor

        for msg in self.profile.messages:
            # first check if I sent it to them
            if msg.get('to') == recipient and msg.get('from') == self.username:
                self.body.insert_user_message(f"You: {msg['message']}")
            # now check if they sent it to me
            elif msg.get('to') == self.username and msg.get('from') == recipient:
                self.body.insert_contact_message(f"{recipient}: {msg['message']}")
            else:
                continue #
                # somehow, if the filtration messed it up and gives a message not between
                # the two of us by some miracle, we just skip it.
    def configure_server(self):
        """Config dialog is opened and initializes DirectMessenger"""
        from ds_messenger import DirectMessenger
        dialogue = NewContactDialog(self.root, title="Configure DS Server", user=self.username, pwd=self.password, server=self.server)
        if dialogue.server and dialogue.user and dialogue.pwd:
            self.server = dialogue.server
            self.username = dialogue.user
            self.password = dialogue.pwd
            print(f"Server configured: {self.server}, Username: {self.username}")
        else:
            print("Server configuration cancelled or incomplete.")
            self.direct_messenger = None
            return

        if self.server and self.username and self.password:
            self.direct_messenger = DirectMessenger(dsuserver=self.server, username=self.username, password=self.password)
            #self.direct_messenger.send_json = lambda json_msg: ds_protocol.DataTuple(type='ok', message='OK', token='TEST', messages=[])
            print(f"DirectMessenger instance created with server: {self.server}, username: {self.username}")

            if not self.direct_messenger._authenticate():
                print("DirectMessenger authentication failed; check username/password/host.")
                self.footer.footer_label.config(text="Auth failed; check server/credentials.")
                self.direct_messenger = None
            else:
                print("DirectMessenger authenticated successfully.")
                self.profile.dsuserver = self.server
                self.profile.username = self.username
                self.profile.password = self.password
                if self.profile_path:
                    self.profile.save_profile(self.profile_path)
                self.footer.footer_label.config(text="DirectMessenger configured and authenticated.")
        else:
            print("Failed to create DirectMessenger instance due to missing server, username, or password.")
            self.footer.footer_label.config(text="Missing server/username/password.")
            self.direct_messenger = None

    def publish(self, message:str):
        """Public method logic"""
        if self.direct_messenger:
            result = self.direct_messenger.publish(message, recipient=self.recipient)
            if result:
                print(f"Message published successfully: {message}")
            else:
                print(f"Failed to publish message: {message}")
        else:
            print("DirectMessenger instance not configured. Cannot publish message.")


    def check_new(self):
        """Server is polled for new msgs and updates UI"""
        if self.direct_messenger:
            try:
                new_messages = self.direct_messenger.retrieve_new()
                if new_messages:
                    for msg in new_messages:
                        sender = getattr(msg, 'sender', None) or "Unknown"
                        recipient = getattr(msg, 'recipient', None) or self.username
                        # store both sides so conversation filtering is robust
                        msg_dict = {
                            "from": sender,
                            "to": recipient,
                            "message": msg.message,
                            "timestamp": msg.timestamp
                        }
                        self.profile.messages.append(msg_dict)
                        if self.recipient == sender:
                            self.body.insert_contact_message(f"{sender}: {msg.message}")
                    if self.profile_path:
                        try:
                            self.profile.save_profile(self.profile_path)
                        except Exception as e:
                            print(f"Failed to save profile after check_new: {e}")
            except Exception as e:
                print(f"check_new exception: {e}")
                new_messages = []
        self.root.after(5000, self.check_new) # check for new messages every 5 seconds


    def _draw(self):
        """Menu bar and main frames created here"""
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar

        # creates file dropdown menu
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=file_menu, label="File")

        # now we connect our methods!
        file_menu.add_command(label="New Profile", command=self.new_profile)
        file_menu.add_command(label="Open Profile", command=self.open_profile)
        file_menu.add_command(label="Close Profile", command=self.close_profile)
        file_menu.add_command(label="Exit", command=self.root.quit)

        settings = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=settings, label="Settings")
        settings.add_command(label="Configure  DS Server", command=self.configure_server)
        settings.add_command(label="Add Contact", command=self.add_contact)
        # Alias publish to send for safety and protocol consistency
        settings.add_command(label="Publish Message", command=self.send_message)
        settings.add_command(label="Send Message", command=self.send_message)

        self.body = Body(self.root, recipient_selected_callback=self.recipient_selected)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(self.root, send_callback=self.send_message)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)
    def open_profile(self):
        """Existing DSU file is opened, then data is loaded"""
        file_path = filedialog.askopenfilename(title="Open Profile", filetypes=[("DSU Files", "*.dsu")])

        if file_path:
            try:
                self.profile.load_profile(file_path)
                self.profile_path = file_path
                self.server = self.profile.dsuserver
                self.username = self.profile.username
                self.password = self.profile.password
                print(f"Profile loaded successfully from {file_path}!")
                print(f"Username: {self.profile.username}")
                print(f"DS Server: {self.profile.dsuserver}")
                print(f"Contacts: {self.profile.contacts}")

                # apply the loaded data to UI
                for contact in self.profile.contacts:
                    self.body.insert_contact(contact)

                if self.profile.contacts:
                    self.recipient = self.profile.contacts[0]

                # attempt to configure and authenticate automatically, if credentials exist
                if self.server and self.username and self.password:
                    self.configure_server()
            except DsuFileError as e:
                print(f"Error loading profile: {e}")
            except DsuProfileError as e:
                print(f"Error with profile data: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
        else:
            print("No file selected. Operation cancelled.")

        if self.profile.contacts:
            # add contacts once to avoid duplicates
            self.body._contacts = []
            self.body.posts_tree.delete(*self.body.posts_tree.get_children())
            for contact in self.profile.contacts:
                self.body.insert_contact(contact)
            self.recipient = self.profile.contacts[0]
            # automatically show conversation history for first contact loaded
            self.recipient_selected(self.recipient)

    def new_profile(self):
        """A new profile is created and stored in a dsu file"""
        file_path = filedialog.asksaveasfilename(
            title="Create New Profile",
            defaultextension=".dsu",
            filetypes=[("DSU Files", "*.dsu")]
        )

        if file_path:
            if not file_path.endswith('.dsu'):
                file_path += '.dsu'

            # create a profile file immediately so user does not lose setup if server is down
            self.profile = Profile()
            self.profile_path = file_path
            self.profile.dsuserver = ''
            self.profile.username = ''
            self.profile.password = ''
            try:
                self.profile.save_profile(file_path)
                print(f"New profile located at {file_path} (saved empty template).")
            except DsuFileError as e:
                print(f"Error saving new profile: {e}")
                return

            # attempt server configuration; fine if it fails, profile still exists
            self.configure_server()

            if self.direct_messenger:
                self.profile.dsuserver = self.server
                self.profile.username = self.username
                self.profile.password = self.password
                try:
                    self.profile.save_profile(file_path)
                    print(f"New profile configured and updated at {file_path}!")
                except DsuFileError as e:
                    print(f"Error saving configured profile: {e}")
            else:
                print("DirectMessenger not configured. Profile file remains available for manual fiddling.")

            # clear contact list and reload after profile actions
            self.body._contacts = []
            self.body.posts_tree.delete(*self.body.posts_tree.get_children())
            self.recipient = None
        else:
            print("No file path provided. Operation cancelled.")

    def close_profile(self):
        """Current prof is cleared, and UI is reset"""
        self.profile = Profile()
        self.profile_path = None
        self.recipient = None
        self.body._contacts = []
        self.body.posts_tree.delete(*self.body.posts_tree.get_children()) # clear the contact list
        self.body.entry_editor.config(state=tk.NORMAL)
        self.body.entry_editor.delete(1.0, tk.END)
        self.body.entry_editor.config(state=tk.DISABLED)
        self.footer.footer_label.config(text="Profile closed. Please open/create a profile.")
        print("Profile closed. All data cleared from the UI.")

if __name__ == "__main__":
    cleanup()

    main = tk.Tk()

    main.title("ICS 32 Distributed Social Messenger")

    main.geometry("720x480")

    main.option_add('*tearOff', False)

    app = MainApp(main)

    main.update()

    main.minsize(main.winfo_width(), main.winfo_height())

    id = main.after(2000, app.check_new)

    print(id)

    main.mainloop()
