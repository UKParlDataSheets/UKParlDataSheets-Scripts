import urllib2
import xml.etree.ElementTree as ET
import csv
import boto3


#
# License 3 clause BSD
# https://github.com/UKParlDataSheets/UKParlDataSheets-Scripts
#


class ModelBase:
    """Base Model for an MP or a Peer. Should not be used directly - Abstract class."""
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
        """Gets Twitter Username."""
        for address in self.addresses:
            twitter = address.getTwitter()
            if twitter is not None:
                return twitter

    def getFacebook(self):
        """Gets Facebook URL."""
        for address in self.addresses:
            fb = address.getFacebook()
            if fb is not None:
                return fb

    def getEmail(self):
        """Gets Email Address"""
        for address in self.addresses:
            email = address.getEmail()
            if email is not None:
                return email

    def getParliamentaryPhone(self):
        """Gets phone number on the Parliamentary record."""
        for address in self.addresses:
            if address.type == 'Parliamentary':
                phone = address.phone.strip() if address.phone is not None else None
                if phone is not None:
                    if phone.startswith('Tel: '):
                        phone = phone[5:]
                    if phone.endswith(' (Office contact)'):
                        phone = phone[:-17]
                    if phone.find('Fax') != -1:
                        bits = address.phone.split('Fax')
                        phone = bits.pop(0).strip()
                    for char in [';', ',', '/']:
                        if phone.find(char) != -1:
                            phones = phone.split(char)
                            for phoneBit in phones:
                                if phoneBit.strip().startswith('020'):
                                    return phoneBit.strip()
                    if phone.strip().startswith('020'):
                        return phone.strip()

    def getParliamentaryFax(self):
        """Gets fax number on the Parliamentary record."""
        for address in self.addresses:
            if address.type == 'Parliamentary':
                if address.fax != '' and address.fax is not None:
                    return address.fax
                if address.phone is not None and address.phone.find('Fax') != -1:
                    bits = address.phone.split('Fax')
                    fax = bits.pop(1).strip()
                    if fax.startswith('.'):
                        fax = fax[1:]
                    if fax.startswith(':'):
                        fax = fax[1:]
                    return fax.strip()


class ModelAddressBase:
    """Base Model for an Address for an MP or a Peer.  Should not be used directly - Abstract class."""
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
        """Gets Twitter Username."""
        if self.address1 is not None and self.address1.startswith('https://twitter.com/'):
            return self.address1[20:].split('?').pop(0)
        if self.note is not None and self.note.startswith('Twitter: @'):
            return self.note[10:].split(',').pop(0).split(';').pop(0).strip()
        if self.note is not None and self.note.startswith('Twitter: '):
            return self.note[9:]
        if self.note is not None and self.note.startswith('Twitter - @'):
            return self.note[11:]

    def getFacebook(self):
        """Gets Facebook URL."""
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

    def getEmail(self):
        """Gets Email Address"""
        if self.email is not None and self.email.find('@') != -1:
            return self.email.strip().split(' ').pop(0)


class ModelPeer(ModelBase):
    """Model for a Peer."""
    def __init__(self):
        ModelBase.__init__(self)


class ModelPeerAddress(ModelAddressBase):
    """Model for an Address for a Peer."""
    def __init__(self):
        ModelAddressBase.__init__(self)

    def getEmail(self):
        """Gets Email Address"""
        if self.email is not None and self.email.find(
                '@') != -1 and self.email.strip() != 'contactholmember@parliament.uk':
            return self.email.strip().split(' ').pop(0)


class ModelMP(ModelBase):
    """Model for a MP."""
    def __init__(self):
        ModelBase.__init__(self)

    def getConstituencyPostalAddress(self):
        """Gets postal Address record for the Constituency."""
        for address in self.addresses:
            if address.isConstituencyPostalAddress():
                return address


class ModelMPAddress(ModelAddressBase):
    """Model for an Address for a MP."""
    def __init__(self):
        ModelAddressBase.__init__(self)

    def isConstituencyPostalAddress(self):
        """Is this a postal address record for the Constituency? Checks type and if there is an adddress there."""
        return self.type == 'Constituency' and ((self.address2 != '' and self.address2 is not None) or (self.postcode != '' and self.postcode is not None))


def go(config, upload=False):
    """Call this to do work - this calls other functions needed."""
    peersXMLFileName = config['DIRECTORY'] + '/peers.xml'
    downloadData('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Lords/Addresses/',
                 peersXMLFileName)
    peers = processData(peersXMLFileName, lambda: ModelPeer(), lambda: ModelPeerAddress())

    peersCSVV1FileName = config['DIRECTORY'] + '/peers-v1.csv'
    writeDataV1(peers, peersCSVV1FileName)
    if upload:
        uploadToS3(config, peersCSVV1FileName, 'lordsV1.csv')

    peersSimpleCSVV1FileName = config['DIRECTORY'] + '/peers-simple-v1.csv'
    writePeersSimpleV1(peers, peersSimpleCSVV1FileName)
    if upload:
        uploadToS3(config, peersSimpleCSVV1FileName, 'lordsSimpleV1.csv')

    # we don't needs this again, so clear it to save some memory.
    peers = None

    mpsXMLFileName = config['DIRECTORY'] + '/mps.xml'
    downloadData('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons/Addresses/',
                 mpsXMLFileName)
    mps = processData(mpsXMLFileName, lambda: ModelMP(), lambda: ModelMPAddress())

    mpsCSVV1FileName = config['DIRECTORY'] + '/mps-v1.csv'
    writeDataV1(mps, mpsCSVV1FileName)
    if upload:
        uploadToS3(config, mpsCSVV1FileName, 'commonsV1.csv')

    mpsSimpleCSVV1FileName = config['DIRECTORY'] + '/mps-simple-v1.csv'
    writeMPsSimpleV1(mps, mpsSimpleCSVV1FileName)
    if upload:
        uploadToS3(config, mpsSimpleCSVV1FileName, 'commonsSimpleV1.csv')


