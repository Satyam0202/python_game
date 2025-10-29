import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime
import time
import random
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import calendar
import string

# theme
bg_color="#FFF8E8"
panel_color="#FFFFFF"
card_color="#FFFFFF"
red_color="#FF4C4C"
green_color="#4CAF50"
text_color="#2D2D2D"
gray_color="#666666"

# main window
root=tk.Tk()
root.title("Student Playground - Ultimate Edition")
root.geometry("1150x720")
root.configure(bg=bg_color)
root.resizable(True,True)

# globals
alarm_list=[]
reminder_list=[]
stopwatch_on=False
stopwatch_start_time=0.0
stopwatch_total=0.0
big_clock=None

# ------------------------------
# GAMES (7) - DEFINED FIRST
# ------------------------------
def open_rps():
    win=tk.Toplevel(root);win.title("Rock Paper Scissors");win.geometry("380x260")
    tk.Label(win,text="Choose:",font=("Helvetica",12)).pack(pady=20)
    result=tk.Label(win,text="",font=("Consolas",13));result.pack(pady=15)
    def play(choice):
        comp=random.choice(["rock","paper","scissors"])
        if choice==comp:res="DRAW"
        elif(choice=="rock"and comp=="scissors")or(choice=="paper"and comp=="rock")or(choice=="scissors"and comp=="paper"):res="YOU WIN"
        else:res="COMPUTER WINS"
        result.config(text=f"You: {choice}\nComputer: {comp}\n{res}")
    btns=tk.Frame(win);btns.pack(pady=10)
    for opt in["rock","paper","scissors"]:
        tk.Button(btns,text=opt.upper(),width=10,command=lambda x=opt:play(x)).pack(side="left",padx=8)

def open_guess():
    win=tk.Toplevel(root);win.title("Guess Number");win.geometry("380x240")
    target=random.randint(1,100)
    tk.Label(win,text="Guess 1-100:",font=("Helvetica",12)).pack(pady=20)
    entry=tk.Entry(win,font=("Helvetica",12));entry.pack(pady=8)
    info=tk.Label(win,text="",fg=gray_color);info.pack()
    def check():
        try:
            g=int(entry.get())
            if g==target:info.config(text="CORRECT!");win.after(1500,win.destroy)
            elif g<target:info.config(text="Too low!")
            else:info.config(text="Too high!")
        except:info.config(text="Enter number")
    tk.Button(win,text="GUESS",command=check,bg=red_color,fg="white").pack(pady=15)

def open_quiz():
    win=tk.Toplevel(root);win.title("Quiz");win.geometry("520x420")
    questions=[("Python file extension?",[".py",".java",".cpp"],0),("2+2*2=?",["6","8","4"],0),("numpy is for?",["data","web","games"],0),("len('hi')=?",["1","2","3"],1),("tkinter is for?",["GUI","web","database"],0)]
    score,i=0,0
    q_lbl=tk.Label(win,text="",font=("Helvetica",12),wraplength=480);q_lbl.pack(pady=25)
    var=tk.StringVar()
    opts=tk.Frame(win);opts.pack()
    def show():
        nonlocal i
        if i>=len(questions):messagebox.showinfo("Score",f"{score}/{len(questions)}");win.destroy();return
        q,c,a=questions[i]
        q_lbl.config(text=q);var.set(None)
        for w in opts.winfo_children():w.destroy()
        for j,ch in enumerate(c):tk.Radiobutton(opts,text=ch,variable=var,value=j).pack(anchor="w",padx=20)
    def submit():
        nonlocal i,score
        if var.get()and int(var.get())==questions[i][2]:score+=1
        i+=1;show()
    show()
    tk.Button(win,text="SUBMIT",command=submit,bg=green_color,fg="white").pack(pady=20)

