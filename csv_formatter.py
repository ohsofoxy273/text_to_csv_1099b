"""
Had to save the outputed file from txt_to_csv.py in another format, asccii and it had spaces every-other character, and when
it was saved it also had "" marks added. This program stripped them and the white space, I removed the 11 headers by hand.
"""
import os

path = "/home/fox/Desktop/Tax"

def text_doc_opener(document):
	inputFileName = os.path.join(path, document)	
	output_list = []
	with open(inputFileName, "r") as myInputFile:
		line_list = myInputFile.readlines()

		for line in line_list:
			line = line[::2]
			line = line.translate(None, '"')
			line= line.rstrip()
			output_list.append(line)

		count = 0
		for line in line_list:
			count += 1
		print output_list
		print count

	with open("formatted_csv.csv", "w") as myOutputFile:
		myOutputFile.writelines(output_list)



text_doc_opener('tax_1099_retry7.csv')
