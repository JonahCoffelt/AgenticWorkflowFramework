import customtkinter as ctk
import threading
import framework as fmk

agent = fmk.Agent()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        ctk.set_appearance_mode("dark")

        # Add frames
        padding = 5
        border_radius = 5
        self.left_frame  = ctk.CTkFrame(self, corner_radius=border_radius)
        self.input_frame = ctk.CTkTabview(self.left_frame, corner_radius=border_radius)
        self.agent_frame = ctk.CTkFrame(self.left_frame, corner_radius=border_radius)
        self.right_frame = ctk.CTkFrame(self, corner_radius=border_radius)

        # Pack frames
        self.left_frame.pack(side='left', expand=True, fill='both', padx=padding, pady=padding)
        self.input_frame.pack(side='top', expand=True, fill='both', padx=padding, pady=padding)
        self.agent_frame.pack(side='top', expand=True, fill='both', padx=padding, pady=padding)
        self.right_frame.pack(side='left', expand=True, fill='both', padx=padding, pady=padding)

        # Input Frame
        self.input_frame.add('Send Message')
        self.input_frame.add('Set Resource')
        self.input_frame.add('Get Resource')


        # Messages
        self.message_frame  = ctk.CTkFrame(self.input_frame.tab('Send Message'), corner_radius=border_radius)
        self.message_frame.pack(side='top', expand=False, fill='x', padx=padding, pady=padding)
        self.message_label = ctk.CTkLabel(self.message_frame, anchor='w', font=('Calibri', 15), text=f"Message")
        self.message_label.pack(side='left', expand=False, fill='x', padx=padding, pady=padding)
        self.message_entry = ctk.CTkEntry(self.message_frame, placeholder_text='Enter Message')
        self.message_entry.pack(side='left', expand=True, fill='x', padx=padding, pady=padding)

        self.recivers_frame  = ctk.CTkFrame(self.input_frame.tab('Send Message'), corner_radius=border_radius)
        self.recivers_frame.pack(side='top', expand=False, fill='x', padx=padding, pady=padding)
        self.recivers_label = ctk.CTkLabel(self.recivers_frame, anchor='w', font=('Calibri', 15), text=f"Recivers")
        self.recivers_label.pack(side='left', expand=False, fill='x', padx=padding, pady=padding)
        self.recivers_entry = ctk.CTkEntry(self.recivers_frame, placeholder_text='Enter Recivers')
        self.recivers_entry.pack(side='left', expand=True, fill='x', padx=padding, pady=padding)

        self.message_send_button = ctk.CTkButton(self.input_frame.tab('Send Message'), text="Send", command=self.send_message)
        self.message_send_button.pack()



        # Set Resource
        self.set_key_frame  = ctk.CTkFrame(self.input_frame.tab('Set Resource'), corner_radius=border_radius)
        self.set_key_frame.pack(side='top', expand=False, fill='x', padx=padding, pady=padding)
        self.set_key_label = ctk.CTkLabel(self.set_key_frame, anchor='w', font=('Calibri', 15), text=f"Key")
        self.set_key_label.pack(side='left', expand=False, fill='x', padx=padding, pady=padding)
        self.set_key_entry = ctk.CTkEntry(self.set_key_frame, placeholder_text='Enter Key')
        self.set_key_entry.pack(side='left', expand=True, fill='x', padx=padding, pady=padding)

        self.set_value_frame  = ctk.CTkFrame(self.input_frame.tab('Set Resource'), corner_radius=border_radius)
        self.set_value_frame.pack(side='top', expand=False, fill='x', padx=padding, pady=padding)
        self.set_value_label = ctk.CTkLabel(self.set_value_frame, anchor='w', font=('Calibri', 15), text=f"Value")
        self.set_value_label.pack(side='left', expand=False, fill='x', padx=padding, pady=padding)
        self.set_value_entry = ctk.CTkEntry(self.set_value_frame, placeholder_text='Enter Value')
        self.set_value_entry.pack(side='left', expand=True, fill='x', padx=padding, pady=padding)

        self.set_button = ctk.CTkButton(self.input_frame.tab('Set Resource'), text="Request", command=self.set_resource)
        self.set_button.pack()



        # Get Resource
        self.get_key_frame  = ctk.CTkFrame(self.input_frame.tab('Get Resource'), corner_radius=border_radius)
        self.get_key_frame.pack(side='top', expand=False, fill='x', padx=padding, pady=padding)
        self.get_key_label = ctk.CTkLabel(self.get_key_frame, anchor='w', font=('Calibri', 15), text=f"Key")
        self.get_key_label.pack(side='left', expand=False, fill='x', padx=padding, pady=padding)
        self.get_key_entry = ctk.CTkEntry(self.get_key_frame, placeholder_text='Enter Key')
        self.get_key_entry.pack(side='left', expand=True, fill='x', padx=padding, pady=padding)

        self.get_button = ctk.CTkButton(self.input_frame.tab('Get Resource'), text="Request", command=self.get_resource)
        self.get_button.pack()



        # Agent Frame
        self.agent_frame_title = ctk.CTkLabel(self.agent_frame, anchor='w', font=('Calibri', 30), text=f"Agent Information")
        self.agent_frame_title.pack(side='top', fill='x', padx=padding, pady=padding)
        self.agent_frame_id = ctk.CTkLabel(self.agent_frame, anchor='w', font=('Calibri', 15), text=f"ID: {agent.identifier}")
        self.agent_frame_id.pack(side='top', fill='x', padx=padding, pady=padding)

    def send_message(self):
        """
        Sends a message based on current inputs
        """
        
        agent.send(content=self.message_entry.get(), recivers=[int(rec) for rec in filter(lambda x: x, self.recivers_entry.get().split(' '))])

    def set_resource(self):
        """
        Sends a message based on current inputs
        """

        agent.send(type='tool', content='set resource', data=[self.set_key_entry.get(), self.set_value_entry.get()])

    def get_resource(self):
        """
        Sends a message based on current inputs
        """

        agent.send(type='tool', content='get resource', data=[self.get_key_entry.get()])


    def add_message(self, text):
        """
        Sends a message based on current inputs
        """
        
        padding = 5
        msg = ctk.CTkLabel(self.right_frame, anchor='w', font=('Calibri', 15), text=text)
        msg.pack(side='top', fill='x', padx=padding, pady=padding)

app = App()

while True:
    for event in agent.events:
        if event[0] == 'message':
            app.add_message(str(event[1]))

    agent.events.clear()
    app.update()
