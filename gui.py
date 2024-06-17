from tkinter import *
from tkinter.ttk import *
from rotor import Rotor
from enigma import EnigmaMachine
from plugboard import Plugboard

# Create the main application window
root = Tk()
icon = PhotoImage(file="media/enigma.png")
root.title("Enigma Simulator")
root.iconphoto(False, icon)
root.geometry("1000x800")
root.configure(bg='black')
canvas_width = 1000
canvas_height = 800

# Create a canvas for the keyboard layout
canvas = Canvas(root, width=canvas_width, height=canvas_height, bg='black', highlightthickness=0)
canvas.pack()

# Dictionary to store the keys' shapes references for keyboard and lampboard
key_shapes = {}
lamp_shapes = {}

# Variable to track currently pressed key
current_key_pressed = None
label_width = 20
# Labels for input and output above the rotors
input_label = Label(root, text="I: ", font=('Helvetica', 14), foreground='lightgreen', background='black', relief='solid', width=label_width)
input_label.place(x=canvas_width/2-100, y=60)

output_label = Label(root, text="O: ", font=('Helvetica', 14), foreground='yellow', background='black', relief='solid', width=label_width)
output_label.place(x=canvas_width/2+150, y=60)

# Initialize Enigma machine components
rotor_start_y = 150
rotor_width = 50
rotor_height = 150
padding = 20
r1 = Rotor("I", "A", canvas, 350, rotor_start_y, rotor_width, rotor_height)
r2 = Rotor("II", "A", canvas, 350 + (rotor_width + padding), rotor_start_y, rotor_width, rotor_height)
r3 = Rotor("III", "A", canvas, 350 + 2 * (rotor_width + padding), rotor_start_y, rotor_width, rotor_height)
pb = Plugboard(["AR", "GK", "OX"])
ref = Rotor(0, "A", None, 0, 0, 0, 0)
rotors = [r1, r2, r3]
enigma = EnigmaMachine(pb, r1, r2, r3, ref)

def draw_keys(start_x, start_y, circle_radius, padding_x, padding_y, outline_color, fill_color, text_color, store_shapes, is_lampboard):
    # Positions for the circles (10-9-7 per line layout)
    border_width = 3
    if (is_lampboard):
        border_width = 1
    positions = [
        (start_x + i * (2 * circle_radius + padding_x), start_y) for i in range(10)
    ] + [
        (start_x + (circle_radius + padding_x / 2) + i * (2 * circle_radius + padding_x), start_y + circle_radius * 2 + padding_y) for i in range(9)
    ] + [
        (start_x + 1.5 * (2 * circle_radius + padding_x) + i * (2 * circle_radius + padding_x), start_y + 2 * (circle_radius * 2 + padding_y)) for i in range(7)
    ]

    # Draw circles for the alphabet keys
    alphabet = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    for i, (x, y) in enumerate(positions):
        oval = canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius,
                                  outline=outline_color, fill=fill_color, width=border_width)
        text = canvas.create_text(x, y, text=alphabet[i], font=('Helvetica', 12), fill=text_color)
        store_shapes[alphabet[i]] = (oval, text)

def draw_keyboard():
    # Constants for positioning and sizing
    global circle_radius
    global padding_y
    keyboard_bottom_y = 750
    circle_radius = 15
    padding_x = 30
    padding_y = 20
    start_x = 170
    start_y = keyboard_bottom_y - 3 * (circle_radius * 2 + padding_y)

    # Draw keyboard keys
    draw_keys(start_x, start_y, circle_radius, padding_x, padding_y, '#DDDDDD', '#333333', 'white', key_shapes, False)
    global backspace_x
    global backspace_y
    # Draw backspace rectangle
    backspace_x = start_x + 9.5 * (2 * circle_radius + padding_x) + padding_x / 2
    backspace_y = start_y
    backspace_rect = canvas.create_rectangle(backspace_x, backspace_y - circle_radius, backspace_x + 2 * circle_radius + 2 * padding_x,
                                             backspace_y + circle_radius, outline='#DDDDDD', fill='#333333', width=3)
    backspace_text = canvas.create_text(backspace_x + circle_radius + padding_x, backspace_y, text='Backspace', font=('Helvetica', 12), fill='white')
    key_shapes['Backspace'] = (backspace_rect, backspace_text)

    # Draw space rectangle
    space_x = start_x + 0.5 * (2 * circle_radius + padding_x)
    space_y = start_y + 3 * (circle_radius * 2 + padding_y)
    space_rect = canvas.create_rectangle(space_x, space_y - circle_radius, space_x + 8 * (2 * circle_radius + padding_x),
                                         space_y + circle_radius, outline='#DDDDDD', fill='#333333', width=3)
    space_text = canvas.create_text(space_x + 4 * (2 * circle_radius + padding_x), space_y, text='Space', font=('Helvetica', 16), fill='white')
    key_shapes['Space'] = (space_rect, space_text)

    