def downloadData(url, filename):
    """Downloads data from Web and saves to local file. Raises Exception if there was a problem."""
    response = urllib2.urlopen(url)
    if response.info().gettype() != 'application/xml':
        raise Exception('Problem Getting Data')
    data = response.read()
    target = open(filename, 'w')
    target.write(data)
    target.close()


def processData(peersXMLFileName, newPersonFunction, newAddressFunction):
    """Processes the local XML of Peers or MPs data and returns data objects in memory."""
    tree = ET.parse(peersXMLFileName)
    root = tree.getroot()
    data = []
    for child in root:
        person = newPersonFunction()
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
        if currentStatus is not None:
            person.currentStatusID = currentStatus.attrib['Id']
            person.currentStatusIsActive = currentStatus.attrib['IsActive']
            person.currentStatusName = currentStatus.find('Name').text
            person.currentStatusReason = currentStatus.find('Reason').text
            person.currentStatusStartDate = currentStatus.find('StartDate').text
        for addressRoot in child.find('Addresses').findall('Address'):
            address = newAddressFunction()
            address.typeId = addressRoot.attrib['Type_Id']
            address.type = addressRoot.find('Type').text if addressRoot.find('Type') is not None else None
            address.isPreferred = addressRoot.find('IsPreferred').text if addressRoot.find(
                'IsPreferred') is not None else None
            address.isPhysical = addressRoot.find('IsPhysical').text if addressRoot.find(
                'IsPhysical') is not None else None
            address.note = addressRoot.find('Note').text if addressRoot.find('Note') is not None else None
            address.address1 = addressRoot.find('Address1').text if addressRoot.find('Address1') is not None else None
            address.address2 = addressRoot.find('Address2').text if addressRoot.find('Address2') is not None else None
            address.address3 = addressRoot.find('Address3').text if addressRoot.find('Address3') is not None else None
            address.address4 = addressRoot.find('Address4').text if addressRoot.find('Address4') is not None else None
            address.address5 = addressRoot.find('Address5').text if addressRoot.find('Address5') is not None else None
            address.postcode = addressRoot.find('Postcode').text if addressRoot.find('Postcode') is not None else None
            address.phone = addressRoot.find('Phone').text if addressRoot.find('Phone') is not None else None
            address.fax = addressRoot.find('Fax').text if addressRoot.find('Fax') is not None else None
            address.email = addressRoot.find('Email').text if addressRoot.find('Email') is not None else None
            person.addresses.append(address)
        data.append(person)
    return data


def writeDataV1(people, filename):
    """Writes in-memory data objects about Peers or MPs to an external file."""
    csvfile = open(filename, 'wb')
    writer = csv.writer(csvfile)
    headings = ['Member_Id', 'Dods_Id', 'Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName',
                'DateOfBirth', 'DateOfDeath', 'Gender',
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
    for person in people:
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
            if len(person.addresses) > i:
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
    """Writes in-memory data objects about Peers to an external file."""
    csvfile = open(filename, 'wb')
    writer = csv.writer(csvfile)
    headings = ['Member_Id', 'Dods_Id', 'Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName', 'MemberFrom', 'Party',
                'Email', 'Twitter', 'FaceBook', 'ParliamentaryPhone', 'ParliamentaryFax']
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
            person.memberFrom,
            person.party,
            person.getEmail(),
            person.getTwitter(),
            person.getFacebook(),
            person.getParliamentaryPhone(),
            person.getParliamentaryFax(),
        ]
        writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
    csvfile.close()


def writeMPsSimpleV1(mps, filename):
    """Writes in-memory data objects about MPs to an external file."""
    csvfile = open(filename, 'wb')
    writer = csv.writer(csvfile)
    headings = ['Member_Id', 'Dods_Id', 'Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName', 'MemberFrom', 'Party',
                'Email', 'Twitter', 'FaceBook', 'ParliamentaryPhone', 'ParliamentaryFax',
                'ConstituencyPostalAddress1', 'ConstituencyPostalAddress2', 'ConstituencyPostalAddress3', 'ConstituencyPostalAddress4', 'ConstituencyPostalAddress5', 'ConstituencyPostCode']
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
            person.memberFrom,
            person.party,
            person.getEmail(),
            person.getTwitter(),
            person.getFacebook(),
            person.getParliamentaryPhone(),
            person.getParliamentaryFax(),
        ]
        constituencyPostalAddress = person.getConstituencyPostalAddress()
        if constituencyPostalAddress is not None:
            row.append(constituencyPostalAddress.address1)
            row.append(constituencyPostalAddress.address2)
            row.append(constituencyPostalAddress.address3)
            row.append(constituencyPostalAddress.address4)
            row.append(constituencyPostalAddress.address5)
            row.append(constituencyPostalAddress.postcode)
        writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
    csvfile.close()


def uploadToS3(config, file, key):
    """Uploads local file to a S3 Bucket."""
    client = boto3.client(
        's3',
        aws_access_key_id=config['AWS_ACCESS_KEY'],
        aws_secret_access_key=config['AWS_SECRET_KEY']
    )
    data = open(file, 'rb')
    client.put_object(Key=key, Body=data, Bucket=config['AWS_BUCKET_NAME'])
