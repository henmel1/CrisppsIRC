import tkinter as tk

message = "penis"

window = tk.Tk()
textEnter = tk.Entry()
button = tk.Button(bd = 5, text="Send", command =lambda: print(message))
textEnter.pack()
button.pack()
window.mainloop()
