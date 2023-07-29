import socket
import sys
import time
import tkinter as tk
import threading

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = tk.Tk()


def check_for_ping():
    text = irc.recv(2040)
    print(text.decode())

    if text.find('PING'.encode()) != -1:
        irc.send(('PONG ' + text.split(":".encode())[1].decode()).encode())


def update_chat():
    while 1:
        check_for_ping()


server = "irc.freenode.org"
channel = "#chat"
botnick = "nonerroneousnickname4523"
password = ""

print("connecting to: "+server)
irc.connect((server, 6667))
irc.send(("NICK " + botnick + "\n").encode())
check_for_ping()
irc.send(("USER " + botnick + " 0 * :" + botnick + "\n").encode())
check_for_ping()
time.sleep(5)
irc.send(("JOIN " + channel + "\n").encode())

textEnter = tk.Entry(window)
textEnter.pack()
button = tk.Button(window, bd=5, text="Send", command=lambda: irc.send(("PRIVMSG " + channel + " :" + textEnter.get() + "\r\n").encode()))
button.pack()

window.update_idletasks()
thread = threading.Thread(target=update_chat)
thread.start()
window.after(1, button.invoke)  # prevents needing to press button twice (bug?)
window.mainloop()
