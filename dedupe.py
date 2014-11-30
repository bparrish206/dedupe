=============
import csv
import wx
import os

#set file types to open
wildcard = "CSV files (*.csv)|*.csv|"      \
           "All files (*.*)|*.*"           \

#create a holder for files selected
master = []

class AppLogic(object):
    def file_open(self, filename="default_name"):
        print "Open a file: "
        print "I'd be opening file: %s now"%filename

    def file_close(self):
        print "Close a file: "
        print "I'd be closing a file now"

#create main form
class MainForm(wx.Panel):
    def __init__(self, *args, **kwargs):
        self.dirname=''
        wx.Panel.__init__(self, *args, **kwargs)

        #set font types
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)

        #creat buttons and labels
        theButton1 = wx.Button(self, label="1st File")
        theButton1.Bind(wx.EVT_BUTTON, self.onButton)
        theButton1.SetBackgroundColour('orchid')
        theButton1.SetFont(font2)

        label1 = wx.StaticText(self, label="Select 1st file:")
        label1.SetForegroundColour('white')
        label1.SetFont(font)

        theButton2 = wx.Button(self, label="2nd File")
        theButton2.Bind(wx.EVT_BUTTON, self.onButton)
        theButton2.SetBackgroundColour('orchid')
        theButton2.SetFont(font2)

        theButton3 = wx.Button(self, label="Dedupe files")
        theButton3.Bind(wx.EVT_BUTTON, self.onDedupe)
        theButton3.SetBackgroundColour('pale green')
        theButton3.SetFont(font2)

        label2 = wx.StaticText(self, label="Select 2nd file:")
        label2.SetForegroundColour('white')
        label2.SetFont(font)

        label11 = wx.StaticText(self, label="You selected these files:")
        label11.SetForegroundColour('white')
        label11.SetFont(font)
        self.outTextControl1 = wx.TextCtrl(self, style=wx.TE_READONLY)

        label3 = wx.StaticText(self, label="The duplicate records are:")
        label3.SetForegroundColour('white')
        label3.SetFont(font)
        self.outTextControl = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        #set button and label positions
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(label1, 0, wx.ALIGN_LEFT | wx.TOP, 4)
        buttonSizer.Add(theButton1, 0, wx.GROW | wx.ALL, 4)
        buttonSizer.Add(label2, 0, wx.ALIGN_LEFT | wx.TOP, 4)
        buttonSizer.Add(theButton2, 0, wx.GROW | wx.ALL, 4)
        buttonSizer.Add(label11, 1, wx.ALIGN_LEFT | wx.TOP, 5)
        buttonSizer.Add(self.outTextControl1, 0, wx.GROW | wx.ALL,4)
        buttonSizer.Add(theButton3, 0, wx.GROW | wx.ALL, 4)
        buttonSizer.Add(label3, 0, wx.ALIGN_LEFT | wx.TOP, 4)
        buttonSizer.Add(self.outTextControl, 5, wx.EXPAND | wx.ALL, 4)

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add((5,5), 5)
        mainSizer.Add(buttonSizer, 5, wx.ALIGN_TOP)
        mainSizer.Add((5,5), 5)

        self.SetBackgroundColour('slate blue')
        self.SetSizer(mainSizer)

    #set up buttons to open files
    def onButton(self, evt=None):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname, self.filename), 'r')
            master.append(f)
            display = []
            display.append(self.filename)
            for i in display:
                self.outTextControl1.write(i +',')
            return f
            f.close()
        dlg.Destroy()

    #run loops over to files selected, display duplicates and create a new file of all unique records
    def onDedupe(self, evt=None):
        first = [row for row in master[0]]
        second = [row2 for row2 in master[1]]
        name = []
        dupes = []
        name.insert(0, first[0])
        name += [i for i in first if i not in second]
        name += [x for x in second if x not in first]
        dupes += [k for k in first if k in second]
        dupes.remove(dupes[0])
        for z in dupes:
            self.outTextControl.write(z+'\n')
        newFile=csv.writer(open('newFile.csv', 'wb'), delimiter=',')
        for b in name:
            newFile.writerow(b.strip().split(','))
        print "You now have a newFile that contains all the unique records between these two files."

class TestFrame(wx.Frame):
    def __init__(self, app_logic, *args, **kwargs):
        kwargs.setdefault('title', "The DEDUPER!!!")
        wx.Frame.__init__(self, size=wx.Size(600,400), *args, **kwargs)

        self.app_logic = app_logic
        self.buttonPanel = MainForm(self)

        menuBar = wx.MenuBar()

        fileMenu = wx.Menu()
        openMenuItem = fileMenu.Append(wx.ID_ANY, "&Open", "Open a file" )
        self.Bind(wx.EVT_MENU, self.onOpen, openMenuItem)

        closeMenuItem = fileMenu.Append(wx.ID_ANY, "&Close", "Close a file" )
        self.Bind(wx.EVT_MENU, self.onClose, closeMenuItem)

        exitMenuItem = fileMenu.Append(wx.ID_EXIT, "Exit", "Exit the application" )
        self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)
        menuBar.Append(fileMenu, "&File")

        helpMenu = wx.Menu()
        helpMenuItem = helpMenu.Append(wx.ID_HELP, "Help", "Get help" )
        menuBar.Append(helpMenu, "&Help")

        self.SetMenuBar(menuBar)

    def onOpen(self, evt=None):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir= os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "I'd opening a file in onOpen ", path
            self.app_logic.file_open( path )
        else :
            print "The file dialog was canceled before anything was selected"

        dlg.Destroy()

    def onClose(self, evt=None):
        print "close menu selected"
        self.app_logic.file_close()

    def onExit(self, evt=None):
        print "Exit the program here"
        print "The event passed to onExit is type", type(evt),
        self.Close()

class TestApp(wx.App):
    def OnInit(self):
        app_logic = AppLogic()
        f = TestFrame(app_logic, parent=None)
        f.Show()

        return True

if __name__ == "__main__":

        app = TestApp(False)
        app.MainLoop()
