#######################################################
#REQUIREMENTS#
import datetime
import csv
import pandas
import argparse
from collections import defaultdict
#END OF REQUIREMENTS#
parser = argparse.ArgumentParser(description="Script to generate account codes for use in Opera 3.")
#CLI ARGUMENTS#
parser.add_argument("input", help="Input file", type=str)
parser.add_argument("output", help="Output file", type=str)
graduate_parser = parser.add_mutually_exclusive_group(required=True)
graduate_parser.add_argument("--graduates", help="For input of Graduates.", dest="graduates", action='store_true')
graduate_parser.add_argument("--no-graduates", help="For input files of non-Graduates.", dest="graduates", action='store_false')
#END OF CLI ARGUMENTS#
args = parser.parse_args()
#Variables#
infile = args.input
outfile = args.output
graduates = args.graduates

#MAGIC#
columns = defaultdict(list)
#Import CSV in sensible format#
with open(infile) as f:
	reader = csv.reader(f)
	next(reader)
	for row in reader:
		for (i,v) in enumerate(row):
			columns[i].append(v)
#First 3 characters of surname#
shortsurname = []
for surname in columns[1]:
	shortsurname.append(surname.ljust(3, '0').upper()[:3])
#Find any duplicates after truncation, and count them#
shortsurnamecount = pandas.DataFrame(shortsurname, columns=['A']).groupby('A').cumcount()

counter = [str(i).zfill(2) for i in shortsurnamecount+1]

#Put the year in the code field#
shortyear = abs(datetime.datetime.now().year) % 100

#Decide what to put at the start of the code#
if graduates == True:
        initial = 'G'
else:        
        if (datetime.datetime.now().year - 2010)% 25 >= 7:
                initial = chr(ord('A')+((datetime.datetime.now().year - 2011)% 25+1))
        else:
                initial = chr(ord('A')+((datetime.datetime.now().year - 2011)% 25))
        

#Final glue and output#
final = pandas.DataFrame([''.join(map(str, i)) for i in zip([initial + str(shortyear) + n for n in shortsurname], counter)], columns=["Code"])
in_csv = pandas.read_csv(infile)
in_csv['Code'] = final
in_csv.to_csv(outfile, index=False)
