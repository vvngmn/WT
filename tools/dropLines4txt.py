import os,sys

def makeTxt(bookname):
	old = os.getcwd()+'\\'+bookname
	new = os.getcwd()+'\\'+bookname.split('.')[0]+'_new.txt'

	oldfile = open(old,'r')
	newfile = open(new,'w')
	s=''
	for line in oldfile.readlines():
		s=s+line.split('\n')[0]
	newfile.write(s)

	oldfile.close()
	newfile.close()

if __name__ == '__main__':
	makeTxt(bookname='Sex_and_the_city.txt')



