"""
Tax form 1099b from broker came as scanned PDF. 
The document had many lines of trading from the year's rebalancing and purchases, and I didn't want to enter it by hand.
I used ghost script to convert the PDF to PNG, which automatically made 19 png files from the 19 page PDF

in the bash (zsh) shell I used ImageMagick with Ghostscript, entering the following in the terminal:

$ convert -density 300 Document_2222014_44439_PM_ZDYE6NXB.pdf -depth 8 Document_2222014_44439_PM_ZDYE6NXB.png

Then in the terminal I used tesseract OCR with a bash script:

$ for i in *.png ; do tesseract $i page$i; done;

This process converted PDF -> PNG -> TXT 

With some cleanup of the text docs, I was able to use the following script to make a CSV file, and then upload it
to an online tax center.

"""



import re, os, csv

path = "/home/fox/Desktop/Tax"

csv_header = ["Date of sale or exchange",
"Date of Acquisition",
"Description",
"Symbol",
"Cusip",
"Quantity Sold",
"Sales Price Less Commissions", 
"Cost or Other Basis",
"Wash Sale Loss Disallowed",
"Income Tax Withheld",
"Loss Not Allowed"]

# make the csv file and add the headers
with open(os.path.join(path, "tax_1099.csv"), "wb") as myFile:
	myFileWriter = csv.writer(myFile)
	myFileWriter.writerows(csv_header)


def text_doc_opener(document):
	# for i in range(3, 20):
	# 	inputFileName = os.path.join(path, "pageDocument_2222014_44439_PM_ZDYE6NXB-%s.txt" %i)
	inputFileName = os.path.join(path, document)	
	myInputFile = open(inputFileName, "r")
	return myInputFile.read()

# find a line in the file
def line_finder(input_list):
	match = re.search(r'(\d+/\d+/\d+ \d+/\d+/\d+ .+)', input_list)
	line = match.group()
	return line

def header_1_finder(line):
	match = re.search(r'(\d+/\d+/\d+ \d+/\d+/\d+)', line_finder(line))
	dates = match.group()
	first_date =  re.search(r'(\d+/\d+/\d+)', dates)
	return first_date.group()

def header_2_finder(line):
	match = re.search(r'(\d+/\d+/\d+ \d+/\d+/\d+)', line_finder(line))
	dates = match.group()
	second_date =  re.search(r'( \d+/\d+/\d+)', dates)
	return second_date.group().lstrip()

def header_3_finder(line):
	match = re.search(r'(\d+/\d+/\d+ \d+/\d+/\d+ \w+)', line_finder(line))
	group = match.group()
	symbol =  re.search(r'([A-Z]+)', group)
	return symbol.group()

def header_4_finder(line):
	match = re.search(r'([A-Z])+ ([0-9]+)', line_finder(line))
	group = match.group()
	symbol =  re.search(r'([A-Z]+)', group)
	return symbol.group()

def header_5_finder(line):
	match = re.search(r'([A-Z])+ ([0-9]+)', line_finder(line))
	group = match.group(2)
	return group

def header_6_finder(line):
	num_sold = re.search(r'(\d+.\d+) (\$\d+.\d+)', line_finder(line))
	return num_sold.group(1)


def header_7_finder(line):
	sales_price = re.search(r'(\d+.\d+) (\$\d+.\d+)', line_finder(line))
	return sales_price.group(2)

def header_8_finder(line):
	cost = re.search(r'(\$\d+.\d+) (\$\d+.\d+)', line_finder(line))
	return cost.group(2)

def header_9_finder(line):
	end_line = re.search(r'(\$\d+.\d+) (\$\d+.\d+) (.+)', line_finder(line))
	end_line = end_line.group(3)
	wash = re.search(r'\S+ ', end_line)
	return wash.group()

def header_10_finder(line):
	end_line = re.search(r'(\$\d+.\d+) (\$\d+.\d+) (.+)', line_finder(line))
	end_line = end_line.group(3)
	tax_withheld = re.search(r'(\S+) (\S+)', end_line)
	return tax_withheld.group(2)

def header_11_finder(line):
	end_line = re.search(r'(\$\d+.\d+) (\$\d+.\d+) (.+)', line_finder(line))
	end_line = end_line.group(3)
	loss_not_allowed = re.search(r'\S \S (.+)', end_line)
	return loss_not_allowed.group(1)

#find all the appropriate lines
def file_scanner(input_file):
	myFile = text_doc_opener(input_file)
	line_list = re.findall(r'(\d+/\d+/\d+ \d+/\d+/\d+ .+)', myFile) #find all the appropriate lines
	
	# iterate through them and extract the data
	output = []
	for line in line_list:
		line_output = header_1_finder(line) + ", " + \
		header_2_finder(line) + ", " + \
		header_3_finder(line) + ", " + \
		header_4_finder(line) + ", " + \
		header_5_finder(line) + ", " + \
		header_6_finder(line) + ", " + \
		header_7_finder(line) + ", " + \
		header_8_finder(line) + ", " + \
		header_9_finder(line) + ", " + \
		header_10_finder(line) + ", " + \
		header_11_finder(line)
		output.append([line_output])
	return output

def document_iterator():
	for i in range(3, 20):
		inputFileName = os.path.join(path, "pageDocument_2222014_44439_PM_ZDYE6NXB-{}.png.txt".format(5))
		print file_scanner(inputFileName)		

document_iterator()
