import urllib2
import xml.etree.ElementTree as ET
import csv
import boto3
import re


#
# License 3 clause BSD
# https://github.com/UKParlDataSheets/UKParlDataSheets-Scripts
#


class ModelBase:
    """Base Model for an MP or a Peer. Should not be used directly - Abstract class."""
    def __init__(self):
        self.member_id = None
        self.dobs_id = None
        self.pims_id = None
        self.display_as = None
        self.list_as = None
        self.full_title = None
        self.laying_minister_name = None
        self.date_of_birth = None
        self.date_of_death = None
        self.gender = None
        self.party = None
        self.house = None
        self.member_from = None
        self.house_start_date = None
        self.house_end_date = None
        self.current_status_id = None
        self.current_status_is_active = None
        self.current_status_name = None
        self.current_status_reason = None
        self.current_status_start_date = None
        self.addresses = []

    def get_twitter(self):
        """Gets Twitter Username."""
        for address in self.addresses:
            twitter = address.get_twitter()
            if twitter is not None:
                return twitter

    def get_facebook(self):
        """Gets Facebook URL."""
        for address in self.addresses:
            facebook = address.get_facebook()
            if facebook is not None:
                return facebook

    def get_email(self):
        """Gets Email Address"""
        for address in self.addresses:
            email = address.get_email()
            if email is not None:
                return re.sub(";$","",email)

    def get_parliamentary_phone(self):
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
                            for phone_bit in phones:
                                if phone_bit.strip().startswith('020'):
                                    return phone_bit.strip()
                    if phone.strip().startswith('020'):
                        return phone.strip()

    def get_parliamentary_fax(self):
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
        self.type_id = None
        self.type = None
        self.is_preferred = None
        self.is_physical = None
        self.note = None
        self.address_1 = None
        self.address_2 = None
        self.address_3 = None
        self.address_4 = None
        self.address_5 = None
        self.postcode = None
        self.phone = None
        self.fax = None
        self.email = None

    def get_twitter(self):
        """Gets Twitter Username."""
        if self.address_1 is not None and self.address_1.startswith('https://twitter.com/'):
            return self.address_1[20:].split('?').pop(0)
        if self.note is not None and self.note.startswith('Twitter: @'):
            return self.note[10:].split(',').pop(0).split(';').pop(0).strip()
        if self.note is not None and self.note.startswith('Twitter: '):
            return self.note[9:]
        if self.note is not None and self.note.startswith('Twitter - @'):
            return self.note[11:]

    def get_facebook(self):
        """Gets Facebook URL."""
        if self.address_1 is not None and self.address_1.startswith('https://www.facebook.com/'):
            return self.address_1
        if self.address_1 is not None and self.address_1.startswith('http://www.facebook.com/'):
            return self.address_1
        if self.address_1 is not None and self.address_1.startswith('https://en-gb.facebook.com/'):
            return self.address_1
        if self.note is not None and self.note.find('Facebook: ') != -1:
            url = self.note.split(', Facebook: ').pop(1)
            if not url.startswith('http'):
                url = 'https://' + url
            return url
        if self.note is not None and self.note.find('www.facebook.com') != -1:
            url = self.note.split('www.facebook.com').pop(1)
            return 'https://www.facebook.com' + url

    def get_email(self):
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

    def get_email(self):
        """Gets Email Address"""
        if self.email is not None and self.email.find(
                '@') != -1 and self.email.strip() != 'contactholmember@parliament.uk':
            return self.email.strip().split(' ').pop(0)


class ModelMP(ModelBase):
    """Model for a MP."""
    def __init__(self):
        ModelBase.__init__(self)

    def get_constituency_postal_address(self):
        """Gets postal Address record for the Constituency."""
        for address in self.addresses:
            if address.is_constituency_postal_address():
                return address


class ModelMPAddress(ModelAddressBase):
    """Model for an Address for a MP."""
    def __init__(self):
        ModelAddressBase.__init__(self)

    def is_constituency_postal_address(self):
        """Is this a postal address record for the Constituency? Checks type and if there is an adddress there."""
        return self.type == 'Constituency' and ((self.address_2 != '' and self.address_2 is not None) or (self.postcode != '' and self.postcode is not None))


