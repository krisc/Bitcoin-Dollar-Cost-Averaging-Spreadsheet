# TODO: Download .csv from CashApp
# Let's experiment with interacting with .csv from CashApp
import csv, openpyxl
cashFile = open('square_cash_report.csv')
reader = csv.reader(cashFile)
cashData = list(reader)

# TODO: filter and edit .csv into form of .xlsx
# let's only keep rows that have the 'Transaction Type' column as 'Bitcoin buy'
# That is every row starting with one, check to see column 10. we'll accumulate a list of rows
csvRows = []
print("Gathering relevant entries from .csv file...")

# For tutorial, first show this block without filtering for relevant columns
# i.e., csvRows.append(cashData[row])
for row in range(len(cashData)-1, 0, -1):
	if cashData[row][10] == 'Bitcoin Buy':
		date = cashData[row][3]
		usd_paid = cashData[row][6][2:]
		btc_received = cashData[row][2]
		btc_string_length = len(btc_received[17:])
		btc_received = btc_received[17:17+btc_string_length-1]

		usd_float = float(usd_paid)
		btc_float = float(btc_received)
		exchange_rate = usd_float / btc_float
		csvRows.append([date, usd_paid, btc_received, exchange_rate])

print("Relevant entries stored.")

# we loop through the list starting from the end to get the entries in ascending order.
# we also strip some of the strings of unnecessary characters

# TODO: append data from .csv to .xlsx
# Now we are ready to add these rows to the .xlsx file

wb = openpyxl.Workbook()
sheet = wb.active

# first, let's set the first row to name the columns
sheet['a1'] = 'Date'
sheet['b1'] = 'USD paid'
sheet['c1'] = 'BTC received'
sheet['d1'] = 'Exchange Rate'
sheet['f1'] = 'Total USD Paid'
sheet['g1'] = 'Total BTC received'
sheet['h1'] = 'Weighted Dollar-cost Average'

# now we can loop through the entries from the csv and add them to the rows of the spreadsheet
print("Appending entries to spreadsheet...")
for i in range(len(csvRows)):
	for j in range(len(csvRows[row])):
		cell = sheet.cell(row=(i + 2), column=(j + 1))
		val = csvRows[i][j]
		if j == 0:
			cell.value = val
		elif j == 3:
			cell.value = '=ROUND(B' + str(i + 2) + '/C' + str(i + 2) + ', 2)'
		else:		
			cell.value = float(val)


# TODO: enter formulas into spreadsheet
sheet['f2'] = '=SUM(B2:B' + str(sheet.max_row) + ')'
sheet['g2'] = '=SUM(C2:C' + str(sheet.max_row) + ')'
sheet['h2'] = '=ROUND(F2/G2, 2)'

# TODO: print how much you paid in USD, print how much you have in BTC, and print the dollar cost average

# TODO: save .xlsx
print("Saving spreadsheet as 'btc_dca.xlsx'")
wb.save('btc_dca.xlsx')