def draw_lampboard():
    # Constants for positioning and sizing
    lampboard_bottom_y = 550
    circle_radius = 15
    padding_x = 30
    padding_y = 20
    start_x = 170
    start_y = lampboard_bottom_y - 3 * (circle_radius * 2 + padding_y)

    # Draw lampboard keys
    draw_keys(start_x, start_y, circle_radius, padding_x, padding_y, '#333333', '#111111', '#444444', lamp_shapes, True)

def reset_enigma(event=None):
    input_label.config(text="I: ")
    output_label.config(text="O: ")
    enigma.reset()

def on_reset_label_click(event):
    reset_label.config(background='#AAAAAA')
    

def on_reset_label_release(event):
    reset_label.config(background='#333333')
    reset_enigma()

# Reset label
reset_label = Label(root, text="     Reset", font=('Helvetica', 11), foreground='#DDDDDD', background='#333333', relief='solid', width=10)
reset_label.place(x=canvas_width/2+400, y=60)
reset_label.bind("<Button-1>", on_reset_label_click)
reset_label.bind("<ButtonRelease-1>", on_reset_label_release)


def on_key_press(event):
    global current_key_pressed
    global output_enigma_key
    key = event.keysym.upper()
    if key == 'BACKSPACE':
        key = 'Backspace'
    elif key == 'SPACE':
        key = 'Space'
    if current_key_pressed is None:
        if key in key_shapes:
            oval, text = key_shapes[key]
            canvas.itemconfig(oval, fill='#777777')
            canvas.itemconfig(text, fill='#333333')
        # if key in lamp_shapes:
        #     oval, text = lamp_shapes[key]
        #     canvas.itemconfig(oval, fill='#FFFF99')  # Off-white yellow glow
        #     canvas.itemconfig(text, fill='#333333')
        current_key_pressed = key

        # Handle input updates in the label
        if key == 'Backspace':
            current_input = input_label.cget("text")
            if current_input != "I: ":
                updated_input = current_input[:-1]  # Remove last character
                input_label.config(text=updated_input)
            
            current_output = output_label.cget("text")
            if current_output != "O: ":
                updated_output = current_output[:-1]  # Remove last character
                output_label.config(text=updated_output)
        
        elif key == 'Space':
            input_label.config(text=input_label.cget("text") + " ")
            output_label.config(text=output_label.cget("text") + " ")
            event.widget.focus_set()  # Ensure the canvas retains focus
            return "break"  # Prevent the event from propagating further
        
        elif key.isalpha():  # Only process alphabet characters
            current_input = input_label.cget("text")
            if len(current_input) >= label_width:
                current_input = current_input[1:]  # Limit to 15 characters, remove oldest character
            input_label.config(text=current_input + key)

            # Feed the input key to the Enigma machine and update the output label
            output_key = enigma.encipher(key)
            current_output = output_label.cget("text")
            if len(current_output) >= label_width:
                current_output = current_output[1:]  # Limit to 15 characters, remove oldest character
            output_label.config(text=current_output + output_key)
            output_enigma_key = output_key
            if output_key in lamp_shapes:
                oval, text = lamp_shapes[output_key]
                canvas.itemconfig(oval, fill='#FFFF99')  # Off-white yellow glow
                canvas.itemconfig(text, fill='#333333')
            
        
            # Advance the rotors

def on_key_release(event):
    global current_key_pressed
    global output_enigma_key
    key = event.keysym.upper()
    if key == 'BACKSPACE':
        key = 'Backspace'
    elif key == 'SPACE':
        key = 'Space'
    if key == current_key_pressed:
        if key in key_shapes:
            oval, text = key_shapes[key]
            canvas.itemconfig(oval, fill='#333333')
            canvas.itemconfig(text, fill='white')
        current_key_pressed = None
        if output_enigma_key in lamp_shapes:
            oval, text = lamp_shapes[output_enigma_key]
            canvas.itemconfig(oval, fill='#111111')  # Darker color for lampboard
            canvas.itemconfig(text, fill='#444444')

        output_enigma_key = None


draw_keyboard()
draw_lampboard()

# Bind the key press and key release events
root.bind('<KeyPress>', on_key_press)
root.bind('<KeyRelease>', on_key_release)

# Start the Tkinter event loop
root.mainloop()
