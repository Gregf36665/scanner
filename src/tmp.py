from tkinter import *
from tkinter import ttk

top = Tk()

tree = ttk.Treeview(top, columns=('widgets', 'size'))
tree.insert('', 'end', text='Listbox', values=('15KB Yesterday mark'))

tree.insert('', 'end', text='button', tags=('ttk', 'simple'))
tree.tag_configure('ttk', background='yellow')
tree.tag_bind('ttk', '<1>', itemClicked)  # the item clicked can be found via tree.focus()

tree.pack()
def helloCallBack():
	text=StringVar()
	text.set((tree.focus()))
	tkMessageBox.showinfo( "Title", text.get()) 
	

B = Button(top, text ="Select", command = helloCallBack)

B.pack()


top.mainloop()