def go(config, upload=False):
    """Call this to do work - this calls other functions needed."""
    peers_xml_file_name = config['DIRECTORY'] + '/peers.xml'
    download_data('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Lords/Addresses/',
                  peers_xml_file_name)
    peers = process_data(peers_xml_file_name, lambda: ModelPeer(), lambda: ModelPeerAddress())

    peers_csv_v1_file_name = config['DIRECTORY'] + '/peers-v1.csv'
    write_data_v1(peers, peers_csv_v1_file_name)
    if upload:
        upload_to_s3(config, peers_csv_v1_file_name, 'lordsV1.csv')

    peers_simple_csv_v1_file_name = config['DIRECTORY'] + '/peers-simple-v1.csv'
    write_peers_simple_v1(peers, peers_simple_csv_v1_file_name)
    if upload:
        upload_to_s3(config, peers_simple_csv_v1_file_name, 'lordsSimpleV1.csv')

    # we don't needs this again, so clear it to save some memory.
    peers = None

    mps_xml_file_name = config['DIRECTORY'] + '/mps.xml'
    download_data('http://data.parliament.uk/membersdataplatform/services/mnis/members/query/House=Commons/Addresses/',
                  mps_xml_file_name)
    mps = process_data(mps_xml_file_name, lambda: ModelMP(), lambda: ModelMPAddress())

    mps_csv_v1_file_name = config['DIRECTORY'] + '/mps-v1.csv'
    write_data_v1(mps, mps_csv_v1_file_name)
    if upload:
        upload_to_s3(config, mps_csv_v1_file_name, 'commonsV1.csv')

    mps_simple_csv_v1_file_name = config['DIRECTORY'] + '/mps-simple-v1.csv'
    write_mps_simple_v1(mps, mps_simple_csv_v1_file_name)
    if upload:
        upload_to_s3(config, mps_simple_csv_v1_file_name, 'commonsSimpleV1.csv')


def download_data(url, filename):
    """Downloads data from Web and saves to local file. Raises Exception if there was a problem."""
    response = urllib2.urlopen(url)
    if response.info().gettype() != 'application/xml':
        raise Exception('Problem Getting Data')
    data = response.read()
    target = open(filename, 'w')
    target.write(data)
    target.close()


def process_data(data_xml_file_name, new_person_function, new_address_function):
    """Processes the local XML of Peers or MPs data and returns data objects in memory."""
    tree = ET.parse(data_xml_file_name)
    root = tree.getroot()
    data = []
    for child in root:
        person = new_person_function()
        person.member_id = child.attrib['Member_Id']
        person.dobs_id = child.attrib['Dods_Id']
        person.pims_id = child.attrib['Pims_Id']
        person.display_as = child.find('DisplayAs').text
        person.list_as = child.find('ListAs').text
        person.full_title = child.find('FullTitle').text
        person.laying_minister_name = child.find('LayingMinisterName').text
        person.date_of_birth = child.find('DateOfBirth').text
        person.date_of_death = child.find('DateOfDeath').text
        person.gender = child.find('Gender').text
        person.party = child.find('Party').text
        person.house = child.find('House').text
        person.member_from = child.find('MemberFrom').text
        person.house_start_date = child.find('HouseStartDate').text
        person.house_end_date = child.find('HouseEndDate').text
        current_status = child.find('CurrentStatus')
        if current_status is not None:
            person.current_status_id = current_status.attrib['Id']
            person.current_status_is_active = current_status.attrib['IsActive']
            person.current_status_name = current_status.find('Name').text
            person.current_status_reason = current_status.find('Reason').text
            person.current_status_start_date = current_status.find('StartDate').text
        for address_root in child.find('Addresses').findall('Address'):
            address = new_address_function()
            address.type_id = address_root.attrib['Type_Id']
            address.type = address_root.find('Type').text if address_root.find('Type') is not None else None
            address.is_preferred = address_root.find('IsPreferred').text if address_root.find(
                'IsPreferred') is not None else None
            address.is_physical = address_root.find('IsPhysical').text if address_root.find(
                'IsPhysical') is not None else None
            address.note = address_root.find('Note').text if address_root.find('Note') is not None else None
            address.address_1 = address_root.find('Address1').text if address_root.find('Address1') is not None else None
            address.address_2 = address_root.find('Address2').text if address_root.find('Address2') is not None else None
            address.address_3 = address_root.find('Address3').text if address_root.find('Address3') is not None else None
            address.address_4 = address_root.find('Address4').text if address_root.find('Address4') is not None else None
            address.address_5 = address_root.find('Address5').text if address_root.find('Address5') is not None else None
            address.postcode = address_root.find('Postcode').text if address_root.find('Postcode') is not None else None
            address.phone = address_root.find('Phone').text if address_root.find('Phone') is not None else None
            address.fax = address_root.find('Fax').text if address_root.find('Fax') is not None else None
            address.email = address_root.find('Email').text if address_root.find('Email') is not None else None
            person.addresses.append(address)
        data.append(person)
    return data


