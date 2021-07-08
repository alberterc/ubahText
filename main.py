from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog, simpledialog, messagebox
import pyperclip




#functions for the 'File' menu
def newFile():      #making a new file
    # global fileName
    if len(texteditorWindow.get('1.0', END+'-1c')) > 0:
        if messagebox.askyesno('Text Editor', 'Do you want to save changes?'):
            saveFile()
    texteditorWindow.delete(0.0, END)      
    mainWindow.title('Text Editor')
def openFile():     #opening an existing file
    chooseFile = filedialog.askopenfile(parent = mainWindow, mode = 'r', filetypes= fileTypes, defaultextension = fileTypes)
    if chooseFile != None:
        readChosenFile = chooseFile.read()
        texteditorWindow.delete(0.0, END)
        texteditorWindow.insert(0.0, readChosenFile)
def saveFile():     #saving a new file
    savePath = filedialog.asksaveasfile(mode = 'w', filetypes= fileTypes, defaultextension = fileTypes)
    if savePath != None:
        newFileData = texteditorWindow.get('1.0', END)
        savePath.write(newFileData)
def saveasFile():   #saving as a new file
    savePath = filedialog.asksaveasfile(mode = 'w', filetypes= fileTypes, defaultextension = fileTypes)
    if savePath != None:
        newFileData = texteditorWindow(0.0, END)
        savePath.write(newFileData.rstrip())
def exitWindow():   #exiting the program
    onWindowClose()

#functions for the 'Edit' menu
def undoEdit():     #undo the last action (typed text)
    try:
        texteditorWindow.edit_undo()
    except TclError:
        pass
def redoEdit():     #redo the last undid action
    try:
        texteditorWindow.edit_redo()
    except TclError:
        pass
def cutEdit():      #cut the selected text into the clipboard
    texteditorWindow.event_generate("<<Cut>>")
def copyEdit():     #copy the selected text into the clipboard
    texteditorWindow.event_generate("<<Copy>>")
def pasteEdit():    #paste from the clipboard (latest data)
    texteditorWindow.event_generate("<<Paste>>")
# def deleteEdit():
#     selectedText = texteditorWindow.selection_get()
#     if len(selectedText) > 0:
#         texteditorWindow.delete(selectedText)
def findEdit():     #find a specific string from the whole text editor window
    texteditorWindow.tag_remove('Found', '1.0', END)
    findWindow = simpledialog.askstring('Find', 'Find what:')
    if findWindow:
        index = '1.0'
        while 1:
            index = texteditorWindow.search(findWindow, index, nocase = 1, stopindex = END)
            if not index:
                break
            lastindex = '%s+%dc' %(index, len(findWindow))
            texteditorWindow.tag_add('Found', index, lastindex)
            index = lastindex
        texteditorWindow.tag_config('Found', foreground = 'white', background = 'blue')
        texteditorWindow.bind('<1>', texteditorWindowVisualReset)    
def selectAll():    #selects/highlights all text in the text editor window
    texteditorWindow.event_generate("<<SelectAll>>")

#function for the 'Help' menu
def aboutHelp():    #shows information about the Text Editor
    label = messagebox.showinfo('About ubahText', 
        'Version 1.0\nubahText is a basic dark themed text editor with simple functions.\n\n\nubahText is created by RadX.')

#mouse and keyboard inputs functions
#used by mouse leftclick
def texteditorWindowVisualReset(event):   #resets the colors or selected text of text editor window after finding the searched string
    texteditorWindow.tag_config('Found', foreground = 'black', background = 'white')
#used by Ctrl+c
def copytext(event):    #copying text function (especially useful for removing newline after every line of text)
    string_in_text_editor_window =  texteditorWindow.get('1.0', END+'-1c')
    if len(string_in_text_editor_window) > 0:
        string_in_text_editor_window.rstrip()
        pyperclip.copy(string_in_text_editor_window)

#additional functions
def onWindowClose():    #when closing window
    if len(texteditorWindow.get('1.0', END+'-1c')) > 0:
        if messagebox.askyesno('Text Editor', 'Do you want to save changes?'):
            saveFile()
    mainWindow.destroy()




#making the main window
mainWindow = Tk()
mainWindow.title('ubahText')
mainWindow.geometry('800x600')
mainWindow.configure(background = '#040720')

#making the window for editing text
texteditorWindow = ScrolledText(mainWindow,
                            width = 80,
                            height = 60,
                            font = ('Consolas', 13),
                            undo = True,
                            )
texteditorWindow.configure(background = '#040720',
                           foreground = 'lightgray',
                           insertbackground = 'white'
                           )

#types of file for filedialog
fileTypes = [('All Files', '*.*'),
             ('Text Documents', '*.txt')]




###################################################################################################
###################################################################################################
##################################MAKING MENUS IN THE MAIN WINDOW##################################
###################################################################################################
###################################################################################################
#making the menus
texteditorMenus = Menu(mainWindow, background = '#040720', foreground = 'lightgray')
mainWindow.configure(menu = texteditorMenus)

#making the 'File' menu
fileMenu = Menu(texteditorMenus, tearoff = False, background = '#040720', foreground = 'lightgray')
texteditorMenus.add_cascade(label = 'File', menu = fileMenu)
#adding submenus in the 'File' menu
fileMenu.add_command(label = 'New', command = newFile)
fileMenu.add_command(label = 'Open...', command = openFile)
fileMenu.add_command(label = 'Save', command = saveFile)
fileMenu.add_command(label = 'Save as...', command = saveasFile)
fileMenu.add_separator()
fileMenu.add_command(label = 'Exit', command = exitWindow)

#making the 'Edit' menu
editMenu = Menu(texteditorMenus, tearoff = False, background = '#040720', foreground = 'lightgray')
texteditorMenus.add_cascade(label = 'Edit', menu = editMenu)
#adding submenus in the 'Edit' menu
editMenu.add_command(label = 'Undo', command = undoEdit)
editMenu.add_command(label = 'Redo', command = redoEdit)
editMenu.add_separator()
editMenu.add_command(label = 'Cut', command = cutEdit)
editMenu.add_command(label = 'Copy', command = copyEdit)
editMenu.add_command(label = 'Paste', command = pasteEdit)
# editMenu.add_command(label = 'Delete', command = deleteEdit)
editMenu.add_separator()
editMenu.add_command(label = 'Find', command = findEdit)
editMenu.add_separator()
editMenu.add_command(label = 'Select All', command = selectAll)

#making the 'Help' menu
helpMenu = Menu(texteditorMenus, tearoff = False, background = '#040720', foreground = 'lightgray')
texteditorMenus.add_cascade(label = 'Help', menu = helpMenu)
#adding submenus in the 'Help' menu
helpMenu.add_command(label = 'About ubahText', command = aboutHelp)
###################################################################################################
###################################################################################################
##################################MAKING MENUS IN THE MAIN WINDOW##################################
###################################################################################################
###################################################################################################




########################################################################################
##################################ADDITIONAL FUNCTIONS##################################
########################################################################################
#uses Ctrl+c to copy texts
mainWindow.bind('<Control-Key-c>', copytext)

#when window closes without pressing the 'Exit' option in the 'File' menu
mainWindow.protocol('WM_DELETE_WINDOW', onWindowClose)
########################################################################################
##################################ADDITIONAL FUNCTIONS##################################
########################################################################################




texteditorWindow.pack(fill = BOTH, expand = YES)
mainWindow.mainloop()
