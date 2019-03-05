""" This is the code module of CND."""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

__author__ = "1966bc aka giuseppe costanzi"
__copyright__ = "Copyleft"
__credits__ = ["hal9000",]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "beta 1"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "2019-03-4"
__status__ = "Production"

class Dialog(tk.Toplevel):     
    def __init__(self, parent, *args, **kwargs):
        super().__init__(name='code')

        self.transient(parent)
        self.resizable(0,0)
        self.parent = parent
        self.engine = kwargs['engine']
        self.index = kwargs['index']

        self.letter = tk.StringVar()
        self.category = tk.StringVar()
        self.cnd = tk.StringVar()
        self.description = tk.StringVar()
        self.level =  tk.IntVar()
        self.terminal = tk.StringVar()
        self.engine.center_me(self)
        self.init_ui()

    def init_ui(self):

        w = self.engine.get_init_ui(self)

        r =0
        ttk.Label(w, text="Letter:",).grid(row=r, sticky=tk.W)
        self.txtLetter = ttk.Entry(w, textvariable=self.letter)
        self.txtLetter.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Category:").grid(row=r, sticky=tk.W)
        self.txtCategory = ttk.Entry(w, textvariable=self.category)
        self.txtCategory.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="CND:").grid(row=r, sticky=tk.W)
        self.txtCND = ttk.Entry(w, textvariable=self.cnd)
        self.txtCND.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Description:").grid(row=r, sticky=tk.W)
        self.txtDescription = ttk.Entry(w, textvariable=self.description)
        self.txtDescription.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Level:").grid(row=r, sticky=tk.W)
        self.txtLevel = ttk.Entry(w, textvariable=self.level)
        self.txtLevel.grid(row=r, column=1, padx=5, pady=5)

        r +=1
        ttk.Label(w, text="Terminal:").grid(row=r, sticky=tk.W)
        self.txtTerminal = ttk.Entry(w, textvariable=self.terminal)
        self.txtTerminal.grid(row=r, column=1, padx=5, pady=5)
        
        self.engine.get_save_cancel(self, w)
       
    def on_open(self, selected_code=None):

        if self.index is not None:
            self.selected_code = selected_code
            msg = "Update  %s" % (self.selected_code[3],)
            self.set_values()
        else:
            msg = "Insert new"
            

        self.title(msg)
        self.txtCategory.focus()

    def on_save(self, evt):

        if self.engine.on_fields_control(self)==False:return
        if messagebox.askyesno(self.engine.title, self.engine.ask_to_save, parent=self) == True:

            args =  self.get_values()

            if self.index is not None:

                sql = self.engine.get_update_sql('codes','code_id')
                args = (*args, self.selected_code[0])
                       
            else:
                sql = self.engine.get_insert_sql('codes',len(args))

            self.engine.write(sql,args)
            self.parent.on_branch_selected()

            if self.index is not None:
                self.parent.lstCodes.see(self.index)
                self.parent.lstCodes.selection_set(self.index)
                    
            self.on_cancel()
            
    def get_values(self,):

        return (self.letter.get(),
                self.category.get(),
                self.cnd.get(),
                self.description.get(),
                self.level.get(),
                self.terminal.get())
    
    def set_values(self,):

        self.letter.set(self.selected_code[1])
        self.category.set(self.selected_code[2])
        self.cnd.set(self.selected_code[3])
        self.description.set(self.selected_code[4])
        self.level.set(self.selected_code[5])
        self.terminal.set(self.selected_code[6])

    def on_cancel(self, evt=None):
        self.destroy()        
