import sqlite3 # database management
import numpy as np
from sty import fg, bg, ef, rs # colors in terminal

# choose font colors
orange = fg(172)
grey = fg(243)
grey_bg = bg(234)

# activate this if colors don't work on windows
#from colorama import init
#init()


# create or open a database file
conn = sqlite3.connect('swing_music.db') 

# ??? dunno what it is but it's needed
c = conn.cursor()

###############################################################
def show_songs(query):
	# run SQL query
	c.execute(query)
	# grab data from SQL query
	data = np.array(c.fetchall())
	
	# convert values to strings (needed for lengths of integers)
	data_str = data.astype(str)

	# convert array to a one containing object types, which 
	# allows for inserting lists into cells
	data_str = data_str.astype(object)


	# column width will be as follows (one space in between):
	# title artist kicks_pm bpm good_for dance_rating 
	# 29    29     9        4   29       14
	# adjustable column widths was hard to do because if the 
	# names are too long the song goes to the next line (which
	# looks bad), and if I block it in terminal then some info 
	# goes out the screen and can't be seen
	# Therefore I give each song 2 lines so it fits for sure
	# and fix column widths
	col_width = [29, 29, 9, 4, 29, 14]

	title_row = ["Title", "Artist", "Kicks_PM", "BPM", \
				"Good_for", "Dance_rating"]

	# choose orange font for column names
	print(orange, end="")
	# print column names
	for i in range(len(title_row)):
		title_row[i] += " " * (col_width[i] - len(title_row[i]))
		print(title_row[i], end=" ")
	print()

	# a line - my macOS terminal is 119 chars wide 
	print("-" * 119)	

	# ok let's go
	# a cool way to iterate over 2D numpy arrays
	for y, x in np.ndindex(data_str.shape):
		temp = data_str[y, x]
		
		# if name is longer than column is wide
		if len(temp) > col_width[x]:
			
			# if there are no spaces in it, just cut it
			if " " not in temp[0:col_width[x]+1]:
				temp_up = temp[0:col_width[x]]
				temp_down = temp[col_width[x]:]
				# if name is so long it goes out of 2nd row, cut it
				if len(temp_down) > col_width[x]:
					temp_down = temp_down[0:col_width[x]]
			
			# if there ARE spaces in it
			else:
				# find the last space before column ends and cut it
				for i in range(col_width[x]):
					if temp[col_width[x]-i] == " ":
						temp_up = temp[0:col_width[x]-i]
						temp_down = temp[col_width[x]-i+1:]
						break

		# if name is not longer than the column we still need an 
		# up-row and down-row, even if empty
		else:
			temp_up = data_str[y, x]
			temp_down = ""

		# fill with spaces until column is full
		temp_up += " "*(col_width[x] - len(temp_up))
		temp_down += " "*(col_width[x] - len(temp_down))
		# save up and down rows as lists in place of names
		data_str[y, x] = [temp_up, temp_down]

	# let's print it finally
	counter = 0
	for song in data_str:
		# choose color, every other line gets grey background
		if counter % 2 == 0:
			print(rs.all, end="") # reset colors
		else:
			print(grey_bg, end="") # grey background

		# create a first line and 2nd line for the song
		row_up = ""
		row_down = ""
		for cell in song:
			# if it's not the first element, add space and next
			# element
			if row_up != "":
				row_up += " " + cell[0]
			# if it's the first element, just add it alone
			else:
				row_up += cell[0]

			# same for the down-row
			if row_down != "":
				row_down += " " + cell[1]
			else:
				row_down += cell[1]
		print(row_up)
		# rs.all resets all colors to normal
		print(row_down, rs.all)
		counter += 1

###############################################################

###############################################################
def add_song():
	# Aiming for:
	# INSERT INTO songs (col1, col2, etc)
	# VALUES (val1, val2, etc);

	# if we want to pass python variables into SQL queries,
	# we can do it like this:
	# INSERT INTO songs (%s, %s, etc)
	# VALUES (?, ?, etc);
	# so we mark column names and operands (=, >, etc) with %s,
	# and values with ?

	# then it's like 
	# c.execute(query % (col1, col2), (value1, value2))

	# or of course we can convert everything into strings and
	# build the query bit by bit

	# here I don't know how many values will be specified, so
	# I can't specify in advance how many %s should be in the 
	# query, hence the brute way

	print("### Adding a song ###")
	Title = input(">>> Title: ")
	Artist = input(">>> Artist: ")
	Kicks_PM = input(">>> Kicks Per Minute: ")
	if Kicks_PM != "":
		BPM = str(2*int(Kicks_PM))
		print(">>> BPM:", BPM)
	else:
		BPM = ""
	Good_for = input(">>> Good for: ")
	Dance_rating = input(">>> Dance rating: ")

	# so column names I made the brute way, straight adding next
	# names if the parameters were filled
	# and for values I built strings of "?, ", which on 2nd 
	# thought might not be the most proper way to do it,
	# but yeah... it works and it's already done :D

	columns = "("
	values = "("
	variables = []
	if Title != "":
		columns += "Title, "
		values += "?, "
		variables.append(Title)
	if Artist != "":
		columns += "Artist, "
		values += "?, "
		variables.append(Artist)
	if Kicks_PM != "":
		columns += "Kicks_PM, "
		values += "?, "
		variables.append(int(Kicks_PM))
	if BPM != "":
		columns += "BPM, "
		values += "?, "
		variables.append(int(BPM))
	if Good_for != "":
		columns += "Good_for, "
		values += "?, "
		variables.append(Good_for)
	if Dance_rating != "":
		columns += "Dance_rating, "
		values += "?, "
		variables.append(int(Dance_rating))

	columns = columns[0:-2] + ")"
	values = values[0:-2] + ")"
	variables = tuple(variables)

	query = "INSERT INTO songs " + columns + \
		" VALUES " + values + ";"

	c.execute(query, variables)
	conn.commit()
