from tkinter import *
import tkinter.messagebox as mb
import random
import sqlite3


class Registr:

    def CreateNewUser(self, username, password, password_again):
        if username == '' or password == '' or password_again == '':
            msg = 'Заполните все поля'
            mb.showerror("Ошибка", msg)
        else:
            con = sqlite3.connect('Users.sqlite')
            cur = con.cursor()
            cur.execute(' create table if not exists Users(Username TEXT,Password TEXT)')
            con.commit()
            cur.execute('SELECT Username FROM Users')
            for i in cur.fetchall():
                if username == i[0]:
                    msg = 'Имя пользователя уже существует'
                    mb.showerror("Ошибка", msg)
            else:
                if password != password_again:
                    msg = 'Пароли не совпадают'
                    mb.showerror("Ошибка", msg)
                else:
                    new_user = (username, password)
                    cur.execute("""INSERT INTO Users(Username, Password) VALUES(?,?);""", new_user)
                    con.commit()
                    msg = "Новый пользователь успешно зарегестрирован"
                    mb.showinfo("Успешно", msg)
                    game = TTT_VS_PC
                    self.window_Reg.destroy()
                    return game()

    def __init__(self):
        window_Entry.destroy()
        self.window_Reg = Tk()
        self.window_Reg.title('Регистрация')
        self.window_Reg.geometry('300x300')
        self.window_Reg.eval('tk::PlaceWindow . center')
        username_label = Label(self.window_Reg, text='Имя пользователя', )
        username_entry = Entry(self.window_Reg, bg='#fff', fg='#444')
        password_label = Label(self.window_Reg, text='Пароль')
        password_entry = Entry(self.window_Reg, bg='#fff', fg='#444')
        password_label_confirm = Label(self.window_Reg, text='Повторите пароль')
        password_entry_confirm = Entry(self.window_Reg, bg='#fff', fg='#444')
        send_btn = Button(self.window_Reg, text='Зарегистрироваться', command=lambda:
        self.CreateNewUser(username_entry.get(), password_entry.get(), password_entry_confirm.get(), ))

        username_label.pack(padx=10, pady=8)
        username_entry.pack(padx=10, pady=8)
        password_label.pack(padx=10, pady=8)
        password_entry.pack(padx=10, pady=8)
        password_label_confirm.pack(padx=10, pady=8)
        password_entry_confirm.pack(padx=10, pady=8)
        send_btn.pack(padx=10, pady=8)

        self.window_Reg.mainloop()


class Login_in:

    def CheckExist(self, username, password):
        if username == '' or password == '':
            msg = 'Заполните все поля'
            mb.showerror("Ошибка", msg)
        else:
            con = sqlite3.connect('Users.sqlite')
            cur = con.cursor()
            cur.execute(' create table if not exists Users(Username TEXT,Password TEXT)')
            con.commit()
            cur.execute('SELECT * FROM Users')
            for i in cur.fetchall():
                if username == i[0]:
                    print(password == i[1])
                    if password == i[1]:
                        msg = "Вы успешно зашли"
                        mb.showinfo("Успешно", msg)
                        self.window_Login.destroy()
                        game = TTT_VS_PC
                        return game()
                    else:
                        msg = 'Пароль не совпадает'
                        mb.showerror("Ошибка", msg)
                        return
            msg = 'Такой пользователь не зарегестрирован'
            mb.showerror("Ошибка", msg)
            return



    def __init__(self):
        window_Entry.destroy()
        self.window_Login = Tk()
        self.window_Login.title('Вход')
        self.window_Login.geometry('300x250')
        self.window_Login.eval('tk::PlaceWindow . center')
        username_label = Label(self.window_Login, text='Имя пользователя', )
        username_entry = Entry(self.window_Login, bg='#fff', fg='#444')
        password_label = Label(self.window_Login, text='Пароль')
        password_entry = Entry(self.window_Login, bg='#fff', fg='#444')
        send_btn = Button(self.window_Login, text='Войти', command=lambda:
        self.CheckExist(username_entry.get(), password_entry.get()))

        username_label.pack(padx=10, pady=8)
        username_entry.pack(padx=10, pady=8)
        password_label.pack(padx=10, pady=8)
        password_entry.pack(padx=10, pady=8)
        send_btn.pack(padx=10, pady=8)

        self.window_Login.mainloop()


