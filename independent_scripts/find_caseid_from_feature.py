# keyword = app_repo
# grep -l $keyword features/tierN/web/admin-console/* | xargs python find_caseid.py $keyword 

import sys

for file in sys.argv[2:]:
	f = open(file)
	list = f.read().split(sys.argv[1])
	list.pop()
	for i in list: print file + ": " + i.split('# @case_id ')[-1].split(' ')[0]
	f.close()