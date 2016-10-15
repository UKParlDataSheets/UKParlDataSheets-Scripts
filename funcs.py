
import urllib2
import xml.etree.ElementTree as ET
import csv
import boto3

class ModelBase:
	def __init__(self):
		self.memberId = None
		self.dobsId = None
		self.pimsId = None
		self.displayAs = None
		self.listAs = None
		self.fullTitle = None
		self.layingMinisterName = None
		self.dateOfBirth = None
		self.dateOfDeath = None
		self.gender = None
		self.party = None
		self.house = None
		self.memberFrom = None
		self.houseStartDate = None
		self.houseEndDate = None
		self.currentStatusID = None
		self.currentStatusIsActive = None
		self.currentStatusName = None
		self.currentStatusReason = None
		self.currentStatusStartDate = None
		self.addresses = []
	def getTwitter(self):
		for address in self.addresses:
			twitter = address.getTwitter()
			if (twitter is not None):
				return twitter
	def getFacebook(self):
		for address in self.addresses:
			fb = address.getFacebook()
			if (fb is not None):
				return fb

class ModelAddressBase:
	def __init__(self):
		self.typeId = None
		self.type = None
		self.isPreferred = None
		self.isPhysical = None
		self.note = None
		self.address1 = None
		self.address2 = None
		self.address3 = None
		self.address4 = None
		self.address5 = None
		self.postcode = None
		self.phone = None
		self.fax = None
		self.email = None
	def getTwitter(self):
		if self.address1 is not None and self.address1.startswith('https://twitter.com/'):
			return self.address1[20:].split('?').pop(0)
		if self.note is not None and self.note.startswith('Twitter: @'):
			return self.note[10:].split(',').pop(0).split(';').pop(0).strip()
		if self.note is not None and self.note.startswith('Twitter: '):
			return self.note[9:]
		if self.note is not None and self.note.startswith('Twitter - @'):
			return self.note[11:]
	def getFacebook(self):
		if self.address1 is not None and self.address1.startswith('https://www.facebook.com/'):
			return self.address1
		if self.address1 is not None and self.address1.startswith('http://www.facebook.com/'):
			return self.address1
		if self.address1 is not None and self.address1.startswith('https://en-gb.facebook.com/'):
			return self.address1
		if self.note is not None and self.note.find('Facebook: ') != -1:
			url = self.note.split(', Facebook: ').pop(1)
			if not url.startswith('http'):
				url = 'https://' + url
			return url 
		if self.note is not None and self.note.find('www.facebook.com') != -1:
			url = self.note.split('www.facebook.com').pop(1)
			return 'https://www.facebook.com' + url

		

class ModelPeer(ModelBase):
	def __init__(self):
		ModelBase.__init__(self)

class ModelPeerAddress(ModelAddressBase):
	def __init__(self):
		ModelAddressBase.__init__(self)


class ModelMP(ModelBase):
	def __init__(self):
		ModelBase.__init__(self)

class ModelMPAddress(ModelAddressBase):
	def __init__(self):
		ModelAddressBase.__init__(self)




def go(config):
	peersXMLFileName = config['DIRECTORY'] + '/peers.xml'
	downloadData('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Lords/Addresses/',peersXMLFileName)
	peers = processPeers(peersXMLFileName)
	
	peersCSVV1FileName =  config['DIRECTORY'] + '/peers-v1.csv'
	writePeersV1(peers, peersCSVV1FileName)
	uploadToS3(config, peersCSVV1FileName, 'lordsV1.csv')
	
	peersSimpleCSVV1FileName =  config['DIRECTORY'] + '/peers-simple-v1.csv'
	writePeersSimpleV1(peers, peersSimpleCSVV1FileName)
	uploadToS3(config, peersSimpleCSVV1FileName, 'lordsSimpleV1.csv')



	mpsXMLFileName = config['DIRECTORY'] + '/mps.xml'
	downloadData('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons/Addresses/',mpsXMLFileName)
	mps = processMPs(mpsXMLFileName)
	
	mpsCSVV1FileName =  config['DIRECTORY'] + '/mps-v1.csv'
	writeMPsV1(mps, mpsCSVV1FileName)
	uploadToS3(config, mpsCSVV1FileName, 'commonsV1.csv')
	
	mpsSimpleCSVV1FileName =  config['DIRECTORY'] + '/mps-simple-v1.csv'
	writeMPsSimpleV1(mps, mpsSimpleCSVV1FileName)
	uploadToS3(config, mpsSimpleCSVV1FileName, 'commonsSimpleV1.csv')



