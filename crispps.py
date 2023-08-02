import socket
import time
import tkinter as tk
import threading

server = "irc.libera.chat"
channel = "#bot-test"
nick = "nonerroneousname414132"

# create irc socket and chat feed frame
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
window = tk.Tk()
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
chat_frame = tk.Frame(window)
text_box = tk.Text(chat_frame, pady=10, padx=10, cursor="arrow")
text_box.bind("<Key>", lambda e: "break")
chat_frame.grid(row=0, column=0, columnspan=4, sticky='nswe')
text_box.pack(expand=True, fill='both')


def format_text(text):
    try:
        n1 = text.index('!')
        n2 = text.index('#')
    except:
        n2 = -1
    if n2 > -1:
        name = text[1:n1]
        message = text[n2+len(channel)+2:]
        if 'JOIN' in text[n1:n2]:
            return name+' joined.'
        else:
            return name + ': ' + message
    elif '!' in text and 'QUIT' in text:
        return text[1:text.index('!')] + ' disconnected.'
    else:
        return text


def check_for_ping():
    text = irc.recv(2040)
    text_box.insert(tk.END, "\n"+format_text(text.decode()))
    text_box.see("end")  # autoscroll to latest message

    if text.find('PING'.encode()) != -1:
        irc.send(('PONG ' + text.split(":".encode())[1].decode()).encode())


def update_chat():
    while 1:
        check_for_ping()


def connect_to_channel():
    text_box.insert(tk.END, "connecting to: "+server)
    irc.connect((server, 6667))
    irc.send(("NICK " + nick + "\n").encode())
    check_for_ping()
    irc.send(("USER " + nick + " 0 * :" + nick + "\n").encode())
    check_for_ping()
    time.sleep(8)
    irc.send(("JOIN " + channel + "\n").encode())


# connect to the given server and channel
connect_to_channel()

# create and format chat entry and send button
textEnter = tk.Entry(window)
button = tk.Button(window, bd=5, text="Send", command=lambda: [irc.send(("PRIVMSG " + channel + " :" + textEnter.get() + "\r\n").encode()),
                                                               text_box.insert(tk.END, "\n"+nick+": "+textEnter.get()),
                                                               text_box.see("end"),
                                                               textEnter.delete(0, 'end')])
textEnter.bind("<Return>", (lambda event: button.invoke()))  # allows user to hit enter to send message
textEnter.grid(row=1, column=0, sticky='ew')
button.grid(row=1, column=1, sticky='w')

# start main window and start updating chat
window.update_idletasks()
thread = threading.Thread(target=update_chat)
thread.start()
window.after(200, button.invoke)  # prevents needing to press button twice (bug?)
window.title("CrisppsIRC")
window.mainloop()