def open_tictactoe():
    win=tk.Toplevel(root);win.title("Tic Tac Toe");win.geometry("380x460")
    board=[[""]*3 for _ in range(3)]
    current="X"
    btns=[[None]*3 for _ in range(3)]
    status=tk.Label(win,text="X's turn",font=("Helvetica",12));status.pack(pady=15)
    def check_win():
        for i in range(3):
            if board[i][0]==board[i][1]==board[i][2]!="":return board[i][0]
            if board[0][i]==board[1][i]==board[2][i]!="":return board[0][i]
        if board[0][0]==board[1][1]==board[2][2]!="":return board[0][0]
        if board[0][2]==board[1][1]==board[2][0]!="":return board[0][2]
        if all(board[r][c]!=""for r in range(3)for c in range(3)):return"DRAW"
        return None
    def click(r,c):
        nonlocal current
        if board[r][c]!="":return
        board[r][c]=current
        btns[r][c].config(text=current)
        res=check_win()
        if res:
            msg="DRAW"if res=="DRAW"else f"{res} WINS!"
            messagebox.showinfo("Game Over",msg);win.destroy();return
        current="O"if current=="X"else"X"
        status.config(text=f"{current}'s turn")
    grid=tk.Frame(win);grid.pack(pady=10)
    for r in range(3):
        row=tk.Frame(grid);row.pack()
        for c in range(3):
            b=tk.Button(row,text="",width=8,height=4,font=("Helvetica",16),command=lambda rr=r,cc=c:click(rr,cc))
            b.pack(side="left",padx=3,pady=3)
            btns[r][c]=b

def open_math():
    win=tk.Toplevel(root);win.title("Math Challenge");win.geometry("380x280")
    a=random.randint(1,15);b=random.randint(1,15);op=random.choice(["+","-","*"])
    q=f"{a} {op} {b} = ?"
    tk.Label(win,text=q,font=("Consolas",18)).pack(pady=30)
    entry=tk.Entry(win,font=("Helvetica",12));entry.pack(pady=10)
    info=tk.Label(win,text="",fg=gray_color);info.pack()
    def check():
        try:
            ans=int(entry.get())
            correct=a+b if op=="+"else a-b if op=="-"else a*b
            info.config(text="CORRECT!"if ans==correct else f"Wrong! ({correct})")
            if ans==correct:win.after(1000,win.destroy)
        except:info.config(text="Enter number")
    tk.Button(win,text="SUBMIT",command=check,bg=red_color,fg="white").pack(pady=15)

def open_coin():
    win=tk.Toplevel(root);win.title("Coin Toss");win.geometry("340x220")
    result=tk.Label(win,text="",font=("Consolas",20));result.pack(expand=True)
    tk.Button(win,text="FLIP COIN",command=lambda:result.config(text=random.choice(["HEADS","TAILS"])),bg=red_color,fg="white").pack(pady=20)

def open_dice():
    win=tk.Toplevel(root);win.title("Dice");win.geometry("320x200")
    res=tk.Label(win,text="",font=("Consolas",40));res.pack(expand=True)
    tk.Button(win,text="ROLL",command=lambda:res.config(text=str(random.randint(1,6))),bg=red_color,fg="white").pack(pady=20)

# ------------------------------
# TOOLS (15)
# ------------------------------
def open_calculator():
    win=tk.Toplevel(root);win.title("Calculator");win.geometry("340x460")
    entry=tk.Entry(win,font=("Consolas",20),justify="right");entry.pack(fill="x",padx=20,pady=20)
    def press(val):entry.insert("end",val)
    def clear():entry.delete(0,"end")
    def calc():
        try:res=eval(entry.get());entry.delete(0,"end");entry.insert("end",str(res))
        except:messagebox.showwarning("Error","Invalid")
    buttons=[("7","8","9","/"),("4","5","6","*"),("1","2","3","-"),("0",".","=","+")]
    for row in buttons:
        f=tk.Frame(win);f.pack()
        for b in row:
            cmd=calc if b=="=" else lambda x=b:press(x)
            tk.Button(f,text=b,width=6,height=2,command=cmd).pack(side="left",padx=5,pady=5)
    tk.Button(win,text="CLEAR",command=clear,bg=red_color,fg="white").pack(pady=10)

def open_notes():
    win=tk.Toplevel(root);win.title("Notes");win.geometry("720x500")
    txt=tk.Text(win,wrap="word",font=("Helvetica",12));txt.pack(fill="both",expand=True,padx=15,pady=15)
    def save():
        path=filedialog.asksaveasfilename(defaultextension=".txt")
        if path:open(path,"w").write(txt.get("1.0","end"))
    def load():
        path=filedialog.askopenfilename()
        if path:txt.delete("1.0","end");txt.insert("1.0",open(path).read())
    btns=tk.Frame(win);btns.pack(pady=10)
    tk.Button(btns,text="SAVE",command=save).pack(side="left",padx=10)
    tk.Button(btns,text="LOAD",command=load).pack(side="left",padx=10)
    tk.Button(btns,text="CLOSE",command=win.destroy).pack(side="left",padx=10)

