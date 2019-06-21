
from pynput import keyboard
from network import Network

# funckja wysyła ruch do servera
def on_press(key):
    if key == keyboard.Key.down:
        n.send('0,1')
    if key == keyboard.Key.up:
        n.send('0,-1')
    if key == keyboard.Key.right:
        n.send('1,0')
    if key == keyboard.Key.left:
        n.send('-1,0')
    if key == keyboard.Key.esc:
        n.send('0,0')
        global running
        running = False

#  funckja nasłuchująca klawaiture
def move():
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":

    running = True
    n = Network()
    nickname = input("Tell me your name: \n ")
    n.send_without_respond(nickname)
    while running:
        move()
