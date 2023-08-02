import socket
import time
import tkinter as tk
import threading

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = tk.Tk()
chat_frame = tk.Frame(window)
text_box = tk.Text(chat_frame, height=40, width=80, pady=10, padx=10)
chat_frame.pack()
text_box.pack()
text_box.insert(tk.END, 'Hello!')


def check_for_ping():
    text = irc.recv(2040)
    text_box.insert(tk.END, "\n"+text.decode())

    if text.find('PING'.encode()) != -1:
        irc.send(('PONG ' + text.split(":".encode())[1].decode()).encode())


def update_chat():
    while 1:
        check_for_ping()


server = "irc.libera.chat"
channel = "#bot-test"
nick = "nonerroneousname414132"

print("connecting to: "+server)
irc.connect((server, 6667))
irc.send(("NICK " + nick + "\n").encode())
check_for_ping()
irc.send(("USER " + nick + " 0 * :" + nick + "\n").encode())
check_for_ping()
time.sleep(8)
irc.send(("JOIN " + channel + "\n").encode())

textEnter = tk.Entry(window, width=24)
textEnter.pack()
textEnter.place(anchor='center', relx=0.5, rely=0.9)
button = tk.Button(window, bd=5, text="Send", command=lambda: [irc.send(("PRIVMSG " + channel + " :" + textEnter.get() + "\r\n").encode()),
                                                               text_box.insert(tk.END, "\n"+nick+": "+textEnter.get()),
                                                               textEnter.delete(0, 'end')])
button.pack()
button.place(anchor='center', relx=0.70, rely=0.9)

window.update_idletasks()
thread = threading.Thread(target=update_chat)
thread.start()
window.after(200, button.invoke)  # prevents needing to press button twice (bug?)
window.geometry("800x800")
window.mainloop()
