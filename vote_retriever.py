#!/usr/bin/env python

import tkinter as tk
from tkinter import filedialog, simpledialog, Button, Text, Label, StringVar
from tkinter.messagebox import askyesno
import tkinter.scrolledtext as st
import os


class VoteLoader:
    def __init__(self, box: Text, names: list, save_loc: str, votes_list: st.ScrolledText):
        self.box = box
        self.votes = []
        self.names = names
        self.save_loc = save_loc
        self.votes_list = votes_list

    def __call__(self, event):
        txt = self.box.get(1.0, "end-1c")
        self.box.delete(1.0, "end-1c")
        txt = txt[:-1]
        self.votes.append(parse_input(txt, self.names))
        self._update_votes_list()

    def save(self):
        with open(self.save_loc, mode='w') as f:
            f.write("\n".join(self.votes))

    def load(self, file_loc):
        with open(file_loc, mode="r") as f:
            txt = f.read()
            self.votes = txt.split(sep='\n')
        self._update_votes_list()

    def undo(self):
        try:
            self.votes.pop()
            self._update_votes_list()
        except IndexError as e:
            pass

    def _update_votes_list(self):
        self.votes_list.configure(state='normal')
        self.votes_list.delete('1.0', tk.END)
        self.votes_list.insert(tk.INSERT, chars="\n".join(self.votes))
        self.votes_list.configure(state='disabled')


def get_names() -> list:
    """
    Asks for names of candidates
    :return: list of candidates including vacant
    """
    nominees = simpledialog.askinteger("Vote Retriever", "Number of nominees excluding vacant:")
    names = []
    for i in range(nominees):
        name = simpledialog.askstring("Vote Retriever", f'Name of candidate {i + 1}:').replace(" ", "_")
        names.append(name)
    names.sort()
    names.append("Vacant")
    return names


def parse_input(inp: str, names: list) -> str:
    """
    Takes input in index form and converts to raw form (e.g. "01 5" --> "name1,name2 name5")
    :param inp: string in index form
    :param names: List of candidate names
    :return: raw vote string
    """
    indices = "0123456789abcdefghijklmnopqrstuvwxyz"
    raw = ""
    for i, char in enumerate(inp):
        if char == " ":
            raw += " "
        else:
            index = indices.rfind(char)
            if (index >= len(names)) or (index == -1):
                raise ValueError("Input contains index that does not correspond to a candidate or vacant.")

            if (i == len(inp) - 1) or (inp[i+1] == " "):
                sep = ""
            else:
                sep = ","
            raw += f'{names[index]}{sep}'
    return raw


def create_key(names: list) -> str:
    """
    Converts list of names into key used for inputting votes
    :param names: List of candidate names
    :return: String representation of voter name and respective index
    """
    indices = "0123456789abcdefghijklmnopqrstuvwxyz"
    name_key = ""
    for i, name in enumerate(names):
        name_key += f'{indices[i]} - {name}\n'
    return name_key[:-1]


def main():
    window = tk.Tk()
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=3)
    window.columnconfigure(2, weight=1)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=1)
    window.rowconfigure(2, weight=40)

    names = get_names()
    name_key = create_key(names)

    # Determine load and save location
    load = askyesno("Vote parser", "Do you want to load and save to a previously created file?")
    if load:
        file_loc = filedialog.askopenfilename(parent=window,
                                              initialdir=os.getcwd(),
                                              title="Select file to load and save to")
    else:
        directory = filedialog.askdirectory(parent=window,
                                            initialdir=os.getcwd(),
                                            title="Select save directory")
        file_name = simpledialog.askstring("Vote parser", "Save filename (without prefix, e.g. '.txt'):")
        file_loc = f'{directory}/{file_name}.txt'

    # Create jank UI
    key = tk.Label(master=window,
                   text=name_key,
                   anchor="nw",
                   justify="left",
                   background="white",
                   borderwidth=2,
                   relief="solid",
                   font=("Helvetica", 15))
    input_box = Text(master=window,
                     height=len(names),
                     width=20,
                     font=("Helvetica", 15),
                     background="white",
                     borderwidth=2,
                     relief="solid")
    votes_list = st.ScrolledText(master=window,
                                 font=("Helvetica", 15),
                                 background="white",
                                 borderwidth=2,
                                 relief="solid")
    loader = VoteLoader(box=input_box,
                        names=names,
                        save_loc=file_loc,
                        votes_list=votes_list)
    save_button = Button(master=window,
                         command=loader.save,
                         text="Save")
    undo_button = Button(master=window,
                         command=loader.undo,
                         text="Undo")

    window.bind('<Return>', loader)
    key.grid(row=0, column=0, sticky='ew', rowspan=2)
    input_box.grid(row=0, column=1, sticky='ew', rowspan=2)
    save_button.grid(row=0, column=2)
    undo_button.grid(row=1, column=2)
    votes_list.grid(row=2, column=0, columnspan=3, sticky='ew')

    # Load previous votes
    if load:
        loader.load(file_loc)

    window.mainloop()

    # Save before closing
    save = askyesno("Vote parser", "Do you want to save before closing?")
    if save:
        loader.save()

if __name__ == '__main__':
    main()
