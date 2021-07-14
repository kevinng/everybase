from chat.tasks.send_confirm_interests import send_confirm_interests

def run():
    send_confirm_interests(
        2,
        seller_only=True
    )