def downloadData(url, filename):
	response = urllib2.urlopen(url)
	if (response.info().gettype() != 'application/xml'):
		raise Exception('Problem Getting Data')
	data = response.read()
	target = open(filename, 'w')
	target.write(data)
	target.close()

def processPeers(peersXMLFileName):
	tree = ET.parse(peersXMLFileName)
	root = tree.getroot()
	peers = []
	for child in root:
		person = ModelPeer()
		person.memberId = child.attrib['Member_Id']
		person.dobsId = child.attrib['Dods_Id']
		person.pimsId = child.attrib['Pims_Id']
		person.displayAs = child.find('DisplayAs').text
		person.listAs = child.find('ListAs').text
		person.fullTitle = child.find('FullTitle').text
		person.layingMinisterName = child.find('LayingMinisterName').text
		person.dateOfBirth = child.find('DateOfBirth').text
		person.dateOfDeath = child.find('DateOfDeath').text
		person.gender = child.find('Gender').text
		person.party = child.find('Party').text
		person.house = child.find('House').text
		person.memberFrom = child.find('MemberFrom').text
		person.houseStartDate = child.find('HouseStartDate').text
		person.houseEndDate = child.find('HouseEndDate').text
		currentStatus = child.find('CurrentStatus')
		if (currentStatus is not None):
			person.currentStatusID = currentStatus.attrib['Id']
			person.currentStatusIsActive = currentStatus.attrib['IsActive']
			person.currentStatusName = currentStatus.find('Name').text
			person.currentStatusReason = currentStatus.find('Reason').text
			person.currentStatusStartDate = currentStatus.find('StartDate').text
		for addressRoot in child.find('Addresses').findall('Address'):
			address = ModelPeerAddress()
			address.typeId = addressRoot.attrib['Type_Id']
			address.type  =  addressRoot.find('Type').text if addressRoot.find('Type') is not None else None
			address.isPreferred  =  addressRoot.find('IsPreferred').text if addressRoot.find('IsPreferred') is not None else None
			address.isPhysical  =  addressRoot.find('IsPhysical').text if addressRoot.find('IsPhysical') is not None else None
			address.note  =  addressRoot.find('Note').text if addressRoot.find('Note') is not None else None
			address.address1  =  addressRoot.find('Address1').text if addressRoot.find('Address1') is not None else None
			address.address2  =  addressRoot.find('Address2').text if addressRoot.find('Address2') is not None else None
			address.address3  =  addressRoot.find('Address3').text if addressRoot.find('Address3') is not None else None
			address.address4  =  addressRoot.find('Address4').text if addressRoot.find('Address4') is not None else None
			address.address5  =  addressRoot.find('Address5').text if addressRoot.find('Address5') is not None else None
			address.postcode  =  addressRoot.find('Postcode').text if addressRoot.find('Postcode') is not None else None
			address.phone  =  addressRoot.find('Phone').text if addressRoot.find('Phone') is not None else None
			address.fax  =  addressRoot.find('Fax').text if addressRoot.find('Fax') is not None else None
			address.email  =  addressRoot.find('Email').text if addressRoot.find('Email') is not None else None
			person.addresses.append(address)
		peers.append(person)
	return peers


