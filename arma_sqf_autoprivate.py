#-------------------------------------------------------------------------------
# SQF autoprivate
# Collect all private variables in the script
#-------------------------------------------------------------------------------
from tkinter import Tk
import re

def main():
	t=Tk()
	t.withdraw()
	text=t.clipboard_get()
	#text="_example=2345..."
	r=re.compile("(_[A-z]+(?==))")
	m=list(set(r.findall(text)))
	m=str(m).translate(str.maketrans("'",'"'))
	print(m)
	t.clipboard_clear()
	t.clipboard_append(m)
	t.destroy()

if __name__ == '__main__':
	main()