class TTT_VS_PC:

    def __init__(self):
        self.reload()

    def click(self, r, c):
        if self.player == "X" and self.field[r][c] == 0:
            self.b[r][c].configure(text="X")
            self.field[r][c] = 'X'
            self.player = "O"
            self.check_win()
            self.check_draw()
            self.pc_move()

    def pc_move(self):
        move_line = self.check_line()
        move_row = self.check_row()
        move_oblique = self.check_oblique()
        if move_line:
            self.b[move_line[0]][move_line[1]].configure(text="O")
            self.field[move_line[0]][move_line[1]] = 'O'
            self.player = "X"
            self.check_win()
            return
        if move_row:
            self.b[move_row[0]][move_row[1]].configure(text="O")
            self.field[move_row[0]][move_row[1]] = 'O'
            self.player = "X"
            self.check_win()
            return
        if move_oblique:
            self.b[move_oblique[0]][move_oblique[1]].configure(text="O")
            self.field[move_oblique[0]][move_oblique[1]] = 'O'
            self.player = "X"
            self.check_win()
            return
        else:
            possiblemove = []
            for i in range(3):
                for j in range(3):
                    if self.field[i][j] == 0:
                        possiblemove.append([i, j])
            corner = []
            for i in possiblemove:
                if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                    corner.append(i)
            if len(corner) >= 2:
                move = random.choice(corner)
                self.b[move[0]][move[1]].configure(text="O")
                self.field[move[0]][move[1]] = 'O'
                self.player = "X"
                self.check_win()
                return
            nswe = []
            for i in possiblemove:
                if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                    nswe.append(i)
            if len(nswe) > 0:
                move = random.choice(nswe)
                self.b[move[0]][move[1]].configure(text="O")
                self.field[move[0]][move[1]] = 'O'
                self.player = "X"
                self.check_win()
                return
            if [1, 1] in possiblemove:
                self.b[1][1].configure(text="O")
                self.field[1][1] = 'O'
                self.player = "X"
                self.check_win()
                return

    def check_win(self):
        if      (self.field[0][0] == "X" and self.field[0][1] == "X" and self.field[0][2] == "X") or\
                (self.field[1][0] == "X" and self.field[1][1] == "X" and self.field[1][2] == "X") or\
                (self.field[2][0] == "X" and self.field[2][1] == "X" and self.field[2][2] == "X") or\
                (self.field[0][0] == "X" and self.field[1][0] == "X" and self.field[2][0] == "X") or\
                (self.field[0][1] == "X" and self.field[1][1] == "X" and self.field[2][1] == "X") or\
                (self.field[0][2] == "X" and self.field[1][2] == "X" and self.field[2][2] == "X") or\
                (self.field[0][0] == "X" and self.field[1][1] == "X" and self.field[2][2] == "X") or\
                (self.field[0][2] == "X" and self.field[1][1] == "X" and self.field[2][0] == "X"):
            answer = mb.askquestion('Вы выиграли!', ' Начать заного?')
            if answer == 'yes':
                self.window_ttt.destroy()
                self.reload()
            else:
                self.window_ttt.destroy()
                exit()
        elif    (self.field[0][0] == "O" and self.field[0][1] == "O" and self.field[0][2] == "O") or\
                (self.field[1][0] == "O" and self.field[1][1] == "O" and self.field[1][2] == "O") or\
                (self.field[2][0] == "O" and self.field[2][1] == "O" and self.field[2][2] == "O") or\
                (self.field[0][0] == "O" and self.field[1][0] == "O" and self.field[2][0] == "O") or\
                (self.field[0][1] == "O" and self.field[1][1] == "O" and self.field[1][2] == "O") or\
                (self.field[0][2] == "O" and self.field[1][2] == "O" and self.field[2][2] == "O") or\
                (self.field[0][0] == "O" and self.field[1][1] == "O" and self.field[2][2] == "O") or\
                (self.field[0][2] == "O" and self.field[1][1] == "O" and self.field[2][0] == "O"):
            answer = mb.askquestion('Компьютер выиграл!', ' Начать заного?')
            if answer == 'yes':
                self.window_ttt.destroy()
                self.reload()
            else:
                self.window_ttt.destroy()
                exit()

    def check_draw(self):
        for i in self.field:
            for j in i:
                if j == 0:
                    return
        answer = mb.askquestion('Ничья', ' Начать заного?')
        if answer == 'yes':
            self.window_ttt.destroy()
            self.reload()
        else:
            self.window_ttt.destroy()
            exit()


    def reload(self):
        self.window_ttt = Tk()
        self.window_ttt.title('Крестики-Нолики')
        self.window_ttt.eval('tk::PlaceWindow . center')
        self.player = "X"
        self.b = []
        self.field = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(3):
            self.b.append(i)
            self.b[i] = []
            for j in range(3):
                self.b[i].append(j)
                self.b[i][j] = Button(height=4, width=8, command=lambda r=i, c=j: self.click(r, c))
                self.b[i][j].grid(row=i, column=j)
        self.window_ttt.mainloop()

    def check_line(self):
        for i in range(3):
            sumO = 0
            for j in range(3):
                if self.field[i][j] == 'O':
                    sumO += 1
                    if sumO == 2:
                        if 0 in self.field[i]:
                            return [i, self.field[i].index(0)]
        for i in range(3):
            sumX = 0
            for j in range(3):
                if self.field[i][j] == 'X':
                    sumX += 1
                    if sumX == 2:
                        if 0 in self.field[i]:
                            return [i, self.field[i].index(0)]
        return False

    def check_row(self):
        for i in range(3):
            sumO = 0
            for j in range(3):
                if self.field[j][i] == 'O':
                    sumO += 1
                    if sumO == 2:
                        for g in range(3):
                            if self.field[g][i] == 0:
                                return [g, i]
        for i in range(3):
            sumX = 0
            for j in range(3):
                if self.field[j][i] == 'X':
                    sumX += 1
                    if sumX == 2:
                        for g in range(3):
                            if self.field[g][i] == 0:
                                return [g, i]

        return False

    def check_oblique(self):
        if self.field[1][1] == 'O':
            for i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                if self.field[i[0]][i[1]] == 'O':
                    if i[0] == i[1] == 2:
                        if self.field[0][0] == 0:
                            return [0, 0]
                    elif i[0] == i[1] == 0:
                        if self.field[2][2] == 0:
                            return [2, 2]
                    elif i[0] != i[1] and i[0] == 0:
                        if self.field[2][0] == 0:
                            return [2, 0]
                    else:
                        if self.field[0][2] == 0:
                            return [0, 2]
        if self.field[1][1] == 'X':
            for i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                if self.field[i[0]][i[1]] == 'X':
                    if i[0] == i[1] == 2:
                        if self.field[0][0] == 0:
                            return [0, 0]
                    elif i[0] == i[1] == 0:
                        if self.field[2][2] == 0:
                            print(2)
                            return [2, 2]
                    elif i[0] != i[1] and i[0] == 0:
                        if self.field[2][0] == 0:
                            return [2, 0]
                    else:
                        if self.field[0][2] == 0:
                            return [0, 2]
        return False

window_Entry = Tk()
window_Entry.title('Крестики-Нолики')
window_Entry.geometry('250x250')
window_Entry.eval('tk::PlaceWindow . center')
loginin = Button(window_Entry, text='Вход', command=Login_in)
reg = Button(window_Entry, text='Регистрация', command=Registr)
loginin.pack(padx=10, pady=8)
reg.pack(padx=10, pady=8)

window_Entry.mainloop()
