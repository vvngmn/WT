import sys, getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
except getopt.GetoptError:
    print "help information and exit"