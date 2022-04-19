import pynput.keyboard as keyboard
import clipboard
import zono.Queue
import time
import threading
import tkinter
import signal



signal.signal(signal.SIGTRAP,lambda x,y:x)

guichangeevent = threading.Event()
root = None
clipboard_q = zono.Queue.Queue(30)


def onselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    clipboard.copy(value)

def copyP():
    try:
        i  = root.lstwidget.curselection()[0]
        clipboard.copy(root.lstwidget.get(i))
    except Exception as e:
        print(e)


def create_window():
    root = tkinter.Tk()
    root.title('clipboard')
    lstwidget = tkinter.Listbox(root,width=40)
    lstwidget.pack()
    for i in clipboard_q:
        lstwidget.insert('end',i)

    lstwidget.bind('<Double-1>', onselect)
    tkinter.Button(root,text='copy',command=copyP).pack()
    root.lstwidget = lstwidget
    return root

def copy():
    time.sleep(0.01)
    paste = clipboard.paste()
    clipboard_q.append(paste)
    if root:
        root.lstwidget.insert('end',paste)


def menu():
    global root
    if not root:
        guichangeevent.set()



shortcuts = {
'<cmd>+c':copy,
'<cmd>+.':menu
}


keyboard.GlobalHotKeys(shortcuts).start()

while True:
    guichangeevent.wait()
    guichangeevent.clear()

    root = create_window()


    root.mainloop()

    root = None





 