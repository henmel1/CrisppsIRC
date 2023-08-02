import socket
import time
import tkinter as tk
import threading
import random

server = "irc.libera.chat"
port = 6667
channel = "#bot-test"
nick = "guestuser" + str(random.randrange(0, 99999, 1))
live = True

# create irc socket, main window and chat feed frame
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = tk.Tk()
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
chat_frame = tk.Frame(window)
text_box = tk.Text(chat_frame, pady=10, padx=10, cursor="arrow")
text_box.bind("<Key>", lambda e: "break")
chat_frame.grid(row=0, column=0, columnspan=4, sticky='nswe')
text_box.pack(expand=True, fill='both')


# allows reset of socket connection
def change_socket():
    global irc
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc = new_socket


def format_text(text):
    n1 = -1  # avoid reference of n1 before assignment
    try:
        n1 = text.index('!')
        n2 = text.index('#')
    except:
        n2 = -1
    if n2 > -1:
        name = text[1:n1]
        message = text[n2 + len(channel) + 2:]
        if 'JOIN' in text[n1:n2]:
            return name + ' joined.'
        else:
            return name + ': ' + message
    elif '!' in text and 'QUIT' in text:
        return text[1:text.index('!')] + ' disconnected.'
    else:
        return text


def check_for_ping():
    text = irc.recv(2040)
    text_box.insert(tk.END, "\n" + format_text(text.decode()))
    text_box.see("end")  # autoscroll to latest message

    if text.find('PING'.encode()) != -1:
        irc.send(('PONG ' + text.split(":".encode())[1].decode()).encode())


def update_chat():
    while live:
        check_for_ping()


def set_live(t):
    global live
    live = t


# create thread to update chat
thread = threading.Thread(target=update_chat)

# create and format chat entry and send button
text_enter = tk.Entry(window)
send_button = tk.Button(window, bd=5, text="Send", command=lambda: [
    irc.send(("PRIVMSG " + channel + " :" + text_enter.get() + "\r\n").encode()),
    text_box.insert(tk.END, "\n" + nick + ": " + text_enter.get()),
    text_box.see("end"),
    text_enter.delete(0, 'end')])
text_enter.bind("<Return>", (lambda event: send_button.invoke()))  # allows user to hit enter to send message
text_enter.grid(row=1, column=0, sticky='ew')
send_button.grid(row=1, column=1, sticky='w')


def connect_to_channel(s, p, c, n):
    text_box.insert(tk.END, "\nconnecting to: " + s)
    irc.connect((s, p))
    irc.send(("NICK " + n + "\n").encode())
    check_for_ping()
    irc.send(("USER " + n + " 0 * :" + n + "\n").encode())
    check_for_ping()
    time.sleep(8)
    irc.send(("JOIN " + c + "\n").encode())


# connect to the given server and channel
connect_to_channel(server, port, channel, nick)


# create settings window and menu
def open_settings():
    settings = tk.Tk()
    settings.title("Settings")
    warning_label = tk.Label(settings, fg="#fc1900", text="*WARNING* Please only change values" +
                                                          "\nif you know what you are doing." +
                                                          "\nInvalid changes may result in a" +
                                                          "\nprogram failure.")
    nick_entry = tk.Entry(settings)
    nick_label = tk.Label(settings, text="Nick: ")
    server_entry = tk.Entry(settings)
    server_label = tk.Label(settings, text="Server: ")
    port_entry = tk.Entry(settings)
    port_label = tk.Label(settings, text="Port: ")
    channel_entry = tk.Entry(settings)
    channel_label = tk.Label(settings, text="Channel: ")

    def change_nick():
        global nick
        nick = nick_entry.get()

    apply_button = tk.Button(settings, bd=5, text="Apply", command=lambda: [
        set_live(False),
        change_socket(),
        change_nick(),
        connect_to_channel(server_entry.get(), int(port_entry.get()), channel_entry.get(), nick_entry.get()),
        settings.destroy(),
        set_live(True)])
    warning_label.grid(row=0, columnspan=2, sticky='ew')
    nick_label.grid(row=1, column=0)
    nick_entry.grid(row=1, column=1)
    server_label.grid(row=2, column=0)
    server_entry.grid(row=2, column=1)
    port_label.grid(row=3, column=0)
    port_entry.grid(row=3, column=1)
    channel_label.grid(row=4, column=0)
    channel_entry.grid(row=4, column=1)
    apply_button.grid(row=5)


# start updating chat on new thread
thread.start()

# create settings button
settings_button = tk.Button(window, text="Settings", command=open_settings)
settings_button.grid(row=1, column=2, sticky='w')

# initialize and start main window
window.update_idletasks()
window.after(200, send_button.invoke)  # prevents needing to press button twice (bug?)
window.title("CrisppsIRC")
window.mainloop()
