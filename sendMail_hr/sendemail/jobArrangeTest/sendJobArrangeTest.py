import smtplib
from email.Header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage

#发送者邮件地址
sender="ann.yao@owmessaging.com"

def sendMail(sender,receiver,subject,sname,satt):
    smtpserver='smtp.owmessaging.com'
    username='ann.yao'
    password='12qwaszxER'
    msg=MIMEMultipart('alternative')
    
    msg['Subject']=Header(subject,'utf-8')

    html="""\
    <html>
    <head>test mail </head>
    <body>
    <p>
      %s 你好:<br>

查收附件为我公司职务说明书，若对此职位有兴趣，请回复邮件安排后续面试事宜.
<p>
<p>
<p>
<p>
<br>
Denise Kong
<br>
HR Officer
<br>
T:(8610)6269 1018-107 
<br>
Email: denise.kong@owmessaging.com
<br>
Website: www.owmessaging.com 
<br>
 Suite 2609, Block B, Eagle Plaza, No.26 Xiaoyun Road, Chaoyang District,
 Beijing China 100016
<br>
    <img src="cid:image1">
    </body>
    </html>
    """% sname
    htm=MIMEText(html,'html','utf-8')
    msg.attach(htm)


#构造显示图片
    
    fp=open('h.png','rb')
    msgImage=MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID','<image1>')
    msg.attach(msgImage)
    
#构造附件
    att2 = MIMEText(open(satt, 'rb').read(), 'base64', 'gb2312')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="job_test.doc"'
    msg.attach(att2)
   
#连接smtp服务器
    
    try:
        smtp=smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(username,password)
        smtp.sendmail(sender,receiver,msg.as_string())
        smtp.close()
        return True
    except Exception,e:
       print str(e)
       return False

if __name__=='__main__':
    #打开参数文件
    txtfile = open("ArrangeTestinfo.txt","r")
    lines=txtfile.readlines()
    i=0
    for line in lines:
      ulist=line.split(',')
      s_name=ulist[0]
      s_job=ulist[1]
      s_email=ulist[2]    
      s_at=ulist[3].replace('\n','')
      
      i=i+1
      m_subject="模板: 美国莱思龙-职位介绍 %s"%s_job
      if sendMail(sender,s_email,m_subject,s_name,s_at):
         print "send arrange test mail successfully %s"%i 
      else:
         print "send arrange test mail failed %s"%i
         
     










    
      
   
