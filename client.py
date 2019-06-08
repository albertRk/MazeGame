import socket
import time

from pygame.locals import Color
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

def move():
    with keyboard.Listener(
        on_press= on_press) as listener:
        listener.join()

if __name__ == "__main__":

    running = True
    n = Network()
    nickname = input("Tell me your name: ")
    n.send(nickname)
    while True:
        try:
            color = input("choose color: ")
            Color(color)
            break
        except ValueError:
            pass
    n.send(color)
    while running:
        move()