def open_converter():
    win=tk.Toplevel(root);win.title("Converter");win.geometry("380x260")
    def km_m():v=simpledialog.askfloat("KM to M","KM:");messagebox.showinfo("Result",f"{v*1000} m")if v else None
    def c_f():v=simpledialog.askfloat("C to F","C:");messagebox.showinfo("Result",f"{(v*9/5)+32:.1f} F")if v else None
    tk.Button(win,text="KM to M",command=km_m,width=20).pack(pady=12)
    tk.Button(win,text="C to F",command=c_f,width=20).pack(pady=12)
    tk.Button(win,text="CLOSE",command=win.destroy,width=20).pack(pady=12)

def open_password_checker():
    pwd=simpledialog.askstring("Password","Enter:",show="*")
    if pwd:
        score=sum([len(pwd)>=8,any(c.isupper()for c in pwd),any(c.islower()for c in pwd),any(c.isdigit()for c in pwd),any(c in"!@#$%^&*()"for c in pwd)])
        level=["Weak","Medium","Strong"][min(score-1,2)]
        messagebox.showinfo("Strength",level)

def open_stopwatch():
    win=tk.Toplevel(root);win.title("Stopwatch");win.geometry("380x200")
    lbl=tk.Label(win,text="00:00:00",font=("Consolas",28));lbl.pack(pady=30)
    def update():
        if stopwatch_on:
            elapsed=stopwatch_total+(time.time()-stopwatch_start_time)
            h,m,s=int(elapsed//3600),int((elapsed%3600)//60),int(elapsed%60)
            lbl.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        win.after(200,update)
    def start():global stopwatch_on,stopwatch_start_time;stopwatch_start_time=time.time();stopwatch_on=True
    def stop():global stopwatch_total;stopwatch_total+=time.time()-stopwatch_start_time;stopwatch_on=False
    def reset():global stopwatch_on,stopwatch_total;stopwatch_on=False;stopwatch_total=0;lbl.config(text="00:00:00")
    btns=tk.Frame(win);btns.pack()
    tk.Button(btns,text="START",command=start).pack(side="left",padx=10)
    tk.Button(btns,text="STOP",command=stop).pack(side="left",padx=10)
    tk.Button(btns,text="RESET",command=reset).pack(side="left",padx=10)
    update()

def open_alarm():
    t=simpledialog.askstring("Alarm","Time (HH:MM):")
    if t and t not in alarm_list:
        try:datetime.strptime(t,"%H:%M");alarm_list.append(t);messagebox.showinfo("Set",f"Alarm at {t}")
        except:messagebox.showwarning("Error","HH:MM")

def open_reminder():
    msg=simpledialog.askstring("Reminder","Message:")
    t=simpledialog.askstring("Time","HH:MM:")
    if msg and t:
        try:datetime.strptime(t,"%H:%M");reminder_list.append((t,msg));messagebox.showinfo("Set",f"At {t}")
        except:messagebox.showwarning("Error","HH:MM")

def open_marks_plot():
    n=simpledialog.askinteger("Marks","Subjects (1-10):",minvalue=1,maxvalue=10)
    if n:
        marks=[safe_float(simpledialog.askstring("Mark",f"Sub {i+1}:"))for i in range(n)]
        plt.bar(range(1,n+1),marks);plt.xlabel("Subject");plt.ylabel("Marks");plt.show()

def open_grade_summary():
    n=simpledialog.askinteger("Grade","Subjects:",minvalue=1,maxvalue=10)
    if n:
        marks=[safe_float(simpledialog.askstring("Mark",f"Sub {i+1}:"))for i in range(n)]
        avg=np.mean(marks)
        grade="A+"if avg>=90 else"A"if avg>=80 else"B"if avg>=70 else"C"if avg>=60 else"D"if avg>=50 else"F"
        messagebox.showinfo("Grade",f"Avg: {avg:.1f}\nGrade: {grade}")

def open_calendar():
    y=simpledialog.askinteger("Year","Year:")
    m=simpledialog.askinteger("Month","Month (1-12):",minvalue=1,maxvalue=12)
    if y and m:
        win=tk.Toplevel(root);win.title("Calendar")
        txt=tk.Text(win,font=("Consolas",11));txt.pack(padx=20,pady=20)
        txt.insert("1.0",calendar.month(y,m));txt.config(state="disabled")

def open_bmi():
    h=simpledialog.askfloat("BMI","Height (cm):")
    w=simpledialog.askfloat("BMI","Weight (kg):")
    if h and w:
        bmi=w/((h/100)**2)
        cat="Underweight"if bmi<18.5 else"Normal"if bmi<25 else"Overweight"if bmi<30 else"Obese"
        messagebox.showinfo("BMI",f"{bmi:.1f} - {cat}")

def open_age():
    from datetime import date
    birth=simpledialog.askstring("Age","Birth (YYYY-MM-DD):")
    try:
        b=datetime.strptime(birth,"%Y-%m-%d").date()
        days=(date.today()-b).days
        years=days//365
        messagebox.showinfo("Age",f"{years} years, {days%365} days")
    except:messagebox.showwarning("Error","YYYY-MM-DD")

def open_tip():
    bill=simpledialog.askfloat("Tip","Bill amount:")
    tip=simpledialog.askfloat("Tip","Tip %:")
    if bill and tip:
        total=bill+(bill*tip/100)
        messagebox.showinfo("Tip",f"Tip: {bill*tip/100:.2f}\nTotal: {total:.2f}")

def open_currency():
    inr=simpledialog.askfloat("Currency","INR amount:")
    if inr:messagebox.showinfo("USD",f"${inr/83:.2f}")

def open_passgen():
    length=simpledialog.askinteger("Password","Length (8-20):",minvalue=8,maxvalue=20)
    if length:
        chars=string.ascii_letters+string.digits+"!@#$%^&*"
        pwd=''.join(random.choice(chars)for _ in range(length))
        messagebox.showinfo("Password",pwd)

# ------------------------------
# UI - AFTER FUNCTIONS
# ------------------------------
# sidebar
sidebar=tk.Frame(root,bg=panel_color,width=260)
sidebar.pack(side="left",fill="y")
sidebar.pack_propagate(False)

tk.Label(sidebar,text="student",bg=panel_color,fg=text_color,font=("Helvetica",16,"bold")).pack(pady=(40,0))
tk.Label(sidebar,text="playground",bg=panel_color,fg=red_color,font=("Helvetica",16,"bold")).pack(pady=(0,25))
tk.Label(sidebar,text="ultimate dashboard",bg=panel_color,fg=gray_color,font=("Helvetica",12)).pack(pady=(0,35))

nav_frame=tk.Frame(sidebar,bg=panel_color)
nav_frame.pack(pady=10,padx=20,fill="x")

def create_button(text,command,is_home=False):
    bg=red_color if is_home else panel_color
    fg="white" if is_home else text_color
    btn=tk.Button(nav_frame,text=text,bg=bg,fg=fg,font=("Helvetica",11,"bold"),command=command,relief="flat",pady=9)
    btn.pack(fill="x",pady=5,padx=10)
    if not is_home:btn.configure(bd=1,relief="solid")

create_button("HOME",lambda:show_section("home"),True)
create_button("GAMES",lambda:show_section("games"))
create_button("TOOLS",lambda:show_section("tools"))
create_button("ANALYTICS",lambda:show_section("analytics"))
create_button("NOTES",lambda:show_section("notes"))
create_button("EXIT",root.quit)

footer=tk.Frame(sidebar,bg=panel_color)
footer.pack(side="bottom",pady=25)
clock_label=tk.Label(footer,text="",bg=panel_color,fg=gray_color,font=("Helvetica",10))
clock_label.pack()
tk.Label(footer,text="by satyam singh",bg=panel_color,fg=gray_color,font=("Helvetica",10)).pack(pady=(8,0))

# dual scroll
main_container=tk.Frame(root,bg=bg_color)
main_container.pack(fill="both",expand=True)

canvas=tk.Canvas(main_container,bg=bg_color,highlightthickness=0)
canvas.pack(side="left",fill="both",expand=True)

v_scroll=tk.Scrollbar(main_container,orient="vertical",command=canvas.yview)
h_scroll=tk.Scrollbar(main_container,orient="horizontal",command=canvas.xview)
v_scroll.pack(side="right",fill="y")
h_scroll.pack(side="bottom",fill="x")

scroll_area=tk.Frame(canvas,bg=bg_color)
scroll_area.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=scroll_area,anchor="nw")
canvas.configure(yscrollcommand=v_scroll.set,xscrollcommand=h_scroll.set)

