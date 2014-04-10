import Handler
from collections import OrderedDict as dict

class ContactModel():
	def __init__(self,dom,username):
		self.xmlHandler = Handler.xmlHandler('contacts')
		self.dom = dom
		self.username = username
	
	def saveSimpleContact(self, action='',fName='first',lName='last',mName='middle'):
		xml = self.xmlHandler
		mailaddr = self.username+'@'+self.dom
		
		contactsHash={'action':action,'addressBookId':'PAB://%s/%s/main'%(self.dom,self.username)}
		xml.addAttri(contactsHash)
			# add node for firstname, lastname
		contactNode = xml.addNode(newNode='contact')
		contactHash = {'fistName':fName,'lastName':lName}
		xml.addAttri(tarNode=contactNode,attrHash=contactHash)
			# add node for middlename
		contactfield  = xml.addNode(newNode='contactfield',parent=contactNode)
		contactfieldHash = {'value':mName, 'primary':'false', 'type':'lzHeader', 'label':'middlename'}   #  
		xml.addAttri(tarNode=contactfield,attrHash=contactfieldHash)
			# add node for mail address
		contactfield  = xml.addNode(newNode='contactfield',parent=contactNode)
		contactfieldHash = {'value': mailaddr, 'primary':'false', 'type':'lzEmail', 'label':'home'}   #  
		xml.addAttri(tarNode=contactfield,attrHash=contactfieldHash)
		
		print xml.toxml()
		return xml.toxml()
		
if __name__ == '__main__':
	contact = ContactModel(dom='test.ie',username='build843.user40')
	contact.saveSimpleContact()
 