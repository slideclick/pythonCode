datepat = re.compile('(?P<mon>\d+)/(\d+)/(\d+)')
text = "Guido will be out of the office from 12/15/2012 - 1/3/2013."
datepat.sub(r'\2/\g<mon>/\3', text)
