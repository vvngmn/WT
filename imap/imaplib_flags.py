#!/bin/python
'store flags to the specific account, copy to sepecific folder.'

import imaplib

def addFlag(user):
    mailbox=imaplib.IMAP4(host='10.17.224.23', port=2143)
    mailbox.login(user,user)
    mailbox.select('inbox')
    mailbox.store('1:*', '+flags', '\seen test 123')
    mailbox.create('1/2/3')
    mailbox.copy('1:*', '1/2/3')
    mailbox.logout()
    

users=('t1','t2','t3')
for user in users :
    addFlag(user)
    


    
    #typ,datas=mailbox.search(None,'all')
    #print typ
    #print datas
    #for i in datas[0].split():
    #    mailbox.store(i, '+flags', '\\flagged test')