canvas.bind_all("<MouseWheel>",lambda e:canvas.yview_scroll(-1 if e.delta>0 else 1,"units"))
canvas.bind_all("<Shift-MouseWheel>",lambda e:canvas.xview_scroll(-1 if e.delta>0 else 1,"units"))

main_frame=scroll_area
current_frame=None

def clear_main():
    global current_frame
    if current_frame:current_frame.destroy()
    current_frame=tk.Frame(main_frame,bg=bg_color)
    current_frame.pack(fill="both",expand=True,padx=40,pady=30)

def show_section(section):
    clear_main()
    if section=="home":show_home()
    elif section=="games":show_games()
    elif section=="tools":show_tools()
    elif section=="analytics":show_analytics()
    elif section=="notes":show_notes()

def show_home():
    add_header("WELCOME TO STUDENT PLAYGROUND","7 Games to 15 Tools to Analytics")
    row=tk.Frame(current_frame,bg=bg_color);row.pack(fill="x",pady=15)
    make_card(row,"games","7 fun mini-games","Gamepad",lambda:show_section("games")).pack(side="left",padx=15)
    make_card(row,"tools","15 study helpers","Tools",lambda:show_section("tools")).pack(side="left",padx=15)
    make_card(row,"analytics","plot marks & stats","Chart",lambda:show_section("analytics")).pack(side="left",padx=15)
    make_card(row,"notes","save/load notes","Note",lambda:show_section("notes")).pack(side="left",padx=15)

    mid=tk.Frame(current_frame,bg=bg_color);mid.pack(fill="both",expand=True,pady=30)
    left=make_big_card(mid,650,360)
    tk.Label(left,text="Hello, Student!\nExplore games, tools & analytics.",bg=card_color,fg=text_color,font=("Helvetica",12),justify="left").pack(anchor="nw",padx=30,pady=30)
    btns=tk.Frame(left,bg=card_color);btns.pack(pady=20)
    tk.Button(btns,text="OPEN GAMES",bg=red_color,fg="white",font=("Helvetica",11,"bold"),command=lambda:show_section("games")).pack(side="left",padx=15)
    tk.Button(btns,text="EXPLORE TOOLS",bg=green_color,fg="white",font=("Helvetica",11,"bold"),command=lambda:show_section("tools")).pack(side="left",padx=15)

    try:
        img=Image.open("main.png").resize((300,200),Image.Resampling.LANCZOS)
        photo=ImageTk.PhotoImage(img)
        tk.Label(left,image=photo,bg=card_color).pack(pady=15)
        left.image=photo
    except:pass

    right=make_big_card(mid,420,360)
    tk.Label(right,text="LIVE CLOCK",bg=card_color,fg=gray_color,font=("Helvetica",10)).pack(pady=(30,8))
    global big_clock
    big_clock=tk.Label(right,text="",bg=card_color,fg=text_color,font=("Consolas",32));big_clock.pack(pady=15)
    quick=tk.Frame(right,bg=card_color);quick.pack(pady=20)
    tk.Button(quick,text="STOPWATCH",command=open_stopwatch,width=20).pack(pady=6)
    tk.Button(quick,text="SET ALARM",command=open_alarm,width=20).pack(pady=6)
    tk.Button(quick,text="SET REMINDER",command=open_reminder,width=20).pack(pady=6)

