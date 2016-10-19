import unittest
from funcs import *


#
# License 3 clause BSD
# https://github.com/UKParlDataSheets/UKParlDataSheets-Scripts
#


class TestTwitter(unittest.TestCase):

    def test_noCrashOnNone1(self):
        """If person has an empty adddress record, test no crashes."""
        person = ModelBase()

        address1 = ModelAddressBase()
        person.addresses.append(address1)

        self.assertEqual(person.getTwitter(), None)
        self.assertEqual(person.getFacebook(), None)
        self.assertEqual(person.getEmail(), None)

    def test_twitter1(self):
        """Tests getting Twitter when URL in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'https://twitter.com/LizBarkerLords'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'LizBarkerLords')

    def test_twitter2(self):
        """Test getting Twitter when it's in a note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: TariqBt1'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'TariqBt1')

    def test_twitter3(self):
        """Test getting Twitter when it's in a note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @lordphilofbrum'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'lordphilofbrum')

    def test_twitter4(self):
        """Tests getting Twitter when URL in Address1, with extra params."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'https://twitter.com/LordRoyKennedy?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'LordRoyKennedy')

    def test_twitter5(self):
        """Test getting Twitter when it's in a note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter - @delythjmorgan'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'delythjmorgan')

    def test_facebook1(self):
        """Tests getting Facebook when HTTPS URL in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'https://www.facebook.com/marycreaghwakefield'
        person.addresses.append(address2)

        self.assertEqual(person.getFacebook(), 'https://www.facebook.com/marycreaghwakefield')

    def test_facebook2(self):
        """Tests getting Facebook when HTTP URL in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'http://www.facebook.com/JeremyCorbynMP/'
        person.addresses.append(address2)

        self.assertEqual(person.getFacebook(), 'http://www.facebook.com/JeremyCorbynMP/')

    def test_facebook3(self):
        """Tests getting Facebook when HTTPS URL with country/lang in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'https://en-gb.facebook.com/LordAltonofLiverpool/'
        person.addresses.append(address2)

        self.assertEqual(person.getFacebook(), 'https://en-gb.facebook.com/LordAltonofLiverpool/')

    def test_twitterAndFacebook1(self):
        """Tests getting Twitter and Facebook when combined in one note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @chiefrabbi, Facebook: www.facebook.com/lordsacks'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'chiefrabbi')
        self.assertEqual(person.getFacebook(), 'https://www.facebook.com/lordsacks')

    def test_twitterAndFacebook2(self):
        """Tests getting Twitter and Facebook when combined in one note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @johnsentamu ; www.facebook.com/pages/John-Sentamu/25396296321'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'johnsentamu')
        self.assertEqual(person.getFacebook(), 'https://www.facebook.com/pages/John-Sentamu/25396296321')

    def test_email1(self):
        """Tests not getting an email when a postcode is supplied instead."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        # this is some real data :-(
        address2.email = 'FK10 3SA'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), None)

    def test_email2(self):
        """Test getting email when in email field."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'tas.mp@parliament.uk'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'tas.mp@parliament.uk')

    def test_email3(self):
        """Test getting one email when multiple set, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'raj@loomba.com / pritti@theloombafoundation.org'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'raj@loomba.com')

    def test_email4(self):
        """Test getting one email when multiple set, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'charles.allen@parliament.uk PA: gill.sharp@thisisglobal.com'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'charles.allen@parliament.uk')

    def test_email5(self):
        """Test getting one email when multiple set, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'damian.gannon@parliament.uk carole.wise@parliament.uk'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'damian.gannon@parliament.uk')

    def test_emailPeer1(self):
        """Test getting an email for a Peer and ignoring contactholmember@parliament.uk."""
        person = ModelPeer()

        address1 = ModelPeerAddress()
        address1.email = 'contactholmember@parliament.uk'
        person.addresses.append(address1)

        address2 = ModelPeerAddress()
        address2.email = 'victor@leadershipinmind.co.uk'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'victor@leadershipinmind.co.uk')

    def test_emailPeer2(self):
        """Test getting an email for a Peer and ignoring contactholmember@parliament.uk when extra padding in input."""
        person = ModelPeer()

        address1 = ModelPeerAddress()
        # note space at end - real data
        address1.email = 'contactholmember@parliament.uk '
        person.addresses.append(address1)

        address2 = ModelPeerAddress()
        address2.email = 'victor@leadershipinmind.co.uk'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'victor@leadershipinmind.co.uk')

    def test_getParliamentaryPhoneAndFax1(self):
        """Get Phone or Fax from Phone and Fax fields."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '0207 219 2807'
        address2.fax = '020 7219 5979'
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '0207 219 2807')
        self.assertEqual(person.getParliamentaryFax(), '020 7219 5979')

    def test_getParliamentaryPhoneAndFax2(self):
        """Get Phone or Fax when both in Phone field, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 1041 Fax: 0207 219 2405'
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 1041')
        self.assertEqual(person.getParliamentaryFax(), '0207 219 2405')

    def test_getParliamentaryPhoneAndFax3(self):
        """Get Phone or Fax when several phone numbers in input, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 3547, 020 7219 5099'
        address2.fax = '020 7219 4614'
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 3547')
        self.assertEqual(person.getParliamentaryFax(), '020 7219 4614')

    def test_getParliamentaryPhoneAndFax4(self):
        """Get Phone or Fax when several phone numbers in input, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 4432; 020 7219 6306'
        address2.fax = '020 7219 5952'
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 4432')
        self.assertEqual(person.getParliamentaryFax(), '020 7219 5952')

    def test_getParliamentaryPhoneAndFax5(self):
        """Get Phone or Fax when Fax in Phone field and several phone numbers in input, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 5135; 020 7219 2088; Fax 020 7219 4780'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 5135')
        self.assertEqual(person.getParliamentaryFax(), '020 7219 4780')

    def test_getParliamentaryPhoneAndFax6(self):
        """Test not getting Phone when Phone not in London and multiple phones."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '01709 331035/331036'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), None)
        self.assertEqual(person.getParliamentaryFax(), None)

    def test_getParliamentaryPhoneAndFax7(self):
        """Test getting phone with extra data in input."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 4936 (Office contact)'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 4936')
        self.assertEqual(person.getParliamentaryFax(), None)

    def test_getParliamentaryPhoneAndFax8(self):
        """Test not getting Phone when Phone not in London."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '01308 456891'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), None)
        self.assertEqual(person.getParliamentaryFax(), None)

    def test_getParliamentaryPhoneAndFax9(self):
        """Test getting London Phone when other phone specified first."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '0777 556 2776 / 020 7219 5353'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 5353')
        self.assertEqual(person.getParliamentaryFax(), None)

    def test_getParliamentaryPhoneAndFax10(self):
        """Get Phone or Fax when both in Phone field, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 5480   Fax. 020 7219 5979'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 5480')
        self.assertEqual(person.getParliamentaryFax(), '020 7219 5979')

    def test_getParliamentaryPhoneAndFax11(self):
        """Test getting phone with extra data in input."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = 'Tel: 020 7219 5353'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.getParliamentaryPhone(), '020 7219 5353')
        self.assertEqual(person.getParliamentaryFax(), None)

    def test_getConstituencyPostalAddress1(self):
        """Test getting Constituency address when address set."""
        person = ModelMP()

        address1 = ModelMPAddress()
        address1.type = 'Parliamentary'
        address1.address1 = 'House of Commons'
        person.addresses.append(address1)

        address2 = ModelMPAddress()
        address2.type = 'Constituency'
        address2.address1 = '94A Town Street'
        address2.address2 = 'Horsforth'
        person.addresses.append(address2)

        self.assertEquals(person.getConstituencyPostalAddress().address1, '94A Town Street')

    def test_getConstituencyPostalAddress2(self):
        """Test not getting Constituency address when it is not publicised."""
        person = ModelMP()

        address1 = ModelMPAddress()
        address1.type = 'Parliamentary'
        address1.address1 = 'House of Commons'
        person.addresses.append(address1)

        address2 = ModelMPAddress()
        address2.type = 'Constituency'
        address2.address1 = 'No constituency office publicised'
        person.addresses.append(address2)

        self.assertEquals(person.getConstituencyPostalAddress(), None)

if __name__ == '__main__':
    unittest.main()