def write_data_v1(people, filename):
    """Writes in-memory data objects about Peers or MPs to an external file."""
    csv_file = open(filename, 'wb')
    writer = csv.writer(csv_file)
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
            person.member_id,
            person.dobs_id,
            person.pims_id,
            person.display_as,
            person.list_as,
            person.full_title,
            person.laying_minister_name,
            person.date_of_birth,
            person.date_of_death,
            person.gender,
            person.party,
            person.house,
            person.member_from,
            person.house_start_date,
            person.house_end_date,
            person.current_status_id,
            person.current_status_is_active,
            person.current_status_name,
            person.current_status_reason,
            person.current_status_start_date,
        ]
        for i in range(0, 4):
            if len(person.addresses) > i:
                row.append(person.addresses[i].type_id)
                row.append(person.addresses[i].type)
                row.append(person.addresses[i].is_preferred)
                row.append(person.addresses[i].is_physical)
                row.append(person.addresses[i].note)
                row.append(person.addresses[i].address_1)
                row.append(person.addresses[i].address_2)
                row.append(person.addresses[i].address_3)
                row.append(person.addresses[i].address_4)
                row.append(person.addresses[i].address_5)
                row.append(person.addresses[i].postcode)
                row.append(person.addresses[i].phone)
                row.append(person.addresses[i].fax)
                row.append(person.addresses[i].email)
            else:
                for x in range(1, 14):
                    row.append(None)
        writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
    csv_file.close()


def write_peers_simple_v1(peers, filename):
    """Writes in-memory data objects about Peers to an external file."""
    csv_file = open(filename, 'wb')
    writer = csv.writer(csv_file)
    headings = ['Member_Id', 'Dods_Id', 'Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName', 'MemberFrom', 'Party',
                'Email', 'Twitter', 'FaceBook', 'ParliamentaryPhone', 'ParliamentaryFax']
    writer.writerow(headings)
    for person in peers:
        row = [
            person.member_id,
            person.dobs_id,
            person.pims_id,
            person.display_as,
            person.list_as,
            person.full_title,
            person.laying_minister_name,
            person.member_from,
            person.party,
            person.get_email(),
            person.get_twitter(),
            person.get_facebook(),
            person.get_parliamentary_phone(),
            person.get_parliamentary_fax(),
        ]
        writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
    csv_file.close()


def write_mps_simple_v1(mps, filename):
    """Writes in-memory data objects about MPs to an external file."""
    csv_file = open(filename, 'wb')
    writer = csv.writer(csv_file)
    headings = ['Member_Id', 'Dods_Id', 'Pims_Id', 'DisplayAs', 'ListAs', 'FullTitle', 'LayingMinisterName', 'MemberFrom', 'Party',
                'Email', 'Twitter', 'FaceBook', 'ParliamentaryPhone', 'ParliamentaryFax',
                'ConstituencyPostalAddress1', 'ConstituencyPostalAddress2', 'ConstituencyPostalAddress3', 'ConstituencyPostalAddress4', 'ConstituencyPostalAddress5', 'ConstituencyPostCode']
    writer.writerow(headings)
    for person in mps:
        row = [
            person.member_id,
            person.dobs_id,
            person.pims_id,
            person.display_as,
            person.list_as,
            person.full_title,
            person.laying_minister_name,
            person.member_from,
            person.party,
            person.get_email(),
            person.get_twitter(),
            person.get_facebook(),
            person.get_parliamentary_phone(),
            person.get_parliamentary_fax(),
        ]
        constituency_postal_address = person.get_constituency_postal_address()
        if constituency_postal_address is not None:
            row.append(constituency_postal_address.address_1)
            row.append(constituency_postal_address.address_2)
            row.append(constituency_postal_address.address_3)
            row.append(constituency_postal_address.address_4)
            row.append(constituency_postal_address.address_5)
            row.append(constituency_postal_address.postcode)
        writer.writerow([(unicode(s).encode("utf-8") if s is not None else '') for s in row])
    csv_file.close()


def upload_to_s3(config, local_file_name, key):
    """Uploads local file to a S3 Bucket."""
    client = boto3.client(
        's3',
        aws_access_key_id=config['AWS_ACCESS_KEY'],
        aws_secret_access_key=config['AWS_SECRET_KEY']
    )
    data = open(local_file_name, 'rb')
    client.put_object(Key=key, Body=data, Bucket=config['AWS_BUCKET_NAME'])