def writePeersV1(peers, filename):
	csvfile = open(filename, 'wb')
	writer = csv.writer(csvfile)
	headings = ['Member_Id','Dods_Id','Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName', 'DateOfBirth', 'DateOfDeath', 'Gender',
    'Party',
    'House',
    'MemberFrom',
    'HouseStartDate',
    'HouseEndDate',
    'CurrentStatus_Id',
    'CurrentStatus_IsActive',
    'CurrentStatus_Name',
    'CurrentStatus_Reason',
    'CurrentStatus_StartDate']
	for i in range(1, 5):
		headings.append('Address' + str(i) + '_Type_Id')
		headings.append('Address' + str(i) + '_Type')
		headings.append('Address' + str(i) + '_IsPreferred')
		headings.append('Address' + str(i) + '_IsPhysical')
		headings.append('Address' + str(i) + '_Note')
		headings.append('Address' + str(i) + '_Address1')
		headings.append('Address' + str(i) + '_Address2')
		headings.append('Address' + str(i) + '_Address3')
		headings.append('Address' + str(i) + '_Address4')
		headings.append('Address' + str(i) + '_Address5')
		headings.append('Address' + str(i) + '_Postcode')
		headings.append('Address' + str(i) + '_Phone')
		headings.append('Address' + str(i) + '_Fax')
		headings.append('Address' + str(i) + '_Email')
	writer.writerow(headings)
	for person in peers:
		row = [
			person.memberId,
			person.dobsId,
			person.pimsId,
			person.displayAs,
			person.listAs,
			person.fullTitle,
			person.layingMinisterName,
			person.dateOfBirth,
			person.dateOfDeath,
			person.gender,
			person.party,
			person.house,
			person.memberFrom,
			person.houseStartDate,
			person.houseEndDate,
			person.currentStatusID,
			person.currentStatusIsActive,
			person.currentStatusName,
			person.currentStatusReason,
			person.currentStatusStartDate,
		]
		for i in range(0, 4):
			if (len(person.addresses) > i):
				row.append(person.addresses[i].typeId)
				row.append(person.addresses[i].type)
				row.append(person.addresses[i].isPreferred)
				row.append(person.addresses[i].isPhysical)
				row.append(person.addresses[i].note)
				row.append(person.addresses[i].address1)
				row.append(person.addresses[i].address2)
				row.append(person.addresses[i].address3)
				row.append(person.addresses[i].address4)
				row.append(person.addresses[i].address5)
				row.append(person.addresses[i].postcode)
				row.append(person.addresses[i].phone)
				row.append(person.addresses[i].fax)
				row.append(person.addresses[i].email)
			else:
				for x in range(1, 14):
					row.append(None)
		writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
	csvfile.close()

def writePeersSimpleV1(peers, filename):
	csvfile = open(filename, 'wb')
	writer = csv.writer(csvfile)
	headings = ['Member_Id','Dods_Id','Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName','Party','Twitter','FaceBook']
	writer.writerow(headings)
	for person in peers:
		row = [
			person.memberId,
			person.dobsId,
			person.pimsId,
			person.displayAs,
			person.listAs,
			person.fullTitle,
			person.layingMinisterName,
			person.party,
			person.getTwitter(),
			person.getFacebook(),
		]
		writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
	csvfile.close()


