from tkinter import *
import socket
import threading
from select import select
import json

s = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

HOST = '192.168.0.4'  # Your IP
PORT = 9999           # Your Port

with open("settings.json") as f:
    data = json.load(f)
f.close()

my_json2 = '>>>>>>{"name": "%s", "rank": "%s"}' % (data['NAME'], data['RANK'])
connected_list = []
NAME = data['NAME']
s.connect((HOST, PORT))
s.send(my_json2.encode("utf-8"))


def check_for_message():
    while True:
        r, w, e = select([s], [], [], 0.01)
        if r:
            d = s.recv(1024)
            d_decoded = d.decode("utf-8")
            print(d_decoded)
            if d_decoded.startswith(">>>>>>"):
                d_decoded = d_decoded.replace(">>>>>>", "")
                connected_list, msg = d_decoded.split("|")
                connected_list = connected_list[1:-1].replace("u'", "").replace("'", "").split(", ")
                if len(connected_list[-1]) > 6:
                    connected_list[-1] = [x[:6] for x in connected_list]
                print(connected_list)
                put_received_messages_list(msg)
                delete_list_box()
                enter_list_box(connected_list)
            elif d_decoded.startswith("<<<<<<"):
                d_decoded = d_decoded.replace("<<<<<<", "")
                connected_list, msg = d_decoded.split("|")
                connected_list = connected_list[1:-1].replace("u'", "").replace("'", "").split(", ")
                if len(connected_list[-1]) > 6:
                    connected_list = ["{}...".format(x[:6]) for x in connected_list]
                print(connected_list)
                delete_list_box()
                put_received_messages_list(msg)
                enter_list_box(connected_list)
            else:
                got_message = d_decoded
                put_received_messages_list(got_message)


def put_received_messages_list(y):
    inputget = "{}".format(y)
    txt.configure(state='normal')
    txt.insert(END, "{}\n".format(inputget))
    txt.yview(END)
    txt.configure(state='disabled')


def enter_list_pressed(event):
    input_get = input_field.get()
    txt.configure(state='normal')
    txt.insert(END, "{}: {}\n".format(NAME, input_get))
    txt.yview(END)
    txt.configure(state='disabled')
    input_user.set('')
    s.send("{}: {}".format(NAME, input_get).encode("utf-8"))
    return "break"


def enter_list_box(event):
    for i in event:
        listbox.insert(END, i)


def delete_list_box():
    listbox.delete(0, END)


window = Tk()
window.title(NAME)
listbox = Listbox(window, width=10, height=10)
listbox.pack(side='right', fill='y')
txt_frm = Frame(window, width=450, height=300)
txt_frm.pack(fill="both", expand=False)
txt_frm.grid_propagate(False)
txt_frm.grid_rowconfigure(0, weight=1)
txt_frm.grid_columnconfigure(0, weight=1)
txt = Text(txt_frm, borderwidth=3, relief="sunken")
txt.config(font=("consolas", 10), undo=True, wrap='word', state='disabled')
txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
scrollb = Scrollbar(txt_frm, command=txt.yview)
scrollb.grid(row=0, column=1, sticky='nsew')
txt['yscrollcommand'] = scrollb.set
input_user = StringVar()
input_field = Entry(window, text=input_user)
input_field.pack(side=BOTTOM, fill=X)
input_field.bind("<Return>", enter_list_pressed)
t = threading.Thread(target=check_for_message)
t.daemon = True
t.start()
window.mainloop()
s.close()
