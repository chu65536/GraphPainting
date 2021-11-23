from tkinter import *
from math import *

# ------------------------------VARIABLES------------------------------
d = 25 # Nodes size
n = 0 # Size of graph
clicked_node = (False, 0, 0, 0, 0)
nodes = [] # All nodes
connections = [] # All nodes connections
lines = [] # All lines between nodes
colors = {} # Colors of all nodes
color = ['red', 'green2', 'blue', 'yellow', 'purple3']
line_shadow_num = 0
line_shadow_x = 0
line_shadow_y = 0


# ------------------------------GRAPHICAL PART------------------------------
# Return info about node under the cursor
def get_node_under_cursor():
    ret_num = 0
    ret_x = 0
    ret_y = 0
    ret_ind = 0

    for i in nodes:
        num, x, y, ind = i
        tag = canvas.gettags(num)

        if tag[0] == 'highlighted':
            ret_num = num
            ret_x = x
            ret_y = y
            ret_ind = ind
            break
            
    return ret_num, ret_x, ret_y, ret_ind

# Checking if node under cursor
def node_under_cursor():
    for i in nodes:
        num = i[0]
        tag = canvas.gettags(num)

        if tag[0] == 'highlighted':
            return True

    return False

# Checking if it possible to place node
def node_place_ok(x, y):
    flag = True
    for i in nodes:
        node_x, node_y = i[1], i[2]
        mx, my = abs(node_x - x), abs(node_y - y)
        r = sqrt(mx * mx + my * my)

        if r <= d * 2:
            flag = False

    return flag

# Painting each node
def paint_nodes():
    for i in nodes:
        num, x, y, ind = i
        if ind in colors:
            canvas.itemconfig(num, fill=color[colors[ind]])
        else:
            canvas.itemconfig(num, fill='grey')

# Connecting pair of nodes
def connect_nodes(num, x, y, ind):
    global clicked_node
    global line_shadow_num, line_shadow_x, line_shadow_y

    if clicked_node[0]:
        line = canvas.create_line(clicked_node[2], clicked_node[3], x, y, width=5)
        canvas.tag_lower(line)
        lines.append((line, clicked_node[1], num, clicked_node[2], clicked_node[3], x, y))
        if (clicked_node[4], ind) not in connections and (ind, clicked_node[4]) not in connections:
            connections.append((clicked_node[4], ind))

        canvas.delete(line_shadow_num)
        clicked_node = (False, 0, 0, 0, 0)
        for i in nodes:
            tmp_num = i[0]
            tag = canvas.gettags(tmp_num)

            if tag[0] == 'clicked':
                if tmp_num == num:
                    canvas.itemconfig(tmp_num, fill='grey', tag='highlighted', width=4)
                else:
                    canvas.itemconfig(tmp_num, fill='grey', tag='common', width=1)
        paint_nodes()
        canvas.tag_lower('shadow')
    else:
        clicked_node = (True, num, x, y, ind)
        line_shadow_num = canvas.create_line(x, y, x, y, width=5, fill='lightgrey', tag='line_shadow')
        line_shadow_x = x
        line_shadow_y = y


# Redrawing lines after drag
def redraw_lines(num, x, y):
    for i in lines:
        if i[1] == num:
            canvas.coords(i[0], x, y, i[5], i[6])
        if i[2] == num:
            canvas.coords(i[0], i[3], i[4], x, y)

# Delete node
def delete_node():
    global n
    i = 0
    while i < len(nodes):
        num = nodes[i][0]
        ind = nodes[i][3]
        tag = canvas.gettags(num)

        if tag[0] == 'highlighted':
            canvas.delete(num)
            nodes.pop(i)
            if ind in colors:
                colors.pop(ind)

            j = 0
            while j < len(lines):
                if lines[j][1] == num or lines[j][2] == num:
                    canvas.delete(lines[j][0])
                    lines.pop(j)
                else:
                    j+= 1
            j = 0
            while j < len(connections):
                if connections[j][0] == ind or connections[j][1] == ind:
                    connections.pop(j)
                else:
                    j += 1
            break
        else:
            i += 1

# Middle click (creating new node or connections between pair)
def mouse_m_click(event):
    x, y = event.x, event.y
    global n

    if node_under_cursor():
        num, mx, my, ind = get_node_under_cursor()
        canvas.itemconfig(num, tag='clicked')
        connect_nodes(num, mx, my, ind)
        return
    else:
        for i in nodes:
            num, ind = i[0], i[3]
            tag = canvas.gettags(num)

            if tag[0] == 'clicked':
                if ind in colors:
                    canvas.itemconfig(num, fill=color[colors[ind]], tag='common', width=1)
                else:
                    canvas.itemconfig(num, fill='grey', tag='common', width=1)
                global clicked_node
                canvas.delete(line_shadow_num)
                clicked_node = (False, 0, 0, 0)
                return
              

    if node_place_ok(x, y):
        n += 1
        num = canvas.create_oval(x - d, y - d, x + d, y + d, fill='grey', tag='highlighted', width=4)
        nodes.append((num, x, y, n))
        print(nodes)
    else:
        print("To close to another node")

    #print(connections)

    
