"""
Had to save the outputed file from txt_to_csv.py in another format, 
asccii, from 'save as' in OpenOffice Calc and it had spaces 
every-other character, and when it was saved it also had "" marks
added. This program stripped them and the white space, I removed the 11 headers by hand.
"""
import os

PATH = "/home/fox/Desktop/Tax"

OUTPUT_LIST = []
def text_doc_opener(document):
	inputFileName = os.path.join(PATH, document)	
	with open(inputFileName, "r") as myInputFile:
		line_list = myInputFile.readlines()

		for line in line_list:
			line = line[::2]
			line = line.translate(None, '"')
			line = line.rstrip()
			line = line.replace(" ", "")
			OUTPUT_LIST.append(line)

		count = 0
		for line in line_list:
			count += 1
		print OUTPUT_LIST
		print count

	OUTPUT_STRING = ','.join(OUTPUT_LIST)
	with open("formatted_csv.csv", "r+") as myOutputFile:
	 	myOutputFile.write(OUTPUT_STRING)
	
text_doc_opener('tax_1099_retry7.csv')
