from tkinter import Frame, Label, CENTER, messagebox
import constants as c
import logic as l
import json
import threading
import random
import time


class Game(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title('2048')
        self.master.bind('<Key>', self.key_down)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grid_rows = []
        self.pprev, self.prev = [], [0]
        self.master.wm_attributes('-topmost', 1)
        self.command = {c.KEY_DOWN: l.down, c.KEY_LEFT: l.left, c.KEY_RIGHT: l.right, c.KEY_UP: l.up}
        self.init_grid()
        self.init_matrix()
        self.update_grid()
    
    def init_grid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR, width=c.size / 2, height=c.size / 2)
        background.grid()
        
        for i in range(c.GRID_LEN):
            grid_row = []
            for j in range(c.GRID_LEN):
                cell = Frame(background, bg=c.BACKGROUND_EMPTY_CELL_COLOR, width=c.size // c.GRID_LEN,
                             height=c.size // c.GRID_LEN)
                cell.grid(row=i, column=j, padx=c.GRID_PADDING, pady=c.GRID_PADDING)
                
                t = Label(cell, text='', bg=c.BACKGROUND_EMPTY_CELL_COLOR, justify=CENTER, font=c.FONT, width=3,
                          height=1)
                t.grid()
                grid_row.append(t)
            self.grid_rows.append(grid_row)
    
    def restart(self):
        for i in range(len(self.grid_rows)):
            for j in range(len(self.grid_rows)):
                self.grid_rows[i][j].configure(text='', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
        self.init_matrix()
        self.update_grid()
    
    def init_matrix(self):
        box = messagebox.askquestion('Start a new game?', 'Sure?')
        if box == 'yes':
            self.matrix = l.new_game(c.GRID_LEN)
            self.matrix = l.gen(self.matrix)
            self.matrix = l.gen(self.matrix)
        else:
            
            with open('gamestate.text', 'r', encoding='utf-8') as f:
                t = f.read()
                if not t:
                    self.matrix = l.new_game(c.GRID_LEN)
                    self.matrix = l.gen(self.matrix)
                    self.matrix = l.gen(self.matrix)
                else:
                    self.matrix = json.loads(t)
    
    def update_grid(self):
        for i in range(c.GRID_LEN):
            for j in range(c.GRID_LEN):
                new_num = self.matrix[i][j]
                
                if new_num == 0:
                    self.grid_rows[i][j].configure(text='', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                else:
                    self.grid_rows[i][j].configure(text=str(new_num), bg=c.BACKGROUND_COLOR_DICT[new_num],
                                                   fg=c.CELL_COLOR_DICT[new_num])
        
        self.update_idletasks()
    
    def key_down(self, event):
        key = repr(event.char)
        if key in self.command:
            self.matrix, done = self.command[key](self.matrix)
            if done:
                self.matrix = l.gen(self.matrix)
                self.update_grid()
                done = False
                if l.game_state(self.matrix, c.winnum) == 'win':
                    self.grid_rows[1][1].configure(text='You', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    self.grid_rows[1][2].configure(text='Win', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    c.winnum *= 2
                if l.game_state(self.matrix, c.winnum) == 'lose':
                    self.grid_rows[1][1].configure(text='You', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    self.grid_rows[1][2].configure(text='lose', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    box = messagebox.askquestion('Restart?', 'Sure?')
                    if box == 'yes':
                        self.restart()
                    else:
                        self.master.destroy()
    
    def auto_key_down(self, key):
        key = '\'' + key + '\''
        if key in self.command:
            self.matrix, done = self.command[key](self.matrix)
            if done:
                self.matrix = l.gen(self.matrix)
                self.update_grid()
                done = False
                if l.game_state(self.matrix, c.winnum) == 'win':
                    self.grid_rows[1][1].configure(text='You', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    self.grid_rows[1][2].configure(text='Win', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    c.winnum *= 2
                if l.game_state(self.matrix, c.winnum) == 'lose':
                    # self.grid_rows[1][1].configure(text='You', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    # self.grid_rows[1][2].configure(text='lose', bg=c.BACKGROUND_EMPTY_CELL_COLOR)
                    box = messagebox.askquestion('Restart?', 'Sure?')
                    if box == 'yes':
                        self.restart()
                    else:
                        self.master.destroy()
    
    def auto_run(self):
        if self.prev == self.pprev:
            self.auto_key_down('w')
            self.pprev, self.prev = self.prev, self.matrix
            if self.prev == self.pprev:
                self.auto_key_down('a')
                self.pprev, self.prev = self.prev, self.matrix
        else:
            for i in 'dsd':
                self.auto_key_down(i)
                self.pprev, self.prev = self.prev, self.matrix
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            with open('gamestate.text', 'w') as f:
                json.dump(self.matrix, f)
            self.master.destroy()


class Control:
    def __init__(self, g):
        self.g = g
        self.pprev, self.prev = [], [0]
        self.direction = 1
        self.prec = ''
    
    def auto_run(self):
        while True:
            self.runs()
    
    def runs(self):
        if self.g.matrix[-1][-1] == 0:
            for i in 'sd':
                self.key_down(i)
        # if self.prev != self.pprev:
        #     t = self.predict(self.g.matrix)
        #     self.key_down(t)
        #     self.pprev, self.prev = self.prev, self.g.matrix
        # else:
        #     self.key_down('s')
        #     self.pprev, self.prev = self.prev, self.g.matrix
        #     self.key_down('d')
        #     self.pprev, self.prev = self.prev, self.g.matrix
        #     if self.prev == self.pprev:
        #         self.key_down('u')
        #         self.pprev, self.prev = self.prev, self.g.matrix
        #         if self.prev == self.pprev:
        #             self.key_down('a')
        #             self.pprev, self.prev = self.prev, self.g.matrix
        #             self.key_down('d')
        #             self.pprev, self.prev = self.prev, self.g.matrix
    
        if self.prev == self.pprev:
            self.key_down('w')
            self.pprev, self.prev = self.prev, self.g.matrix
            if self.prev == self.pprev:
                self.key_down('a')
                self.pprev, self.prev = self.prev, self.g.matrix
        else:
            t = self.predict(self.g.matrix)
            for i in t:
                self.key_down(i)
                self.pprev, self.prev = self.prev, self.g.matrix
     
    
    def key_down(self, key):
        return self.g.auto_key_down(key)
    
    def next_step(self, mat):
        temp = l.transpose(mat)
    
    def predict(self, mat):
        w = l.up(mat)[0]
        d = l.right(mat)[0]
        
        if mat[-1][-1] == 0:
            return 's'

        d0 = sum([b.count(0) for b in d])
        m0 = sum([b.count(0) for b in mat])
        if d0 > m0:
            return 'd'
        
        for i in range(len(w)):
            for j in range(len(w[0])-1):
                if w[i][j] == w[i][j+1]:
                    return 's'
            
        
        for i in range(len(w)):
            for j in range(len(w)-1):
                if w[i][j] == w[i][j+1]:
                    return 'wd'
        
        
        # code = ['w', 's', 'a', 'd']
        # for j in range(c.GRID_LEN - 1, -1, -2):
        #     for i in range(c.GRID_LEN - 1, -1, -1):
        #         t = self.compare(w[i][j], s[i][j], a[i][j], d[i][j])
        #         if t:
        #             temp = [w[i][j], s[i][j], a[i][j], d[i][j]]
        #             return code[temp.index(max(temp))]
        #
        #     for i in range(c.GRID_LEN):
        #         t = self.compare(w[i][j - 1], s[i][j - 1], a[i][j - 1], d[i][j - 1])
        #         if t:
        #             temp = [w[i][j - 1], s[i][j - 1], a[i][j - 1], d[i][j - 1]]
        #             return code[temp.index(max(temp))]
        
        return 'sd'
    
    def compare(self, w, s, a, d):
        l = [w, a, s, d]
        if l.count(max(l)) == 1:
            return True
        return False


game_grid = Game()
contr = Control(game_grid)
thread = threading.Thread(target=contr.auto_run)
thread.start()
game_grid.mainloop()
