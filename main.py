from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import time
import tkinter as tk
import threading

mouse_controller = MouseController()
keyboard_controller = KeyboardController()

class MacroRecorder:
    def __init__(self):
        self.keyboard_data = []
        self.mouse_data = []
        self.start_time = time.time()
        self.root = tk.Tk()
        self.root.geometry('100x100+0+0')  # Kleines Fenster in der oberen linken Ecke

    def on_click(self, x, y, button, pressed):
        if pressed:
            click_time = time.time() - self.start_time
            self.mouse_data.append(('click', x, y, button, click_time))

    def on_key(self, key, pressed):
        if pressed:
            key_time = time.time() - self.start_time
            self.keyboard_data.append(('key', key, key_time))

    def start_recording(self, duration):
        self.start_time = time.time()
        with MouseListener(on_click=self.on_click) as self.mouse_listener, KeyboardListener(on_press=self.on_key) as self.keyboard_listener:
            self.root.after(int(duration * 1000), self.root.quit)  # Beendet die Aufnahme nach der angegebenen Dauer
            self.root.mainloop()
            self.mouse_listener.stop()
            self.keyboard_listener.stop()

    def play_recording(self, iterations):
        for _ in range(iterations):
            for action, x_or_key, y_or_time, button_or_none, click_or_none in sorted(self.mouse_data + self.keyboard_data, key=lambda x: x[4]):
                time.sleep(click_or_none - (time.time() - self.start_time))
                if action == 'click':
                    mouse_controller.position = (x_or_key, y_or_time)
                    mouse_controller.click(button_or_none)
                elif action == 'key':
                    keyboard_controller.press(x_or_key)
                    keyboard_controller.release(x_or_key)

if __name__ == "__main__":
    recorder = MacroRecorder()
    duration = float(input("Wie lange wird ein Durchgang der Aufnahme dauern (in Sekunden)? "))
    iterations = int(input("Wie viele Durchgänge sollen aufgezeichnet werden? "))
    recorder.start_recording(duration)
    recorder.play_recording(iterations)
