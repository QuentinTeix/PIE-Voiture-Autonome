import curses
import time
window=curses.initscr()
window.nodelay(True)
while True:
	key=window.getch()
	if key==97:
		curses.endwin()
		break
	