def processMPs(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	mps = []
	for child in root:
		person = ModelMP()
		person.memberId = child.attrib['Member_Id']
		person.dobsId = child.attrib['Dods_Id']
		person.pimsId = child.attrib['Pims_Id']
		person.displayAs = child.find('DisplayAs').text
		person.listAs = child.find('ListAs').text
		person.fullTitle = child.find('FullTitle').text
		person.layingMinisterName = child.find('LayingMinisterName').text
		person.dateOfBirth = child.find('DateOfBirth').text
		person.dateOfDeath = child.find('DateOfDeath').text
		person.gender = child.find('Gender').text
		person.party = child.find('Party').text
		person.house = child.find('House').text
		person.memberFrom = child.find('MemberFrom').text
		person.houseStartDate = child.find('HouseStartDate').text
		person.houseEndDate = child.find('HouseEndDate').text
		currentStatus = child.find('CurrentStatus')
		if (currentStatus is not None):
			person.currentStatusID = currentStatus.attrib['Id']
			person.currentStatusIsActive = currentStatus.attrib['IsActive']
			person.currentStatusName = currentStatus.find('Name').text
			person.currentStatusReason = currentStatus.find('Reason').text
			person.currentStatusStartDate = currentStatus.find('StartDate').text
		for addressRoot in child.find('Addresses').findall('Address'):
			address = ModelPeerAddress()
			address.typeId = addressRoot.attrib['Type_Id']
			address.type  =  addressRoot.find('Type').text if addressRoot.find('Type') is not None else None
			address.isPreferred  =  addressRoot.find('IsPreferred').text if addressRoot.find('IsPreferred') is not None else None
			address.isPhysical  =  addressRoot.find('IsPhysical').text if addressRoot.find('IsPhysical') is not None else None
			address.note  =  addressRoot.find('Note').text if addressRoot.find('Note') is not None else None
			address.address1  =  addressRoot.find('Address1').text if addressRoot.find('Address1') is not None else None
			address.address2  =  addressRoot.find('Address2').text if addressRoot.find('Address2') is not None else None
			address.address3  =  addressRoot.find('Address3').text if addressRoot.find('Address3') is not None else None
			address.address4  =  addressRoot.find('Address4').text if addressRoot.find('Address4') is not None else None
			address.address5  =  addressRoot.find('Address5').text if addressRoot.find('Address5') is not None else None
			address.postcode  =  addressRoot.find('Postcode').text if addressRoot.find('Postcode') is not None else None
			address.phone  =  addressRoot.find('Phone').text if addressRoot.find('Phone') is not None else None
			address.fax  =  addressRoot.find('Fax').text if addressRoot.find('Fax') is not None else None
			address.email  =  addressRoot.find('Email').text if addressRoot.find('Email') is not None else None
			person.addresses.append(address)
		mps.append(person)
	return mps


def writeMPsV1(mps, filename):
	csvfile = open(filename, 'wb')
	writer = csv.writer(csvfile)
	headings = ['Member_Id','Dods_Id','Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName', 'DateOfBirth', 'DateOfDeath', 'Gender',
    'Party',
    'House',
    'MemberFrom',
    'HouseStartDate',
    'HouseEndDate',
    'CurrentStatus_Id',
    'CurrentStatus_IsActive',
    'CurrentStatus_Name',
    'CurrentStatus_Reason',
    'CurrentStatus_StartDate']
	for i in range(1, 5):
		headings.append('Address' + str(i) + '_Type_Id')
		headings.append('Address' + str(i) + '_Type')
		headings.append('Address' + str(i) + '_IsPreferred')
		headings.append('Address' + str(i) + '_IsPhysical')
		headings.append('Address' + str(i) + '_Note')
		headings.append('Address' + str(i) + '_Address1')
		headings.append('Address' + str(i) + '_Address2')
		headings.append('Address' + str(i) + '_Address3')
		headings.append('Address' + str(i) + '_Address4')
		headings.append('Address' + str(i) + '_Address5')
		headings.append('Address' + str(i) + '_Postcode')
		headings.append('Address' + str(i) + '_Phone')
		headings.append('Address' + str(i) + '_Fax')
		headings.append('Address' + str(i) + '_Email')
	writer.writerow(headings)
	for person in mps:
		row = [
			person.memberId,
			person.dobsId,
			person.pimsId,
			person.displayAs,
			person.listAs,
			person.fullTitle,
			person.layingMinisterName,
			person.dateOfBirth,
			person.dateOfDeath,
			person.gender,
			person.party,
			person.house,
			person.memberFrom,
			person.houseStartDate,
			person.houseEndDate,
			person.currentStatusID,
			person.currentStatusIsActive,
			person.currentStatusName,
			person.currentStatusReason,
			person.currentStatusStartDate,
		]
		for i in range(0, 4):
			if (len(person.addresses) > i):
				row.append(person.addresses[i].typeId)
				row.append(person.addresses[i].type)
				row.append(person.addresses[i].isPreferred)
				row.append(person.addresses[i].isPhysical)
				row.append(person.addresses[i].note)
				row.append(person.addresses[i].address1)
				row.append(person.addresses[i].address2)
				row.append(person.addresses[i].address3)
				row.append(person.addresses[i].address4)
				row.append(person.addresses[i].address5)
				row.append(person.addresses[i].postcode)
				row.append(person.addresses[i].phone)
				row.append(person.addresses[i].fax)
				row.append(person.addresses[i].email)
		else:
			for x in range(1, 14):
				row.append(None)
		writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
	csvfile.close()

def writeMPsSimpleV1(mps, filename):
	csvfile = open(filename, 'wb')
	writer = csv.writer(csvfile)
	headings = ['Member_Id','Dods_Id','Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName','Party','Twitter','FaceBook']
	writer.writerow(headings)
	for person in mps:
		row = [
			person.memberId,
			person.dobsId,
			person.pimsId,
			person.displayAs,
			person.listAs,
			person.fullTitle,
			person.layingMinisterName,
			person.party,
			person.getTwitter(),
			person.getFacebook(),
		]
		writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
	csvfile.close()


def uploadToS3(config, file, key):
	client = boto3.client(
		's3',
		aws_access_key_id=config['AWS_ACCESS_KEY'],
		aws_secret_access_key=config['AWS_SECRET_KEY']
	)
	data = open(file, 'rb')
	client.put_object(Key=key, Body=data,Bucket=config['AWS_BUCKET_NAME'])
