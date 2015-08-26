#!/usr/bin/python fileencoding=utf-8:
import imaplib
import sys
import os
import getopt
import time
import codecs

def modified_base64(s):
    s_utf7 = s.encode('utf-7')
    return s_utf7[1:-1].replace('/', ',')

def modified_unbase64(s):
    s_utf7 = '+' + s.replace(',', '/') + '-'
    return s_utf7.decode('utf-7')

def encoder(s, errors=None):
    """
    Encode the given C{unicode} string using the IMAP4 specific variation of
    UTF-7.

    @type s: C{unicode}
    @param s: The text to encode.

    @param errors: Policy for handling encoding errors.  Currently ignored.

    @return: C{tuple} of a C{str} giving the encoded bytes and an C{int}
        giving the number of code units consumed from the input.
    """
    r = []
    _in = []
    for c in s:
        if ord(c) in (range(0x20, 0x26) + range(0x27, 0x7f)):
            if _in:
                r.extend(['&', modified_base64(''.join(_in)), '-'])
                del _in[:]
            r.append(str(c))
        elif c == '&':
            if _in:
                r.extend(['&', modified_base64(''.join(_in)), '-'])
                del _in[:]
            r.append('&-')
        else:
            _in.append(c)
    if _in:
        r.extend(['&', modified_base64(''.join(_in)), '-'])
    return (''.join(r), len(s))

def decoder(s, errors=None):
    """
    Decode the given C{str} using the IMAP4 specific variation of UTF-7.

    @type s: C{str}
    @param s: The bytes to decode.

    @param errors: Policy for handling decoding errors.  Currently ignored.

    @return: a C{tuple} of a C{unicode} string giving the text which was
        decoded and an C{int} giving the number of bytes consumed from the
        input.
    """
    r = []
    decode = []
    for c in s:
        if c == '&' and not decode:
            decode.append('&')
        elif c == '-' and decode:
            if len(decode) == 1:
                r.append('&')
            else:
                r.append(modified_unbase64(''.join(decode[1:])))
            decode = []
        elif decode:
            decode.append(c)
        else:
            r.append(c)
    if decode:
        r.append(modified_unbase64(''.join(decode[1:])))
    return (''.join(r), len(s))

class StreamReader(codecs.StreamReader):
    def decode(self, s, errors='strict'):
        return decoder(s)

class StreamWriter(codecs.StreamWriter):
    def encode(self, s, errors='strict'):
        return encoder(s)

_codecInfo = (encoder, decoder, StreamReader, StreamWriter)
try:
    _codecInfoClass = codecs.CodecInfo
except AttributeError:
    pass
else:
    _codecInfo = _codecInfoClass(*_codecInfo)

def imap4_utf_7(name):
    if name == 'imap4-utf-7':
        return _codecInfo

codecs.register(imap4_utf_7)

