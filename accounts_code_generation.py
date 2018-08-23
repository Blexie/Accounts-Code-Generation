"""Script to generate account codes for use in Opera 3."""
#######################################################
#REQUIREMENTS#
import datetime
import argparse
import pandas
#END OF REQUIREMENTS#
PARSER = argparse.ArgumentParser(
    description="Script to generate the SN_ACCOUNT field for use in Opera 3.")
#CLI ARGUMENTS#
PARSER.add_argument("input", help="""
    Input file. Required headers: 
   'Forename'
   'Surname'
   'Address1'
   'Address2'
   'Address3'
   'Address4'
   'Postcode'
   'Email'
   'PersonalEmail'""", type=str)

PARSER.add_argument("output",
                    help="Output file", type=str)

GRADUATE_PARSER = PARSER.add_mutually_exclusive_group(required=True)

GRADUATE_PARSER.add_argument("--graduates",
                             help="For input files of graduates.",
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

#Import CSV and rename the columns#
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
    if ord('A')+((datetime.datetime.now().year - 2010)% 26) >= 71:
        INITIAL = chr(ord('A')+((datetime.datetime.now().year - 2009)% 26))
    else:
        INITIAL = chr(ord('A')+((datetime.datetime.now().year - 2010)% 26))

#Final glue and output#
FINAL = pandas.DataFrame([''.join(map(str, i))
                          for i in zip
                          ([INITIAL + str(SHORTYEAR) + n for n in SHORTSURNAME], COUNTER)],
                         columns=["SN_ACCOUNT"])

#Rename Columns#
IN_CSV.rename(columns={
    'Forename':'Forename',
    'Surname':'Surname',
    'Address1':'SN_ADDR1',
    'Address2':'SN_ADDR2',
    'Address3':'SN_ADDR3',
    'Address4':'SN_ADDR4',
    'Postcode':'SN_PSTCODE',
    'Email':'SN_EMAIL',
    'PersonalEmail':'SN_ORDMAIL'
    }, inplace=True)
#Insert new columns#
IN_CSV.insert(loc=0, column='SN_ACCOUNT', value=FINAL)
IN_CSV.insert(loc=1, column='SN_NAME', value=IN_CSV.Forename+' '+IN_CSV.Surname)
IN_CSV.insert(loc=8, column='SN_TELENO', value='')
IN_CSV.insert(loc=9, column='SN_CUSTYPE', value='UN')
IN_CSV.insert(loc=10, column='SN_TPRFL', value='STUDENT')
IN_CSV.insert(loc=11, column='SN_CPRFL', value='STANDARD')
IN_CSV.insert(loc=13, column='SN_FCREATE', value='')
IN_CSV['SN_EMAILST'] = 'T'
IN_CSV['SN_DOCMAIL'] = '8'
del IN_CSV['Forename']
del IN_CSV['Surname']
#Out#
IN_CSV.to_csv(OUTFILE, index=False)
