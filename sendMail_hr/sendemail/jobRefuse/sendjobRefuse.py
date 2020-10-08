import smtplib
from email.Header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEMultipart import MIMEMultipart
from email.mime.image import MIMEImage

#发送者邮件地址
sender="ann.yao@owmessaging.com"

def sendMail(sender,receiver,subject):
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
      尊敬的候选人：<br>
<p>
感谢您对我公司的关注，经过与用人部门的充分沟通，我们暂时无法提供与您经验匹配的工作机会。但我们会把您的相关资料保存在我们的简历库中作为储备，预祝您未来一切顺利！ 
<p>
<p>
再次感谢您的关注。预祝您未来一切顺利！
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
    """
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
    txtfile = open("refuseinfo.txt","r")
    lines=txtfile.readlines()
    txtfile.close()
    for line in lines:
      s_maillist=line.replace('\n','').split(',')    
      m_subject="模板：感谢对我公司关注"
      if sendMail(sender,s_maillist,m_subject):
         print "send refuse email successfully "
      else:
         print "send refuse email  failed "
    
    
    
   
         
     










    
      
   
