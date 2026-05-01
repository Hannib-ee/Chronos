from pynput import mouse
from pynput import keyboard
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import time
import tkinter as tk
import threading

window = tk.Tk()
window.title("Chronos")

actions = []
replaying = False
mouse_controls = MouseController()
keyboard_control = KeyboardController()

def on_move(x, y):
    print(f"mouse moved to ({x}, {y})")
    actions.append(("move", x, y, time.time()))

def on_click(x, y, button, pressed):
    print(f"{button} {pressed} at ({x}, {y})")
    actions.append(("click", x, y, button, pressed, time.time()))


def on_press(button):
    print(f"{button} pressed")
    if button == keyboard.Key.esc:
        return False
    actions.append(("press", button, time.time()))

def start_recording():
    actions.clear()
    with mouse.Listener(on_click=on_click, on_move=on_move) as listener:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
    record_button.config(state="normal")

    print(actions)

def replay():
    while replaying:
        previous_time = actions[0][-1]
        for action in actions:                                                           
            current_time = action[-1]
            pause_time = current_time - previous_time
            time.sleep(pause_time)
            if action[0] == "move":
                mouse_controls.position = (action[1],action[2])
            elif action[0] == "click":
                if action[4] == True:
                    mouse_controls.press(action[3])
                else:
                    mouse_controls.release(action[3])
            elif action[0] == "press":
                keyboard_control.press(action[1])
                keyboard_control.release(action[1])

            previous_time = current_time
            if not replaying:
                break

def start_recording_thread():
    thread = threading.Thread(target = start_recording)
    thread.start()
    record_button.config(state="disabled")

def replay_thread():
    global replaying
    if not replaying:
        replaying = True
        thread = threading.Thread(target = replay)
        thread.start()

def stop_replay():
    global replaying
    replaying = False

def on_activate():
    stop_replay()
    print("Replay Stopped")

hotkey = keyboard.GlobalHotKeys({
    '<ctrl>+<shift>+s': on_activate
})
hotkey.start()

record_button = tk.Button(window, text = "Record", command = start_recording_thread)
replay_button = tk.Button(window, text = "Replay", command = replay_thread)
stop_button = tk.Button(window, text = "Stop", command = stop_replay)


record_button.pack()
replay_button.pack()
stop_button.pack()
window.mainloop()

