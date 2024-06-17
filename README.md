# enigma-simulator
# Background
Having just recently re-watched The Imitation Game during my summer break, I set about trying to simulate Enigma using my insane "button mashing and praying to God it works" skills. The movie aside, I have been a 
**world history** enthusiast for a long time (and by world, I mean Europe and by history, I mean WW2). The machine itself was a fantastic bit of engineering and it had the smartest mathematicians in the world scratching their heads trying to crack it.
This project itself, is dedicated to the Polish cryptologists, **Marian Rejewski, Henryk Zygalski** and **Jerzy Rozycki** (who cracked Enigma first and worked with Bletchley Park during the war), and the great **Alan Turing** himself. For more information on its history, click [here](https://en.wikipedia.org/wiki/Enigma_machine#History).
<br>
<p align = "center"><img src = "https://github.com/rghanty/enigma-simulator/assets/99227180/89d4e9f5-3aa4-4af8-938b-dc892c8f0570"></p>
<p align = "center"><i>Jimmy James describes himself. Source: NewsRadio 1995</i></p> 

# Machine Design
On a real-life enigma machine, there are **four** key components visible to a user working on the machine.<p align = "right"><img src = "https://github.com/rghanty/enigma-simulator/assets/99227180/0f890e77-b6ab-452a-a77e-bb23bbf84648"></p><p align = "center"><i>
Source: Wikipedia: Cryptanalysis of the Enigma</i></p> 

- The rotors are responsible for directing and jumbling electrical signals from the keyboard yielding a **different** output letter from the input letter. 
- The keyboard takes in user input.
- The lampboard has letters which light up based on the output produced by the enigma machine.
- The plugboard is used to swap a letter for another one. If say "A" and "R" are connected on the plugboard. The signal for the letter "A" will become that for "R" before traveling to the rotors, and vice versa.


Vis-a-vis this, I created classes `rotor.py`, `plugboard.py` and `enigma.py`. The first two files contain logic for accepting, forwarding and backwarding signals to neighbouring rotors or the plugboard. `enigma.py` consolidates this logic and creates an overall workflow from input to output. <br><br>
A component **not** visible to the user is the **Reflector**. The reflector is nothing but a rotor that accepts a signal and forwards it to itself, thereby *reflecting* the signal before sending it back to the rotors.
<br><br> On each click of the keyboard, the rightmost rotor advances once. Upon reaching its turnover point, it activates the neighboring rotor. Each rotor has a different turnover point. For more information, check out its [design](https://en.wikipedia.org/wiki/Enigma_machine#Design) and [operation](https://en.wikipedia.org/wiki/Enigma_machine#Operation).
<br><br>

# The Simulator
This program simulates an [Enigma I](https://www.cryptomuseum.com/crypto/enigma/i/) machine used by the Wehrmacht before and during WWII.<br>
Upon running the file `gui.py`. You will be greeted with this window. (fullscreen)![image](https://github.com/rghanty/enigma-simulator/assets/99227180/bfdbfd75-8418-4091-82ae-41374a579244) The components of this window are (from top-bottom, left-right):

- **Configure Enigma (button)**: Use this button to set rotor, reflector and plugboard settings. You can only use the enigma machine after configuring it using this button.
- **Input (label)**: What you type on the keyboard will appear here.
- **Output (label)**: The output of the enigma machine will appear here.
- **Reset (button)**: Using this button will reset the rotors back to their original position and clear the input and output.
- **Lampboard**: Respective letters will light up depending on the output of the machine.
- **Keyboard**: This will display what keys you are using.

Upon using the Configure Enigma button, you will encounter this window.![image](https://github.com/rghanty/enigma-simulator/assets/99227180/de960ce5-6583-4c40-a6ee-260272f16ebf)<br> You similarly have:

- Three drop-down menus for rotor selection with options "I","II","III","IV","V" based on historic enigma rotor wirings. All three rotors must be unique.
- Reflector selection with options "A","B","C" based on historic reflector wirings.
- A space for entering plugboard pairs. You can enter at most 10 pairs of unique letters.
- A button for applying configuration.

When you apply your selected configuration to the machine, you will be taken back to the enigma machine ui, with a slight change. You will find three vertical rectangles used to visualise the rotors you selected. Each rotor has letters going from A-Z and will rotate upon typing in a letter. The updated window is as follows with the selected rotors being "I","III","V". ![image](https://github.com/rghanty/enigma-simulator/assets/99227180/0fc19c1b-a107-4949-9bf5-6f7172a9637e)
<br><br>

# Historical Rotor Wirings
| Rotor/Reflector # | Wiring | Turnover Notch
|-------------------|----------------------------------|---------------|
| I                 | EKMFLGDQVZNTOWYHXUSPAIBRCJ       |Q              |
| II                | AJDKSIRUXBLHWTMCQGZNPYFVOE       |E              |
| III               | BDFHJLCPRTXVZNYEIWGAKMUSQO       |V              |
| IV                | ESOVPZJAYQUIRHXLNFTGKDCMWB       |J              |
| V                 | VZBRGITYUPSDNHLXAWMJQOFECK       |Z              |
| Reflector A       | EJMZALYXVBWFCRQUONTSPIKHGD       |N/A            |
| Reflector B       | YRUHQSLDPXNGOKMIEBFZCWVJAT       |N/A            |
| Reflector C       | FVPJIAOYEDRZXWGCTKUQSBNMHL       |N/A            |

Source: https://en.wikipedia.org/wiki/Enigma_rotor_details


# Demo
Here is a brief demonstration of the machine. Make sure to read the entire README file before watching this to understand the specifics of the machine!!!.



https://github.com/rghanty/enigma-simulator/assets/99227180/8484124b-619f-4c0a-ac5c-c3e77413f6a1

<br><br>
If you have any questions or concerns, do let me know in Issues!! 
<br><br>


