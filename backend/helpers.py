from datetime import date

def fun_daysDiff(date_ini, date_end):
	diff = date_end - date_ini
	return diff.days

def format_currency(value):
	return "{:,.2f}".format(value)