def show_games():
    clear_main()
    add_header("7 FUN GAMES","Play & Enjoy")
    create_grid(games_list,game_tile,6)

def show_tools():
    clear_main()
    add_header("15 STUDENT TOOLS","Study, Calculate, Convert")
    create_grid(tools_list,tool_tile,6)

def show_analytics():
    clear_main()
    add_header("ANALYTICS","Visualize Progress")
    body=tk.Frame(current_frame,bg=bg_color);body.pack(pady=50,padx=50,fill="both",expand=True)
    tk.Button(body,text="PLOT MARKS",command=open_marks_plot,bg=red_color,fg="white",width=30,height=2).pack(pady=20)
    tk.Button(body,text="GRADE SUMMARY",command=open_grade_summary,bg=green_color,fg="white",width=30,height=2).pack(pady=20)

def show_notes():
    clear_main()
    add_header("NOTES SAVER","Save & Load")
    open_notes()

# data
games_list=[
    ("Rock Paper Scissors","vs Computer",open_rps),
    ("Guess Number","1-100",open_guess),
    ("Quiz Game","5 MCQs",open_quiz),
    ("Tic Tac Toe","2 Players",open_tictactoe),
    ("Math Challenge","Quick Solve",open_math),
    ("Coin Toss","Heads/Tails",open_coin),
    ("Dice Roll","1-6",open_dice)
]

