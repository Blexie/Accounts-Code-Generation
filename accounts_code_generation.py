"""Script to generate account codes for use in Opera 3."""
#######################################################
#REQUIREMENTS#
import datetime
import argparse
import pandas
#END OF REQUIREMENTS#
PARSER = argparse.ArgumentParser(description="Script to generate account codes for use in Opera 3.")
#CLI ARGUMENTS#
PARSER.add_argument("input",
                    help="Input file", type=str)

PARSER.add_argument("output",
                    help="Output file", type=str)

GRADUATE_PARSER = PARSER.add_mutually_exclusive_group(required=True)

GRADUATE_PARSER.add_argument("--graduates",
                             help="For input of graduates.",
                             dest="graduates",
                             action='store_true')


GRADUATE_PARSER.add_argument("--no-graduates",
                             help="For input files of non-graduates.",
                             dest="graduates",
                             action='store_false')

#END OF CLI ARGUMENTS#
ARGS = PARSER.parse_args()
#Variables#
INFILE = ARGS.input
OUTFILE = ARGS.output
GRADUATES = ARGS.graduates
#End of Variables#

IN_CSV = pandas.read_csv(INFILE)

#First 3 characters of surname#
SHORTSURNAME = []
for surname in IN_CSV['Surname']:
    SHORTSURNAME.append(surname.ljust(3, '0').upper()[:3])
#Find any duplicates after truncation, and count them#
SHORTSURNAMECOUNT = pandas.DataFrame(SHORTSURNAME, columns=['A']).groupby('A').cumcount()

COUNTER = [str(i).zfill(2) for i in SHORTSURNAMECOUNT+1]

#Put the year in the code field#
SHORTYEAR = abs(datetime.datetime.now().year) % 100

#Decide what to put at the start of the code#
if GRADUATES:
    INITIAL = 'G'
else:
    if (datetime.datetime.now().year - 2010)% 25 >= 7:
        INITIAL = chr(ord('A')+((datetime.datetime.now().year - 2011)% 25+1))
    else:
        INITIAL = chr(ord('A')+((datetime.datetime.now().year - 2011)% 25))

#Final glue and output#
FINAL = pandas.DataFrame([''.join(map(str, i))
                          for i in zip
                          ([INITIAL + str(SHORTYEAR) + n for n in SHORTSURNAME], COUNTER)],
                         columns=["Code"])
IN_CSV['Code'] = FINAL
IN_CSV.to_csv(OUTFILE, index=False)
