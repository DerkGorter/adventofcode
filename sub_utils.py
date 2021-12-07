def convert_movement_instruction(instruction: str) -> tuple:
    if 'up' in instruction:
        x = int(instruction.replace('up ', ''))
        return 'aim', -x
    elif 'down' in instruction:
        x = int(instruction.replace('down ', ''))
        return 'aim', x
    elif 'forward' in instruction:
        x = int(instruction.replace('forward ', ''))
        return 'horizontal', x
