import sqlite3

# create or open a database file
conn = sqlite3.connect('storage/emulated/0/SWING_MUSIC/swing_music.db') 

# ??? dunno what it is but it's needed
c = conn.cursor()

###############################################################
def show_songs(query):
	# run SQL query
	c.execute(query)
	print("##########################################")
	print("Title - Artist")
	print("Kicks_PM, BPM, Good_for, Dance_rating")
	print("##########################################")
	print("------------------------------------------")
	
	# on my phone there are just 42 chars in a line
	# so let's only print Title and Artist in 1 line
	# and the rest in 2nd line
	for row in c.fetchall():
		print(row[0], "-", row[1])
		info_row = ""
		for i in range(2, 5):
			info_row += str(row[i]) + ", "
		print(info_row + str(row[5]))
		print("------------------------------------------")
	print("##########################################")
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
	# build big ass query bit by bit, but it's less readable
	# and probably less efficient

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
	# grab data from SQL query (sadly no numpy)
	data = c.fetchall()

	# a line - my phone terminal is 42 chars wide
	print("#"*42)
	for header in headers:
		print(header + "; ", end="")
	# another line
	print("\n" + "#"*42)
	print("-"*42)

	for row in data:
		for element in row:
			print(str(element) + "; ", end="")
		print()
		print("-"*42)
	print("#"*42)

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
