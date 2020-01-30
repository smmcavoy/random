import tkinter as tk

class App:
    def __init__(self, master):

        #frame containing listbox and accompanying scrollbar
        console = tk.Frame(master)
        console.pack(side = tk.TOP, fill = tk.X)

        #vertical scrollbar
        scrollbar = tk.Scrollbar(console)
        scrollbar.pack(side = tk.RIGHT, fill=tk.Y)

        #listbox
        self.listbox = tk.Listbox(console, yscrollcommand = scrollbar.set, height = 30)
        self.listbox.pack(fill = tk.BOTH)

        #bind scrollbar to listbox
        scrollbar.config(command=self.listbox.yview)

        #frame containing field for text entry
        frame = tk.Frame(master)
        frame.pack(side = tk.BOTTOM)

        prefix = tk.Label(frame, text = '> ')
        prefix.pack(side = tk.LEFT)

        #field for text entry
        self.field = tk.Entry(frame, width = 60)
        self.field.pack(side = tk.LEFT)
        self.field.bind('<Return>', self.enterText) 


        #necessary? (idk if i want this in here)
        self.enter = tk.Button(frame, text = 'GO', command = self.enterText)
        self.enter.pack(side = tk.LEFT)

    
    def enterText(self, e=None):
        text = ' > '+self.field.get()
        self.listbox.insert(tk.END, text)
        self.listbox.see('end')
        self.field.delete(0, tk.END)

if __name__=='__main__':
    root = tk.Tk()
    a = App(root)
    root.mainloop()
