import smtplib
from email.Header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage

#发送者邮件地址
sender="ann.yao@owmessaging.com"

def sendMail(sender,receiver,subject,sname,sjob,stime):
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
<p>
职位：%s
<p>
时间：%s 
<p>
地址：朝阳区霄云路26号 鹏润大厦B座2609
<p>
建议路线： 10号线亮马桥站C口 出，燕莎桥南乘坐516,707 二站 莱太花卉下车，步行即到；405,421,416两站麦子店西街下车，步行即到
<p>
时间确认请回复

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
    """%(sname,sjob,stime)
    htm=MIMEText(html,'html','utf-8')
    msg.attach(htm)


#构造显示图片
    
    fp=open('h.png','rb')
    msgImage=MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID','<image1>')
    msg.attach(msgImage)
    

   
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
    txtfile = open("testinfo.txt","r")
    lines=txtfile.readlines()
    i=0
    for line in lines:
      ulist=line.split(',')
      s_name=ulist[0]
      s_job=ulist[1]
      s_email=ulist[2]    
      s_time=ulist[3].replace('\n','')
      
      i=i+1
      m_subject="模板: 美国莱思龙-职位介绍 %s"%s_job
      if sendMail(sender,s_email,m_subject,s_name,s_job,s_time):
         print "send test email successfully %s"%i 
      else:
         print "send test email failed %s"%i
         
     










    
      
   