tools_list=[
    ("Calculator","Arithmetic",open_calculator),
    ("Notes Saver","Save/Load",open_notes),
    ("Unit Converter","km to m, C to F",open_converter),
    ("Password Checker","Strength",open_password_checker),
    ("Stopwatch","Timer",open_stopwatch),
    ("Set Alarm","Alert",open_alarm),
    ("Set Reminder","Schedule",open_reminder),
    ("Marks Plot","Chart",open_marks_plot),
    ("Grade Summary","A+/F",open_grade_summary),
    ("Calendar","View Month",open_calendar),
    ("BMI Calculator","Health",open_bmi),
    ("Age Calculator","Years",open_age),
    ("Tip Calculator","Bill",open_tip),
    ("Currency","INR to USD",open_currency),
    ("Password Gen","Random",open_passgen)
]

# helpers
def add_header(title,sub):
    tk.Label(current_frame,text=title,bg=bg_color,fg=text_color,font=("Helvetica",28,"bold")).pack(anchor="nw",padx=40,pady=(40,10))
    tk.Label(current_frame,text=sub,bg=bg_color,fg=gray_color,font=("Helvetica",15)).pack(anchor="nw",padx=40,pady=(0,30))

def create_grid(items,tile_func,cols):
    grid=tk.Frame(current_frame,bg=bg_color);grid.pack(padx=40,pady=30,fill="both",expand=True)
    for i,(t,s,cmd)in enumerate(items):
        r,c=i//cols,i%cols
        tile_func(grid,t,s,cmd).grid(row=r,column=c,padx=18,pady=18,sticky="nsew")
    for i in range(cols):grid.grid_columnconfigure(i,weight=1,uniform="col")

def make_card(parent,title,sub,emoji,cmd):
    c=tk.Frame(parent,bg=card_color,width=260,height=140,relief="raised",bd=1);c.pack_propagate(False)
    tk.Label(c,text=f"{emoji}  {title.upper()}",bg=card_color,fg=text_color,font=("Helvetica",13,"bold")).pack(pady=(20,8),padx=20,anchor="w")
    tk.Label(c,text=sub,bg=card_color,fg=gray_color,font=("Helvetica",10),wraplength=230).pack(padx=20,anchor="w")
    tk.Button(c,text="OPEN",bg=red_color,fg="white",font=("Helvetica",11,"bold"),command=cmd).pack(side="bottom",pady=18)
    return c

def game_tile(parent,title,sub,cmd):
    t=tk.Frame(parent,bg=card_color,width=220,height=150,relief="raised",bd=1);t.pack_propagate(False)
    tk.Label(t,text=title.upper(),bg=card_color,fg=text_color,font=("Helvetica",11,"bold")).pack(pady=(18,6),padx=18,anchor="w")
    tk.Label(t,text=sub,bg=card_color,fg=gray_color,font=("Helvetica",10)).pack(padx=18,anchor="w")
    tk.Button(t,text="PLAY",bg=red_color,fg="white",font=("Helvetica",11,"bold"),command=cmd).pack(side="bottom",pady=18)
    return t

def tool_tile(parent,title,sub,cmd):
    t=tk.Frame(parent,bg=card_color,width=220,height=140,relief="raised",bd=1);t.pack_propagate(False)
    tk.Label(t,text=title.upper(),bg=card_color,fg=text_color,font=("Helvetica",10,"bold")).pack(pady=(16,5),padx=16,anchor="w")
    tk.Label(t,text=sub,bg=card_color,fg=gray_color,font=("Helvetica",10)).pack(padx=16,anchor="w")
    tk.Button(t,text="OPEN",bg=red_color,fg="white",font=("Helvetica",11,"bold"),command=cmd).pack(side="bottom",pady=15)
    return t

def make_big_card(parent,w,h):
    f=tk.Frame(parent,bg=card_color,width=w,height=h,relief="raised",bd=1);f.pack(side="left",fill="both",expand=True,padx=15);f.pack_propagate(False)
    return f

# clock & schedules
def update_clock():
    now=datetime.now()
    if big_clock:big_clock.config(text=now.strftime("%H:%M:%S"))
    clock_label.config(text=now.strftime("%d %b %Y to %H:%M"))
    root.after(500,update_clock)

def check_schedules():
    now=datetime.now().strftime("%H:%M")
    if now in alarm_list:
        root.bell();messagebox.showinfo("ALARM",f"Time: {now}");alarm_list.remove(now)
    for t,msg in reminder_list[:]:
        if t==now:
            root.bell();messagebox.showinfo("REMINDER",msg);reminder_list.remove((t,msg))
    root.after(60000,check_schedules)

def safe_float(val,default=0.0):
    try:return float(val)
    except:return default

# start
show_section("home")
update_clock()
check_schedules()

root.mainloop()