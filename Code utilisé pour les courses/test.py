'''
Programme de tests de la fonctionnalité qui permet de donner des ordres à la voiture même une fois que le code a été lancé.
Tout a été implémenté ensuite dans la fonction main.py
'''
import curses
import time
window=curses.initscr()
window.nodelay(True)
while True:
	key=window.getch()
	if key==97:
		curses.endwin()
		break
	
