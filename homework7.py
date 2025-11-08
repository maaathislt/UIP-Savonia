import flet as ft
from flet.security import encrypt, decrypt

def main(page: ft.Page):
    page.title = "Home Work 7_UIP_pubsub_LE TEXIER Mathis_s2520833"

    # Here, we create the controls that we will have on our page
    username = ft.TextField(label="Username", width=200, border_color=ft.Colors.WHITE)
    passphrase_field = ft.TextField(
        label="Enter passphrase", password=True, can_reveal_password=True, width=250, border_color=ft.Colors.WHITE
    )
    topic_dropdown = ft.Dropdown(
        label="Select Topic",
        options=[
            ft.dropdown.Option("General"),
            ft.dropdown.Option("UIP Course"),
            ft.dropdown.Option("Savonia Admin"),
            ft.dropdown.Option("Kuopio"),
        ],
        width=200,
        border_color=ft.Colors.WHITE,
    )
    message_field = ft.TextField(label="Type your message", expand=True, border_color=ft.Colors.WHITE)
    chat_display = ft.ListView(expand=True, spacing=10, auto_scroll=True)

    # Send message
    def send_message(e):
        if not passphrase_field.value or not topic_dropdown.value:
            return  # If one the values is missing, the message can't be sent

        encrypted_text = encrypt(message_field.value, passphrase_field.value) # We use the encrypt from flet with the password and the message

        page.pubsub.send_all({
            "user": username.value or "Anonymous",                          #We send the following informations to the pubsub
            "topic": topic_dropdown.value,
            "message": encrypted_text,
        })

        message_field.value = ""
        page.update()

    # Receive message 
    def handle_message(data):
        sender = data.get("user", "Anonymous")
        topic = data.get("topic", "")
        encrypted_text = data.get("message", "")
        decrypted_text = decrypt(encrypted_text, passphrase_field.value)    # We decrypt the text and the password


        if topic == topic_dropdown.value:                                   # If the topix is the same, we display the message with the topic,                                                               
            chat_display.controls.append(                                   # the sender and the message
                ft.Text(f"[{topic}] {sender}: {decrypted_text}", color=ft.Colors.WHITE)
            )
            page.update()

    page.pubsub.subscribe(handle_message)
    send_button = ft.ElevatedButton("Send", on_click=send_message)

    # Layout, we add the controls that we created in the beginning
    page.add(
        ft.Column([
            ft.Row([username, passphrase_field, topic_dropdown]),
            chat_display,
            ft.Row([message_field, send_button]),
        ], expand=True)
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER)