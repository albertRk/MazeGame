import socket
import time

from pynput import keyboard
from network import Network


def on_press(key):
    if key == keyboard.Key.down:
        n.send('0,1')
    if key == keyboard.Key.up:
        n.send('0,-1')
    if key == keyboard.Key.right:
        n.send('1,0')
    if key == keyboard.Key.left:
        n.send('-1,0')

def move(network):
    with keyboard.Listener(
        on_press= on_press) as listener:
        listener.join()

if __name__ == "__main__":

    running = True
    n = Network()
    # initial_position = False

    while running:
        move(n)


