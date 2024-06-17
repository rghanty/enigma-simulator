from tkinter import *
from tkinter.ttk import *
from rotor import Rotor
from enigma import EnigmaMachine
from plugboard import Plugboard
from tkinter import messagebox
import pygame

# Create the main application window
root = Tk()
icon = PhotoImage(file="media/enigma.png")
root.title("Enigma Simulator")
root.iconphoto(False, icon)
root.geometry("1000x800")

root.configure(bg='black')
canvas_width = 1000
canvas_height = 800
pygame.mixer.init()
click_sound = pygame.mixer.Sound('media/click.wav')
advance_sound = pygame.mixer.Sound('media/wind-up.wav')

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


def draw_keys(start_x, start_y, circle_radius, padding_x, padding_y, outline_color, fill_color, text_color, store_shapes, is_lampboard):
    # Positions for the circles (10-9-7 per line layout)
    border_width = 3
    if is_lampboard:
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
reset_label = Label(root, text=" Reset", font=('Lucida Console', 11), foreground='#DDDDDD', background='#333333', relief='solid', width=7)
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
            play_click_sound()
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
            if output_enigma_key in lamp_shapes:
                oval, text = lamp_shapes[output_enigma_key]
                canvas.itemconfig(oval, fill='#FFFF99')  # Off-white yellow glow
                canvas.itemconfig(text, fill='#333333')
            play_click_sound()

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
            play_advance_sound()
        output_enigma_key = None

        

def configure_enigma():
    def apply_configuration():
        rotor_settings = [rotor_vars[i].get() for i in range(3)]
        # plugboard_settings = plugboard_entry.get().split()

        plugboard_input = plugboard_entry.get().strip().upper()  # Convert to uppercase
        plugboard_settings = [plugboard_input[i:i+2] for i in range(0, len(plugboard_input), 3)]
        
        if len(set(rotor_settings)) < 3:
            messagebox.showerror("Error", "Please select 3 unique rotors.")
            return
        
        for pair in plugboard_settings:
            if len(pair) != 2 or not pair.isalpha() or pair[0] == pair[1]:
                messagebox.showerror("Error", f"Invalid plugboard pair: {pair}.")
                return
        
        if len(plugboard_settings) > 10:
            messagebox.showerror("Error", "Too many plugboard pairs. Maximum is 10 pairs.")
            return
        
        combined = "".join(plugboard_settings)
        seen = ""
        for i in combined:
            if i not in seen:
                seen+=i
            else:
                messagebox.showerror("Error","Cannot use the same letter " + i + " in different pairs")
                return
        
        
        reflector_type = reflector_var.get()

        global enigma
        enigma = EnigmaMachine(
            Plugboard(plugboard_settings),
            Rotor(rotor_settings[0], reflector_type, canvas, 350, rotor_start_y, rotor_width, rotor_height),
            Rotor(rotor_settings[1], reflector_type, canvas, 350 + (rotor_width + padding), rotor_start_y, rotor_width, rotor_height),
            Rotor(rotor_settings[2], reflector_type, canvas, 350 + 2 * (rotor_width + padding), rotor_start_y, rotor_width, rotor_height),
            Rotor(0, reflector_type, None, 0, 0, 0, 0)
        )

        
        config_window.destroy()
        config_label.destroy()

    config_window = Toplevel(root)
    config_window.title("Configure Enigma Machine")
    config_window.iconphoto(False,icon)
    config_window.geometry("400x400")

    rotor_label = Label(config_window, text="Select Rotors:", font=('Helvetica', 12))
    rotor_label.pack(pady=10)

    rotor_choices = ["I", "II", "III", "IV", "V"]
    rotor_vars = [StringVar(value=rotor_choices[i]) for i in range(3)]
    rotor_comboboxes = [Combobox(config_window, textvariable=rotor_vars[i], values=rotor_choices, state="readonly") for i in range(3)]

    for combobox in rotor_comboboxes:
        combobox.pack(pady=5)

    reflector_label = Label(config_window, text="Select Reflector:", font=('Helvetica', 12))
    reflector_label.pack(pady=10)

    reflector_var = StringVar(value="A")
    reflector_combobox = Combobox(config_window, textvariable=reflector_var, values=["A", "B", "C"], state="readonly")
    reflector_combobox.pack(pady=5)

    plugboard_label = Label(config_window, text="Plugboard Pairs (e.g., AB CD EF or ab cd ef):", font=('Helvetica', 12))
    plugboard_label.pack(pady=10)

    plugboard_entry = Entry(config_window, font=('Helvetica', 12))
    plugboard_entry.pack(pady=5)

    apply_button = Button(config_window, text="Apply Configuration", command=apply_configuration)
    apply_button.pack(pady=20)

    config_window.grab_set()

    # Initialize the rotor menus



def play_click_sound():
    click_sound.play()

def play_advance_sound():
    advance_sound.play()


# Configuration label to open Enigma configuration
def on_config_label_click(event):
    config_label.config(background='#AAAAAA')

def on_config_label_release(event):
    config_label.config(background='#333333')
    configure_enigma()
    

config_label = Label(root, text=" Configure Enigma", font=('Lucida Console', 12), foreground='white', background='grey', relief='solid', width=18)
config_label.place(x=canvas_width/2+50, y=20)
config_label.bind("<Button-1>", on_config_label_click)
config_label.bind("<ButtonRelease-1>", on_config_label_release)

draw_keyboard()
draw_lampboard()

# Bind the key press and key release events
root.bind('<KeyPress>', on_key_press)

root.bind('<KeyRelease>', on_key_release)

# Start the Tkinter event loop
root.mainloop()