###############################################################

###############################################################
def delete_song():
	# Aiming for:
	# DELETE FROM songs
	# WHERE column_name = something;

	conditions = []

	print("Specify a song by typing:\n" + \
	"column_name operand(>, =, etc) value\n")
	x = input(">>> ")

	if x == "":
		print("Song(s) not specified")
		return

	y = x.split()
	# if name has more than 1 word we need to join it together
	if len(y) > 3:
		for i in range(3, len(y)):
			y[2] += " " + y[i]

	c.execute("""
		DELETE FROM songs
		WHERE %s %s ?;
	""" % (y[0], y[1]) , tuple([y[2]]) )
	conn.commit()
###############################################################

###############################################################
def is_it_a_number(value):
	try:
		temp = int(value)
	except ValueError:
		return False
	return True

def edit_song():
	# Aiming for:
	# UPDATE songs
	# SET column_name = something, column_name2 = something2, etc
	# WHERE column_name = something;

	print("### Edit ###")

	print("What?")
	print("column_name = value")
	x = input(">>> ").split()
	
	# if value is a string
	if is_it_a_number(x[2]) == False:
		# if name has more than 1 word we need to join it together
		if len(x) > 3:
			for i in range(3, len(x)):
				x[2] += " " + x[i]
		# string values in SQL queries need "" 
		x[2] = '"' + x[2] + '"'

	print("\nAssign:")
	print("column_name = value (one change = one line)")
	y = [""]
	i = 0
	while True:
		y[i] = input(">>> ").split()
		# if nothing written, query is over
		if y[i] == []:
			break
		# if something is written
		else:
			# and it's a string 
			if is_it_a_number(y[i][2]) == False:
				# and if name has more than 1 word, we need to
				# join it together
				if len(y[i]) > 3:
					for j in range(3, len(y[i])):
						y[i][2] += " " + y[i][j]

				# then strings also need these "" in SQL query
				y[i][2] = '"' + y[i][2] + '"'

			i += 1
			y.append("")

	### building the query bit by bit
	query = "UPDATE songs SET "

	for j in range(i):
		query += y[j][0] + ' = ' + y[j][2] + ', ' \
	
	# cut the ", " from the end and add space to continue query
	query = query[0:-2] + " "
	query += "WHERE " + x[0] + ' = ' + x[2] + ';' 
	###

	c.execute(query)
	conn.commit()
###############################################################

###############################################################
def show_custom(query):
	# run SQL query
	c.execute(query)
	# grab headers
	headers = [i[0] for i in c.description]
	# grab data from SQL query
	data = np.array(c.fetchall()).astype(str)

	# print headers in orange
	print(orange, end="")
	for header in headers:
		print(header + "; ", end="")
	# a line - my macOS terminal is 119 chars wide 
	print("\n" + "-" * 119, rs.all)

	# print data - every other line has grey font
	counter = 0
	for row in data:
		if counter % 2 == 1:
			print(grey, end="")
		
		for element in row:
			print(element + "; ", end="")
		
		# reset colors
		print(rs.all)
		counter += 1

def custom_query():
	print("Your query, Sir (type 'exit' to return to menu)")
	proceed = True
	while proceed == True:
		y = ""
		while True:
			x = input(">>> ")
			# if empty line, query is over
			# I could do it with ";", but this forces nice 
			# formatting
			if x == "":
				break
			# if I type exit, return to main menu
			elif x == "exit":
				proceed = False
				break
			# if something is already in the query
			if y != "":
				# if there is no space at the end
				if y[-1] != " ":
					# add it (spaces are enough, SQL queries can
					# be written in one line)
					y += " "
			# add line to query
			y += x

		# if we want to see something that has all columns, use
		# our super neat showing function
		if "SELECT * FROM" in y:
			show_songs(y)
		else:
			# if not all the columns, show it raw
			# Some queries may have things like COUNT(*), or
			# AVG(Dance_rating), so it's very hard to create 
			# one beautiful template that would show all
			# possible queries properly in terminal.
			# At least I can make headers and the line orange,
			# and print every other line in different font color.
			if "SELECT" in y:
				show_custom(y)
			# if it's not a show-me-something query, just do it
			else:
				c.execute(y)
				conn.commit()
###############################################################


###############################################################
################          MAIN MENU          ##################
###############################################################
while True:
	action = int(input("""
		1 -> show songs
		2 -> add a song
		3 -> edit song
		4 -> delete song
		5 -> exit
		0 -> custom query mode
		"""))
	print('')

	if action == 1:
		show_songs('SELECT * FROM songs ORDER BY BPM;')
	elif action == 2:
		add_song()
	elif action == 3:
		edit_song()
	elif action == 4:
		delete_song()
	elif action == 5:
		break
	elif action == 0:
		custom_query()
###############################################################
###############################################################
###############################################################

# after all is done close the database file
conn.close()