# Right click (removin node and all it connections)
def mouse_r_click(event):
    x, y = event.x, event.y

    for i in nodes:
        num, ind = i[0], i[3]
        tag = canvas.gettags(num)

        if tag[0] == 'clicked':
            if ind in colors:
                canvas.itemconfig(
                    num, fill=color[colors[ind]], tag='common', width=1)
            else:
                canvas.itemconfig(num, fill='grey', tag='common', width=1)
            global clicked_node
            canvas.delete(line_shadow_num)
            clicked_node = (False, 0, 0, 0)
            return

    delete_node()

# Drag nodes
def drag_motion(event):
    x, y = event.x, event.y
    canvas.moveto('shadow', x - d, y - d)

    ok = False
    for i in nodes:
        num = i[0]
        tag = canvas.gettags(num)

        if tag[0] == 'highlighted':
            ok = True
            break

    if not ok:
        return

    x = min(x, 775)
    x = max(x, 25)
    y = min(y, 575)
    y = max(y, 25)

    canvas.moveto(num, x - d, y - d)
    for i in range(len(nodes)):
        cur_num = nodes[i][0]
        cur_ind = nodes[i][3]

        if cur_num == num:
            nodes[i] = cur_num, x, y, cur_ind
            for j in range(len(lines)):
                if lines[j][1] == num:
                    lines[j] = lines[j][0], lines[j][1], lines[j][2], x, y, lines[j][5], lines[j][6]
                if lines[j][2] == num:
                    lines[j] = lines[j][0], lines[j][1], lines[j][2], lines[j][3], lines[j][4], x, y

            redraw_lines(cur_num, x, y)

# Drawing shadow under cursor
def draw_shadow(x, y):
    canvas.moveto('shadow', x - d, y - d)
    canvas.tag_lower('shadow')

# Highlighting node under cursor
def highlight_node(x, y):
    cnt = 0
    for i in nodes:
        num, node_x, node_y, ind = i
        tag = canvas.gettags(num)
        mx, my = abs(node_x - x), abs(node_y - y)
        r = sqrt(mx * mx + my * my)

        if tag[0] == 'clicked':
            continue

        if r <= d and cnt < 1:
            canvas.itemconfig(num, tag='highlighted', outline='black', width=4)
            cnt += 1
        else:
            canvas.itemconfig(num, tag='common', width=1)

# Line shadow
def draw_line_shadow(x, y):
    canvas.coords('line_shadow', line_shadow_x, line_shadow_y, x, y)
    canvas.tag_lower('line_shadow')

# Mouse Motion
def mouse_motion(event):
    x, y = event.x, event.y

    if clicked_node[0]:
        draw_line_shadow(x, y)

    draw_shadow(x, y)
    paint_nodes()
    highlight_node(x, y)


#------------------------------LOGIC------------------------------
# Painting graph
def painting():
    tmp_dict = {}

    for i in connections:
        a, b = i
        if a in tmp_dict:
            tmp_dict[a] += 1
        else:
            tmp_dict[a] = 1

        if b in tmp_dict:
            tmp_dict[b] += 1
        else:
            tmp_dict[b] = 1

    number_of_connections = []
    for i in tmp_dict:
        number_of_connections.append((tmp_dict[i], i))
    number_of_connections.sort(reverse=True)

    colors.clear()
    color = -1

    for i in range(5):
        used = []
        color += 1

        for k in number_of_connections:
            node = k[1]
            if node in colors:
                continue

            if node not in used:
                colors[node] = color
                for j in connections:
                    if node == j[0]:
                        used.append(j[1])
                    if node == j[1]:
                        used.append(j[0])

    paint_nodes()

def reset_nodes():
    colors.clear()

    for i in nodes:
        num = i[0]
        canvas.itemconfig(num, fill='grey')

def clear_graph():
    global clicked_node, n
    while len(nodes) > 0:
        num = nodes[0][0]
        canvas.delete(num)
        nodes.pop(0)

    while len(lines) > 0:
        num = lines[0][0]
        canvas.delete(num)
        lines.pop(0)

    canvas.delete('line_shadow')
    connections.clear()
    colors.clear()
    clicked_node = (False, 0, 0, 0, 0)
    n = 0



#------------------------------SET UP------------------------------
# Creating and setting up main window
root = Tk()
root.title('test')
root.geometry('800x782+600+100')
root.configure(background='white')

# Creating and setting up canvas for drawing
canvas = Canvas(root, height=600, width=600, background='white')
canvas.create_oval(0, 0, 50, 50, fill='lightgrey', tag='shadow')
canvas.pack(fill=X)

# Canvas functions
canvas.bind("<Button-2>", mouse_m_click)
canvas.bind("<Button-3>", mouse_r_click)

canvas.bind("<Motion>", mouse_motion)
canvas.bind("<B1-Motion>", drag_motion)

# Buttons
paint_btn = Button(root, text='Paint graph', command=painting, font=("", 25))
reset_btn = Button(root, text='Reset', command=reset_nodes, font=("", 25))
clear_btn = Button(root, text='Clear', command=clear_graph, font=("", 25))

paint_btn.pack(fill=BOTH)
reset_btn.pack(fill=BOTH)
clear_btn.pack(fill=BOTH)

root.mainloop()
