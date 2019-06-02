import socket
import time

from pynput import keyboard
from network import Network


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def on_press(key):
    if key == keyboard.Key.down:
        n.send('0,1')
    if key == keyboard.Key.up:
        n.send('0,-1')
    if key == keyboard.Key.right:
        n.send('1,0')
    if key == keyboard.Key.left:
        n.send('-1,0')
    # else:
    #     n.send('0,0')

def move(network):
    cords = ''
    with keyboard.Listener(
        on_press= on_press) as listener:
        listener.join()
    # try:
    # if keyboard.pressed("a"):
    #     cords = '1,0'
    #
        initial_position = True
    #
    # if keyboard.pressed("b"):
    #     cords = '-1,0'
    #
        initial_position = True
    #
    # if keyboard.pressed("c"):
    #     cords = '0,1'

        # initial_position = True

    # if keyboard.pressed("d"):
    #     cords = '0,-1'

        # initial_position = True

    # print(cords)
    # n.send(cords + ',red')


if __name__ == "__main__":

    running = True
    n = Network()
    # n.connect()
    # n.getPlayerNumber()
    # initial_position = False

    while running:
        # pass
        # n.send('100,100,red')
        move(n)


