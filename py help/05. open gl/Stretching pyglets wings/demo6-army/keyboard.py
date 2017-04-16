key_handlers = {}

def on_key_press(symbol, modifiers):
    if symbol in key_handlers:
        key_handlers[symbol]()

