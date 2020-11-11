import tkinter as tk
from tkinter import ttk
import sqlite3

class Main( tk.Frame ) :
    def __init__( self, root ) :
        super().__init__( root )
        self.init_main()
        self.db = db
        self.view_records()

    def init_main( self ) :
        toolbar = tk.Frame( bg='#d7d8e0', bd=2 )
        toolbar.pack( side=tk.TOP, fill=tk.X )

        btn_open_dialog = tk.Button( toolbar, text='Добавить вопрос', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP )
        btn_open_dialog.pack( side=tk.LEFT )

        btn_edit_dialog = tk.Button( toolbar, text='Редактировать вопрос', command=self.open_update_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP )
        btn_edit_dialog.pack( side=tk.LEFT )

        btn_delete = tk.Button( toolbar, text='Удалить вопрос', command=self.delete_records, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP )
        btn_delete.pack( side=tk.LEFT )

        self.tree = ttk.Treeview( self, columns=( 'ID', 'question', 'type' ), height=15, show='headings' )

        self.tree.column( 'ID', width=30, anchor=tk.CENTER )
        self.tree.column( 'question', width=470, anchor=tk.CENTER )
        self.tree.column( 'type', width=150, anchor=tk.CENTER )

        self.tree.heading( 'ID', text='ID' )
        self.tree.heading( 'question', text='Вопрос' )
        self.tree.heading( 'type', text='Тип Выборка/Поле' )

        self.tree.pack()

    def records( self, question, type ):
        self.db.insert_data( question, type )
        self.view_records()

    def update_records( self, question, type ) :
        self.db.c.execute( '''UPDATE survey SET question=?, type=? WHERE ID=?''', 
                         ( question, type, self.tree.set( self.tree.selection()[0], '#1' ) ) )
        self.db.conn.commit()
        self.view_records()

    def view_records( self ) :
        self.db.c.execute( '''SELECT * FROM survey''' )
        [ self.tree.delete(i) for i in self.tree.get_children() ]
        [ self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall() ]

    def delete_records( self ) :
        for selection_item in self.tree.selection() :
            self.db.c.execute( '''DELETE FROM survey WHERE id=?''', ( self.tree.set( selection_item, '#1' ), ) )
        self.db.conn.commit()
        self.view_records()

    def open_dialog( self ) :
        Child()

    def open_update_dialog( self ) :
        Update()


class Child( tk.Toplevel ) :
    def __init__( self ):
        super().__init__( root )
        self.init_child()
        self.view = app

    def init_child( self ) :
        self.title( 'Добавить вопрос' )
        self.iconbitmap( r"img/icon.ico" )
        self.geometry( '400x220+400+300' )
        self.resizable( False, False )

        label_question = tk.Label( self, text='Вопрос:' )
        label_question.place( x=50, y=50 )
        label_select = tk.Label( self, text='Тип Выборка/Поле:' )
        label_select.place( x=50, y=80 )

        self.entry_question = ttk.Entry( self )
        self.entry_question.place( x=200, y=50 )

        self.combobox = ttk.Combobox( self, values=[ u'Выборка', u'Поле' ] )
        self.combobox.current( 0 )
        self.combobox.place( x=200, y=80 )

        btn_cancel = ttk.Button( self, text='Закрыть', command=self.destroy )
        btn_cancel.place( x=300, y=170 )

        self.btn_ok = ttk.Button( self, text='Добавить' )
        self.btn_ok.place( x=220, y=170 )
        self.btn_ok.bind( '<Button-1>', lambda event: self.view.records( self.entry_question.get(),
                                                                         self.combobox.get() ) )

        self.grab_set()
        self.focus_set()

class Update( Child ) :
    def __init__( self ) :
        super().__init__()
        self.init_edit()
        self.view = app

    def init_edit( self ) :
        self.title( 'Редактировать вопрос' )
        btn_edit = ttk.Button( self, text = "Редактировать" )
        btn_edit.place( x = 205, y = 170 )
        btn_edit.bind( '<Button-1>', lambda event: self.view.update_records( self.entry_question.get(),
                                                                            self.combobox.get() ) )
        
        self.btn_ok.destroy()


class DB:
    def __init__(self) :
        self.conn = sqlite3.connect('survey.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS survey (id integer primary key, question text, type text)''')
        self.conn.commit()

    def insert_data( self, question, type ) :
        self.c.execute( '''INSERT INTO survey(question, type) VALUES (?, ?)''',
                       ( question, type ) )
        self.conn.commit()


if __name__ == "__main__" :
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("SurveyBot")
    root.iconbitmap( r"img/icon.ico" )
    root.geometry("640x420+300+200")
    root.resizable(False, False)
    root.mainloop()