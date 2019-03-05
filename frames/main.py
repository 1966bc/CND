""" This is the main module of CND."""
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from engine import Engine
import frames.code

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "beta 1"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-03-4"
__status__ = "Production"


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__()

        self.engine = kwargs['engine']
    
        self.master.protocol("WM_DELETE_WINDOW",self.on_exit)
        self.objs = []
        self.status_bar_text = tk.StringVar()
    
        self.set_icon()
        self.set_title()
        self.center_ui()
        self.init_menu()
        self.init_ui()
        self.set_style()
        self.init_status_bar()

    def set_style(self):
        self.master.style = ttk.Style()
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
        self.master.style.theme_use("clam")
        self.master.style.configure('.', background=self.engine.get_rgb(240,240,237))
        self.lstCodes.tag_configure('is_terminal', background=self.engine.get_rgb(255,160,122))

    def set_icon(self):
        imgicon = tk.PhotoImage(file=os.path.join('icons','home.png'))
        self.master.call('wm', 'iconphoto', self.master._w, '-default', imgicon)

    def set_title(self):
        s = "{0}".format(self.engine.title,)
        self.master.title(s)
           
    def init_menu(self):

        m_main = tk.Menu(self, bd=1)
               
        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        s_menu = tk.Menu(m_file)
                
        m_about = tk.Menu(m_main, tearoff=0, bd=1)
        
        m_main.add_cascade(label="File", underline=0, menu=m_file)
        m_main.add_cascade(label="?", underline=0, menu=m_about)

        m_file.add_separator()
 
        m_file.add_command(label="Exit", underline=0, command=self.on_exit)

        m_about.add_command(label="About", underline=0, command=self.on_about)

        self.master.config(menu=m_main)      


    def center_ui(self):

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # calculate position x, y
        d = self.engine.get_dimensions()
        w = int(d['w'])
        h = int(d['h'])
        x = (ws/2) - (w/2)    
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))     
        

    def init_status_bar(self):

        self.status = tk.Label(self.master,
                            textvariable=self.status_bar_text,
                            bd=1,
                            relief=tk.SUNKEN,
                            anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_bar_text.set(__version__)

    def init_ui(self):

        """create widgets"""

        self.pack(fill=tk.BOTH, expand=1)

        
        f0 = self.engine.get_frame(self, 8)

        f1 = tk.Frame(f0,)

        cols = (["#0",'','w',True,300,300],
                 ["#1",'','w',True,0,0],)
        
        self.Categories = self.engine.get_tree(f1, cols, show="tree")
        self.Categories.show="tree"
        self.Categories.pack(fill=tk.BOTH, padx=2, pady=2)
        self.Categories.bind("<<TreeviewSelect>>", self.on_branch_selected)
        f1.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)

        f2 = tk.Frame(f0,)
        
        self.lblCodes = ttk.LabelFrame(f2,text='Products',)

        cols = (["#0",'id','w',False,0,0],
                      ["#1",'CND','w',True,100,100],
                      ["#2",'Description','w',True,200,200],
                      ["#3",'L','w',True,20,20],
                      ["#4",'T','w',True,20,20],)
        
        self.lstCodes = self.engine.get_tree(self.lblCodes, cols,)
        self.lstCodes.bind("<<TreeviewSelect>>", self.get_selected_code)
        self.lstCodes.bind("<Double-1>", self.on_double_click)
        self.lblCodes.pack(fill=tk.BOTH, expand=1)

        f2.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        
     
        f3 = self.engine.get_frame(self, 8)

        bts = (('Reset', self.on_open),
               ('New', self.on_add),
               ('Edit', self.on_edit),
               ('Close', self.on_exit))

        for btn in bts:
            self.engine.get_button(f3, btn[0] ).bind("<Button-1>", btn[1])

        f3.pack(side=tk.RIGHT, fill=tk.Y, expand=0)
        
        f0.pack(fill=tk.BOTH, expand=1)
     
    def on_open(self, evt=None):

        self.lblCodes['text'] = 'Codes 0'
        self.selected_code = None
        sql = "SELECT code_id, letter, category FROM codes WHERE level=1"
        rs = self.engine.read(True, sql, ())
        if rs:
            self.set_values(rs)
        
    def set_values(self, rs):

        for i in self.Categories.get_children():
            self.Categories.delete(i)

        for i in self.lstCodes.get_children():
            self.lstCodes.delete(i)            

        #.insert(parent, index, iid=None, **kw)
        self.Categories.insert('', 0, 0, text='Categories')

        for i in rs:
            categories = self.Categories.insert("",
                                                tk.END,
                                                iid=i[0],
                                                text=i[2], values=(i[1],'categories'))
            branches = self.load_second_branch(i[1])
            if branches is not None:
                for branch in branches:
                    self.Categories.insert(categories,
                                           tk.END,
                                           iid=branch[0],
                                           text=branch[2],
                                           values=(branch[1],'branches'))

    def load_second_branch(self, i):

        sql = "SELECT code_id,cnd, description \
               FROM codes\
               WHERE cnd LIKE ?\
               AND  level=2"

        args = (i+"%",)
        
        return self.engine.read(True, sql, args)


    def on_branch_selected(self, evt=None):

        selected_item = self.Categories.focus()

        d = self.Categories.item(selected_item)

        if d['values']:
            if d['values'][1]=='branches':

                pk = d['values'][0]

                sql = "SELECT code_id, cnd,description,level,terminal\
                       FROM codes\
                       WHERE  cnd LIKE ?\
                       AND  level >3"
                
                args = (pk+"%",)
            
                self.set_codes(sql, args)

    def get_selected_code(self, evt):

        if self.lstCodes.focus():
            pk = int(self.lstCodes.item(self.lstCodes.focus())['text'])
            self.selected_code = self.engine.get_selected('codes', 'code_id', pk)
                
    def set_codes(self, sql, args):

        for i in self.lstCodes.get_children():
            self.lstCodes.delete(i)
        
        rs = self.engine.read(True, sql, args)

        if rs:
            self.lblCodes['text'] = 'Codes %s'%len(rs)
            for i in rs:
                if i[4]!='N':
                    self.lstCodes.insert('',
                                         tk.END,
                                         iid=i[0],
                                         text=i[0],
                                         values=(i[1],i[2],i[3],i[4]),
                                         tags = ('is_terminal',))
                else:
                    self.lstCodes.insert('',
                                         tk.END,
                                         iid=i[0],
                                         text=i[0],
                                         values=(i[1],i[2],i[3],i[4]))
                        

        else:
            self.lblCodes['text'] = 'Codes 0'                
        
    def on_add(self, evt):

        obj = frames.code.Dialog(self, engine=self.engine, index=None)
        obj.on_open()
                   
    def on_edit(self, evt):
        
        if self.lstCodes.focus():

            item_iid = self.lstCodes.selection()
            obj = frames.code.Dialog(self, engine=self.engine, index=item_iid)
            obj.on_open(self.selected_code,)
            
        else:
            msg = "Please select an item."
            messagebox.showwarning(self.engine.title,msg, parent=self)

    def on_double_click(self, evt):

        self.on_edit(self)
 
             
    def on_about(self,):
        messagebox.showinfo(self.engine.title, self.engine.about, parent=self)   
        
    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.engine.title, "Do you want to quit?", parent=self):
            self.master.destroy()

      
def main():
    root = tk.Tk()
    app = App(root, engine=Engine())
    app.on_open()
    root.mainloop()
  
if __name__ == '__main__':
    main()
