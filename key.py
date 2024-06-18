from tkinter import ttk
from database import load_api_key, save_api_key, delete_api_key

# Function to show the last 4 digits of the API key
def display_censored_key(api_key):
    if len(api_key) > 4:
        return '*' * (len(api_key) - 4) + api_key[-4:]
    else:
        return api_key
    
# Function to save the API key and update the label
def save_key_and_update_label(api_key_input, api_key_label_semi_hidden):
    api_key = api_key_input.get()
    save_api_key(api_key)
    censored_key = display_censored_key(api_key)
    api_key_label_semi_hidden.config(text=f"Your API Key: {censored_key}")

# Function to delete API key from the database
def delete_api_key_from_db():
    delete_api_key()
    update_api_key_label(None)

# Function to update the API key label
def update_api_key_label(api_key):
    if api_key:
        api_key_label_semi_hidden.config(text=f"Your API Key: {'*' * (len(api_key) - 4) + api_key[-4:]}")
    else:
        api_key_label_semi_hidden.config(text="Your API Key: None")

# Create a API Key Frame
def apikey_frame(api_key_tab):
    global api_key_input, api_key_label_semi_hidden
    api_key_frame = ttk.Frame(api_key_tab)
    api_key_frame.grid(row=0, column=0, sticky="n", padx=10, pady=10)

    api_key_header = ttk.Label(api_key_frame, text="Instructions to gain and enter your own Steam API Key")
    api_key_header.configure(font=("Helvetica", 15, "bold underline"))
    api_key_header.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    api_key_step1 = ttk.Label(api_key_frame, text="1. Go to https://steamcommunity.com/dev/apikey and create an API Key. Enter anything as domainname. It doesn't matter.")
    api_key_step1.grid(row=1, column=0, sticky="w", padx=10, pady=10)

    api_key_step2 = ttk.Label(api_key_frame, text="2. Copy your API Key and enter it below.")
    api_key_step2.grid(row=2, column=0, sticky="w", padx=10, pady=10)

    api_key_input = ttk.Entry(api_key_frame)
    api_key_input.grid(row=3, column=0, sticky="w", padx=10, pady=10)

    api_key_input_button = ttk.Button(api_key_frame, text="Use this API Key", command=lambda: save_key_and_update_label(api_key_input, api_key_label_semi_hidden))
    api_key_input_button.grid(row=3, column=0, sticky="w", padx=200, pady=10)

    api_key_label_semi_hidden = ttk.Label(api_key_frame, text="Your API Key:")
    api_key_label_semi_hidden.grid(row=4, column=0, sticky="w", padx=10, pady=10)

    api_key_delete_button = ttk.Button(api_key_frame, text="Delete current API Key", command=delete_api_key_from_db)
    api_key_delete_button.grid(row=4, column=0, sticky="w", padx=300, pady=10)

    api_key_step2 = ttk.Label(api_key_frame, text="3. Restart SAM+. Enjoy Unlocking.")
    api_key_step2.grid(row=5, column=0, sticky="w", padx=10, pady=10)

    # Display the last saved API key on startup
    saved_key = load_api_key()
    if saved_key:
        api_key_label_semi_hidden.config(text=f"Your API Key: {display_censored_key(saved_key)}")