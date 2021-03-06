from tkinter import *
import time

root = Tk()

#creating 2 frames: top(contains Buttons) bottom (contains grid)
topFrame = Frame(root)
topFrame.pack()

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

#whenever click on Text Field, clear the content
def clear_on_entry(event):
    event.widget.delete(0,END)


###################################### BOTTOM FRAME ######################################


#Create a grid of Labels for GOL in bottom frame
def Create_grid():

        for label_Grid in bottomFrame.winfo_children():
            label_Grid.destroy()

        #matrix of cell
        global matrix, nex_gen_matrix
        matrix = [[0 for x in range(int(col_Field.get()))] for y in range(int(row_Field.get()))]
        nex_gen_matrix = [[0 for x in range(int(col_Field.get()))] for y in range(int(row_Field.get()))]

        #create a label matrix in GUI and set initial values to matrix as 0 for every cell
        for row_index in range(int(row_Field.get())):
            Grid.rowconfigure(bottomFrame, row_index, weight=1)
            for col_index in range(int(col_Field.get())):
                Grid.columnconfigure(bottomFrame, col_index, weight=1, )
                label_Grid = Label(bottomFrame, bg="white", borderwidth=2, relief="groove", width="5", height="2", name=str(row_index)+" "+str(col_index))
                label_Grid.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                label_Grid.bind("<Button-1>", label_click)


#change color of label and value of matrix
def label_click(event):
    names = str(event.widget).split(".")[-1]
    names = names.split(" ")

    r = int(names[0])
    c = int(names[1])


    if event.widget.cget("bg")=="black":
        event.widget.config(bg="white")
        matrix[r][c] = 0

    else:
        event.widget.config(bg="black")
        matrix[r][c] = 1



####################################### Generations #######################################

def generations():
    global matrix, nex_gen_matrix

    #aux = [[0 for x in range(int(col_Field.get()))] for y in range(int(row_Field.get()))]

    for row_position in range(int(row_Field.get())):
        for col_position in  range(int(col_Field.get())):

            count_neighbor = get_neighbor(row_position,col_position)

            #less than 2 neighbor die of lonelyness
            if (matrix[row_position][col_position] == 1 and count_neighbor < 2):
                nex_gen_matrix[row_position][col_position] = 0

            #more than 3 neighbor die of overpopulation
            elif (matrix[row_position][col_position] == 1 and count_neighbor > 3):
               nex_gen_matrix[row_position][col_position] = 0

            #exactely 3 and dead, back to life
            elif (matrix[row_position][col_position] == 0 and count_neighbor == 3):
                nex_gen_matrix[row_position][col_position] = 1

            #2 or 3 neighbors alive, keep the same
            elif (matrix[row_position][col_position] == 1 and (count_neighbor == 2 or count_neighbor == 3)):
                nex_gen_matrix[row_position][col_position] = matrix[row_position][col_position]

    matrix = nex_gen_matrix[:]

    nex_gen_matrix = [[0 for x in range(int(col_Field.get()))] for y in range(int(row_Field.get()))]

    nex_Generation_Gui()



#Show next generetion on screen
def  nex_Generation_Gui():


    for label_Grid in bottomFrame.winfo_children():
        label_Grid.destroy()

    for row_index in range(int(row_Field.get())):
        Grid.rowconfigure(bottomFrame, row_index, weight=1)
        for col_index in range(int(col_Field.get())):
            if(matrix[row_index][col_index] == 1):

                #set label color to black
                Grid.columnconfigure(bottomFrame, col_index, weight=1, )
                label_Grid = Label(bottomFrame, bg="black", borderwidth=2, relief="groove", width="5", height="2",
                                   name=str(row_index) + " " + str(col_index))
                label_Grid.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                label_Grid.bind("<Button-1>", label_click)

            else:
                #set label color to white
                Grid.columnconfigure(bottomFrame, col_index, weight=1, )
                label_Grid = Label(bottomFrame, bg="white", borderwidth=2, relief="groove", width="5", height="2",
                                   name=str(row_index) + " " + str(col_index))
                label_Grid.grid(row=row_index, column=col_index, sticky=N + S + E + W)
                label_Grid.bind("<Button-1>", label_click)


def get_neighbor(row,col):

    count = 0;

    #Down
    if(int(row_Field.get()) > row+1):
        if ( matrix[row + 1][col] == 1):
            count += 1
    #UP
    if(row-1>=0):
        if (matrix[row - 1][col] == 1):
            count += 1
    #RIGHT
    if (int(col_Field.get()) > col+1):
        if (matrix[row][col + 1] == 1 ):
            count += 1
    #LEFT
    if(col-1>=0):
        if (matrix[row][col - 1] == 1):
            count+=1
    #DIAG RD
    if(int(row_Field.get()) > row+1 and int(col_Field.get()) > col+1):
        if (matrix[row + 1][col + 1] == 1):
            count += 1
    #DIAG LD
    if(int(row_Field.get()) > row+1 and col-1>=0):
        if (matrix[row + 1][col - 1] == 1):
            count += 1
    #DIAG RU
    if (row-1 >= 0 and int(col_Field.get()) > col + 1):
        if (matrix[row - 1][col + 1] == 1):
            count += 1
    #DIAG LU
    if(row-1>=0 and col-1>=0):
        if (matrix[row - 1][col - 1] == 1):
            count += 1

    return count;

play_click = TRUE
def play():
    print("start")
    while play_click:
        generations()
        print("time")
        time.sleep(5)

def stop():
    play_click = FALSE;
####################################### TOP FRAME #######################################
#Creating buttons and textfield

row_Field = Entry(topFrame)
row_Field.insert(0,'ROW Value')
row_Field.bind('<FocusIn>',clear_on_entry)
row_Field.pack(side=LEFT)


label1 = Label(topFrame,text="X")
label1.pack(side=LEFT);


col_Field = Entry(topFrame)
col_Field.insert(0,'COL Value')
col_Field.bind('<FocusIn>',clear_on_entry)
col_Field.pack(side=LEFT)

set_Btn = Button(topFrame, text="Set Grid", command=Create_grid)
set_Btn.pack(side=LEFT)


gen_Btn = Button(topFrame, text="Generations", command=generations)
gen_Btn.pack(side=LEFT)

gen_Field = Entry(topFrame)
gen_Field.pack(side=LEFT)

play_Btn = Button(topFrame, text="Play", bg="green", command=play)
play_Btn.pack(side=LEFT)
play_Btn.config(width=25)

stop_Btn = Button(topFrame, text="stop", bg="red", command=stop)
stop_Btn.pack(side=LEFT)
stop_Btn.config(width=10)

root.mainloop()