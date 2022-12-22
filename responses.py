import random

def get_response(message: str) -> str:
    p_message = message.lower()

    if p_message == 'hello':
        return 'Hey there.'

    if p_message == 'roll':
        return str(random.randint(1,6))

    if p_message == 'introon':
        return 'Your intro was turned on.'

    if p_message == 'introoff':
        return 'Your intro was turned off.'

    if p_message == '!help':
        return "`This is a help message that you can modify.`"