class ImapHandler:

    method = ""
    conn = None
    
    def __init__(self, user, passwd, host = "locahost", port = 143, debug = False, ssl = False):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.debug = debug
        self.ssl = ssl
        self.isLogin = False

    def __del__(self):
        if not self.conn:
            return

        self.conn.logout()
        if self.debug:
            self.conn.print_log()

    def run(self, method, argsList):
        if not method:
            return

        handler = getattr(self, "_handler_" + method, None)
        if not handler:
            return

        if len(argsList) != len(handler['parameters']):
            print "bad parameters !!!"
            if handler['parameters']:
                print "%s '%s'" % (method, "' '".join(handler['parameters']))
            else:
                print method
            return

        handler['method'](self, *argsList)

    def connect(self):
        if self.conn:
            return
        if self.ssl:
            self.conn = imaplib.IMAP4_SSL(self.host, self.port)
        else:
            self.conn = imaplib.IMAP4(self.host, self.port)

    def login(self):
        if self.isLogin:
            return

        res = self.conn.login(self.user, self.passwd)
        if res[0].upper() != 'OK':
            raise(exception('Failed to login'))
        self.isLogin = True 

    def do_append_mails(self, mailbox, path):

        mailbox = mailbox.encode('imap4-utf-7')
        self.mailCount = 0

        def handle_directory(path):

            for p in os.listdir(path):
                p = "%s/%s" % (path, p)
                if os.path.isdir(p):
                    handle_directory(p)
                else:
                    self.mailCount += 1
                    handle_file(p)

        def handle_file(path):
            with open(path) as f:
                message = f.read()
                res = self.conn.append(mailbox,None,None,message)

            if res[0].upper() != 'OK':
                print '%d, %s, %s, %s, %s' % (self.mailCount, mailbox, path, res[0], res[1])
            else:
                print '%d, %s, %s, %s' % (self.mailCount, mailbox, path, res[0])

        self.connect()
        self.login()

        if path.endswith('/'):
            path = path[:-1]

        print mailbox, path
        if os.path.isdir(path):
            handle_directory(path)
        else:
            handle_file(path)

    _handler_append_mails = {"method": do_append_mails, "parameters": ("mailbox", "path",)}

    def do_fetch_all(self):
        """
        download all mails
        """
        self.connect()
        self.login()
        res = self.conn.list()
        if res[0].upper() != 'OK':
            return

        folderInfo = {}

        for mailboxes in res[1]:
            mailbox = filter(lambda x: x, mailboxes.split('"'))[-1]
            folderInfo[mailbox.decode('imap4-utf-7')] = self.do_fetch_mailbox(mailbox)

        print '---------------------------result--------------------------'
        for key, value in folderInfo.items():
            print "%s total:%d, failed:%s" % (key, value[0], value[1])

    _handler_fetch_all = {"method": do_fetch_all, "parameters": ()}

    def do_fetch_mailbox(self, mailbox):
        """
        download all mails in a specific mailbox
        """

        def parse_response_str(mailDict, line):
            """
            parse fetch
            """
            if not line:
                return mailDict, None

            if line[0] == '(':
                line = line[1:]
            if line[-1] == ')':
                line = line[:-1]
            line = line.strip()

            if not line:
                return mailDict, None

            key, _, rest = line.partition(' ')
            key = key.upper()
            rest = rest.strip()
            while(rest):
                if rest[0] != '(':
                    value, _, rest = rest.partition(' ')
                    rest = rest.strip()
                else:
                    lParenthesis = 0
                    value = ''
                    for i in range(len(rest)):
                        if rest[i] == '(':
                            lParenthesis += 1
                            value += rest[i]
                        elif rest[i] == ')':
                            lParenthesis -= 1
                            value += rest[i]
                        else:
                            value += rest[i]

                        if not lParenthesis:
                            i += 1
                            break
                    rest = rest[i:].strip()
                    
                mailDict[key] = value
                lastKey = key
                key, _, rest = rest.partition(' ')
                key = key.upper()
                rest = rest.strip()

            return mailDict, lastKey

        def parse_fetch_response(res):
            mailDict = {}
            if type(res[0]) is str:
                mailDict['id'], _, rest = res[0].partition(' ')
                parse_response_str(mailDict, rest.strip())
                return mailDict

            mailDict['id'], _, rest = res[0][0].partition(' ')
            _ , lastKey = parse_response_str(mailDict, rest.strip())
            if len(res[0]) > 1 and lastKey:
                mailDict[lastKey] = res[0][1]

            for i in range(1, len(res)):
                _ , lastKey = parse_response_str(mailDict, res[i][0].strip())
                if len(res[i]) > 1 and lastKey:
                    mailDict[lastKey] = res[i][1]

            return mailDict

        def save_mail(mailInfo):
            p = "%s/%s" % (self.user, mailbox.decode('imap4-utf-7'))
            if not os.path.isdir(p):
                os.makedirs(p)

            path = "%s/%s" % (p, mailInfo['UID'])
            with open(path, 'w') as fp:
                fp.write(mailInfo['RFC822'])

        self.connect()
        self.login()
        res = self.conn.select(mailbox)
        if res[0].upper() != 'OK':
            print 'Failed to select: ', mailbox
            if self.debug:
                self.conn.print_log()
            return (0, [])
        mailNum = int(res[1][0])

        failedIds = []
        for i in range(1, mailNum + 1):
            res = self.conn.fetch(str(i), "(UID RFC822)")
            if res[0].upper() != 'OK':
                continue
    
            try:
                mailInfo = parse_fetch_response(res[1])
                save_mail(mailInfo)
                print "%s %d/%d uid:%s OK" % (mailbox.decode('imap4-utf-7'), i, mailNum, mailInfo['UID'])
            except:
                failedIds.append(i)
                print "%s %d/%d uid:%s Failed" % (mailbox.decode('imap4-utf-7'), i, mailNum, mailInfo['UID'])

        #print 'total: %d, success: %d, fail: %d' % (mailNum, mailNum - len(failedIds), len(failedIds))
        #if failedIds: print 'failed id: %s' % failedIds
        if self.debug:
            self.conn.print_log()

        return (mailNum, failedIds)

    _handler_fetch_mailbox = {"method": do_fetch_mailbox, "parameters": ("mailbox",)}

    @classmethod
    def help(self):

        print 'methods:'
        for i in dir(self):
            if i.startswith('do_'):
                print '\t', i[3:]

def main(argv):

    host = "localhost"
    port = 143
    user = "homer"
    passwd = "homer"
    method = ""
    debug = False
    ssl = False
    argsList = []

    if not argv:
        print 'imap.py -h <host> -p <port> -u <user> -w <password> -m <method>'
        ImapHandler.help()
        return

    try:
        while(argv):
            opts,args = getopt.getopt(argv, "h:p:u:w:m:ds")
            for opt, arg in opts:
                if opt == '-h':
                    host = arg
                elif opt == '-p':
                    port = int(arg)
                elif opt == '-u':
                    user = arg
                elif opt == '-w':
                    passwd = arg
                elif opt == '-m':
                    method = arg
                elif opt == '-d':
                    debug = True
                elif opt == '-s':
                    ssl = True
            if args:
                argsList.append(args[0].decode('utf-8', 'ignore'))
                argv = args[1:]
            else:
                break
            
    except getopt.GetoptError:
        print 'imap.py -h <host> -p <port> -u <user> -w <password> -m <method>'
        ImapHandler.help()
        return

    print "Connect to:", host, " port:", port, " as:", user, " with pass:", passwd, "ssl:", ssl

    imap = ImapHandler(user, passwd, host, port, debug, ssl)
    t0 = time.time()
    imap.run(method, argsList) 
    print time.time() - t0, "run time"

if __name__ == "__main__":
    main(sys.argv[1:])

