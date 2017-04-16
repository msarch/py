from curses import initscr,curs_set,newwin,endwin,KEY_RIGHT,KEY_LEFT,KEY_DOWN,KEY_UP;from random import randrange;initscr();curs_set(0);win = newwin(16,60,0,0);win.keypad(1);win.nodelay(1);win.border('|','|','-','-','+','+','+','+');win.addch(4,44,'O');snake = [ [30,7],[29,8],[28,7],[27,7],[26,7],[25,7] ];key = KEY_RIGHT
while key != 27:
    win.addstr(0,2,' Score: '+str(len(snake)-6)+' ')
    win.timeout(180+ ( (len(snake)-6) % 10- (len(snake)-6) ) * 3 )
    getkey = win.getch()
    key = key if getkey==-1 else getkey
    snake.insert(0,[snake[0][0]+(key==KEY_RIGHT and 1 or key==KEY_LEFT and -1), snake[0][1]+(key==KEY_DOWN and 1 or key==KEY_UP and -1)])
    win.addch(snake[len(snake)-1][1],snake[len(snake)-1][0],' ')
    if win.inch(snake[0][1],snake[0][0]) & 255 == 32: snake.pop()
    elif win.inch(snake[0][1],snake[0][0]) & 255 == ord('O'):  
        c = [n for n in [[randrange(1,58,1),randrange(1,14,1)] for x in range(len(snake))] if n not in snake]
        win.addch(c == [] and 4 or c[0][1],c == [] and 44 or c[0][0],'O')
    else: break
    win.addch(snake[0][1],snake[0][0],'X')
endwin();print '\n  Snake15l.PY (by Kris Cieslak),\n  Thanks for playing, your score: '+str(len(snake)-7)+'\n'

"""
Snake.PY-15lines by Kris Cieslak (defaultset.blogspot.com)
         
Controls:  Left,Right,Up,Down - move
           ESC -quit         

Linux/python 2.6.5
"""