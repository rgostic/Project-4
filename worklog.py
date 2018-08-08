import datetime
import re

from peewee import *
from collections import OrderedDict


db = SqliteDatabase('worklog.db')

class LogEntry(Model):
	employee_name = TextField()
	duration = IntegerField(default=0)
	task_name = TextField()
	notes = TextField()
	timestamp = DateTimeField(default=datetime.datetime.now)

	class Meta:
		database = db

def initialize():
	db.connect()
	db.create_tables([LogEntry], safe=True)


def menu_loop():
	'''show the menu'''
	choice = None

	while choice != 'q':
		
		print("Main Menu - (q) to quit")
		print("=========")
		for input_term, input_function in menu.items():
			print('{}) {}'.format(input_term, input_function.__doc__))
		choice = get_user_choice()

		if choice in menu:
			menu[choice]()


def add_entry():
	'''Add worklog entry to database'''
	employee_name = input("Please enter the employee name:\n")
	task_name = input("Please enter a task name:\n")
	duration = input("Please enter a duration (min):\n")
	notes = input("Please enter your notes:\n")

	LogEntry.create(
		employee_name = employee_name,
		duration = duration,
		task_name = task_name,
		notes = notes
	)


def _show_all_entries():
	'''show all the entries'''
	entries = LogEntry.select()

	for entry in entries:
		print_log_entry(entry)


def display_search_options():
	'''Get a list of search options'''	
	choice = None
	print("Worklog Search Options")
	print("======================")
	for input_term, input_function in search_options.items():
		print('{}) {}'.format(input_term, input_function.__doc__))
	choice = get_user_choice()

	if choice in search_options:
		search_options[choice]()


def show_employee_list():
	'''Prints employee list to console'''	
	print("Employees with log entries")
	print("==========================")
	employees = set()
	employee_dict = {}
	for e in LogEntry.select():
		employees.add(e.employee_name)

	for i, e in enumerate(employees):
		employee_dict[str(i)] = e
		print("{}) {}".format(i,e))

	return employee_dict


def get_by_employee_list():
	'''By employee list'''	

	lookup = show_employee_list()
	user_input = get_user_choice()
	#handle error
	selected_employee = lookup[user_input]
	
	result = LogEntry.select().where(LogEntry.employee_name.contains(selected_employee))
	print("Log Entries By: {}".format(selected_employee))
	for log_entry in result:
		print_log_entry(log_entry)


def get_by_employee_name():
	'''By employee name'''
	employee_search = input("Please enter the name of the employee you would like to search for:\n")
	result = LogEntry.select().where(LogEntry.employee_name.contains(employee_search))
	print("Log Entries Matching Name: {}".format(employee_search))
	for log_entry in result:
		print_log_entry(log_entry)


def show_date_list():
	'''Prints date list to console'''	
	print("Dates with log entries")
	print("==========================")
	dates = set()
	dates_dict = {}
	for e in LogEntry.select():
		dates.add(e.timestamp.date())

	for i, e in enumerate(dates):
		dates_dict[str(i)] = e
		print("{}) {}".format(i,e))

	return dates_dict

def get_by_date():
	'''By date'''
	lookup = show_date_list()
	user_input = get_user_choice()
	selected_date = lookup[user_input]

	result = LogEntry.select().where(LogEntry.timestamp.date() == selected_date)
	print("Log Entries For: {}".format(selected_date))
	for log_entry in result:
		print_log_entry(log_entry)


def get_by_duration():
	'''By Duration'''
	duration_search = input("Please enter the duration of the task you would like to search for:\n")
	duration_int = int(duration_search)
	result = LogEntry.select().where(LogEntry.duration == duration_int)
	print("Log Entries Matching Duration: {}min".format(duration_search))
	for log_entry in result:
		print_log_entry(log_entry)


def get_by_search_term(search_term):
	'''By search term'''
	pass


def print_log_entry(entry):
	'''pretty print a worklog entry to console'''
	print()
	print("\t| {} |".format(entry.task_name))
	print("\t" + "="*(len(entry.task_name)+4))
	print("\tEmployee: {}".format(entry.employee_name))
	print("\tDuration: {}min".format(entry.duration))
	print("\tDate: {}".format(entry.timestamp))
	print("\tNotes: {}".format(entry.notes))
	print()

	
def get_user_choice():
	return input(">>> ").lower().strip()


menu = OrderedDict([
	('a', add_entry),
	('s', display_search_options)
])

search_options = OrderedDict([
	('e', get_by_employee_list),
	('x', get_by_employee_name),
	('d', get_by_date),
	('t', get_by_duration),
	('s', get_by_search_term)
])


if __name__ == "__main__":
	initialize()
	menu_loop()
