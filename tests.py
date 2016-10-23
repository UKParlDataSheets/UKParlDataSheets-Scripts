import unittest
from funcs import *


#
# License 3 clause BSD
# https://github.com/UKParlDataSheets/UKParlDataSheets-Scripts
#


class TestTwitter(unittest.TestCase):

    def test_no_crash_on_none_1(self):
        """If person has an empty adddress record, test no crashes."""
        person = ModelBase()

        address1 = ModelAddressBase()
        person.addresses.append(address1)

        self.assertEqual(person.get_twitter(), None)
        self.assertEqual(person.get_facebook(), None)
        self.assertEqual(person.get_email(), None)

    def test_twitter_1(self):
        """Tests getting Twitter when URL in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address_1 = 'https://twitter.com/LizBarkerLords'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'LizBarkerLords')

    def test_twitter_2(self):
        """Test getting Twitter when it's in a note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: TariqBt1'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'TariqBt1')

    def test_twitter_3(self):
        """Test getting Twitter when it's in a note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @lordphilofbrum'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'lordphilofbrum')

    def test_twitter_4(self):
        """Tests getting Twitter when URL in Address1, with extra params."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address_1 = 'https://twitter.com/LordRoyKennedy?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'LordRoyKennedy')

    def test_twitter_5(self):
        """Test getting Twitter when it's in a note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter - @delythjmorgan'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'delythjmorgan')

    def test_facebook_1(self):
        """Tests getting Facebook when HTTPS URL in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address_1 = 'https://www.facebook.com/marycreaghwakefield'
        person.addresses.append(address2)

        self.assertEqual(person.get_facebook(), 'https://www.facebook.com/marycreaghwakefield')

    def test_facebook_2(self):
        """Tests getting Facebook when HTTP URL in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address_1 = 'http://www.facebook.com/JeremyCorbynMP/'
        person.addresses.append(address2)

        self.assertEqual(person.get_facebook(), 'http://www.facebook.com/JeremyCorbynMP/')

    def test_facebook_3(self):
        """Tests getting Facebook when HTTPS URL with country/lang in Address1."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address_1 = 'https://en-gb.facebook.com/LordAltonofLiverpool/'
        person.addresses.append(address2)

        self.assertEqual(person.get_facebook(), 'https://en-gb.facebook.com/LordAltonofLiverpool/')

    def test_twitter_and_facebook_1(self):
        """Tests getting Twitter and Facebook when combined in one note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @chiefrabbi, Facebook: www.facebook.com/lordsacks'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'chiefrabbi')
        self.assertEqual(person.get_facebook(), 'https://www.facebook.com/lordsacks')

    def test_twitter_and_facebook_2(self):
        """Tests getting Twitter and Facebook when combined in one note in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @johnsentamu ; www.facebook.com/pages/John-Sentamu/25396296321'
        person.addresses.append(address2)

        self.assertEqual(person.get_twitter(), 'johnsentamu')
        self.assertEqual(person.get_facebook(), 'https://www.facebook.com/pages/John-Sentamu/25396296321')

    def test_email_1(self):
        """Tests not getting an email when a postcode is supplied instead."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        # this is some real data :-(
        address2.email = 'FK10 3SA'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), None)

    def test_email_2(self):
        """Test getting email when in email field."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'tas.mp@parliament.uk'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), 'tas.mp@parliament.uk')

    def test_email_3(self):
        """Test getting one email when multiple set, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'raj@loomba.com / pritti@theloombafoundation.org'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), 'raj@loomba.com')

    def test_email_4(self):
        """Test getting one email when multiple set, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'charles.allen@parliament.uk PA: gill.sharp@thisisglobal.com'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), 'charles.allen@parliament.uk')

    def test_email_5(self):
        """Test getting one email when multiple set, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.email = 'damian.gannon@parliament.uk carole.wise@parliament.uk'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), 'damian.gannon@parliament.uk')

    def test_email_peer_1(self):
        """Test getting an email for a Peer and ignoring contactholmember@parliament.uk."""
        person = ModelPeer()

        address1 = ModelPeerAddress()
        address1.email = 'contactholmember@parliament.uk'
        person.addresses.append(address1)

        address2 = ModelPeerAddress()
        address2.email = 'victor@leadershipinmind.co.uk'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), 'victor@leadershipinmind.co.uk')

    def test_email_peer_2(self):
        """Test getting an email for a Peer and ignoring contactholmember@parliament.uk when extra padding in input."""
        person = ModelPeer()

        address1 = ModelPeerAddress()
        # note space at end - real data
        address1.email = 'contactholmember@parliament.uk '
        person.addresses.append(address1)

        address2 = ModelPeerAddress()
        address2.email = 'victor@leadershipinmind.co.uk'
        person.addresses.append(address2)

        self.assertEqual(person.get_email(), 'victor@leadershipinmind.co.uk')

    def test_get_parliamentary_phone_and_fax_1(self):
        """Get Phone or Fax from Phone and Fax fields."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '0207 219 2807'
        address2.fax = '020 7219 5979'
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '0207 219 2807')
        self.assertEqual(person.get_parliamentary_fax(), '020 7219 5979')

    def test_get_parliamentary_phone_and_fax_2(self):
        """Get Phone or Fax when both in Phone field, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 1041 Fax: 0207 219 2405'
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 1041')
        self.assertEqual(person.get_parliamentary_fax(), '0207 219 2405')

    def test_get_parliamentary_phone_and_fax_3(self):
        """Get Phone or Fax when several phone numbers in input, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 3547, 020 7219 5099'
        address2.fax = '020 7219 4614'
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 3547')
        self.assertEqual(person.get_parliamentary_fax(), '020 7219 4614')

    def test_get_parliamentary_phone_and_fax_4(self):
        """Get Phone or Fax when several phone numbers in input, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 4432; 020 7219 6306'
        address2.fax = '020 7219 5952'
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 4432')
        self.assertEqual(person.get_parliamentary_fax(), '020 7219 5952')

    def test_get_parliamentary_phone_and_fax_5(self):
        """Get Phone or Fax when Fax in Phone field and several phone numbers in input, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 5135; 020 7219 2088; Fax 020 7219 4780'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 5135')
        self.assertEqual(person.get_parliamentary_fax(), '020 7219 4780')

    def test_get_parliamentary_phone_and_fax_6(self):
        """Test not getting Phone when Phone not in London and multiple phones."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '01709 331035/331036'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), None)
        self.assertEqual(person.get_parliamentary_fax(), None)

    def test_get_parliamentary_phone_and_fax_7(self):
        """Test getting phone with extra data in input."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 4936 (Office contact)'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 4936')
        self.assertEqual(person.get_parliamentary_fax(), None)

    def test_get_parliamentary_phone_and_fax_8(self):
        """Test not getting Phone when Phone not in London."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '01308 456891'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), None)
        self.assertEqual(person.get_parliamentary_fax(), None)

    def test_get_parliamentary_phone_and_fax_9(self):
        """Test getting London Phone when other phone specified first."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '0777 556 2776 / 020 7219 5353'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 5353')
        self.assertEqual(person.get_parliamentary_fax(), None)

    def test_get_parliamentary_phone_and_fax_10(self):
        """Get Phone or Fax when both in Phone field, in one format."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = '020 7219 5480   Fax. 020 7219 5979'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 5480')
        self.assertEqual(person.get_parliamentary_fax(), '020 7219 5979')

    def test_get_parliamentary_phone_and_fax_11(self):
        """Test getting phone with extra data in input."""
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.type = 'External/Private Office'
        address1.address_1 = 'My House'
        address1.address_2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.type = 'Parliamentary'
        address2.phone = 'Tel: 020 7219 5353'
        address2.fax = ''
        person.addresses.append(address2)

        self.assertEqual(person.get_parliamentary_phone(), '020 7219 5353')
        self.assertEqual(person.get_parliamentary_fax(), None)

    def test_get_constituency_postal_address_1(self):
        """Test getting Constituency address when address set."""
        person = ModelMP()

        address1 = ModelMPAddress()
        address1.type = 'Parliamentary'
        address1.address_1 = 'House of Commons'
        person.addresses.append(address1)

        address2 = ModelMPAddress()
        address2.type = 'Constituency'
        address2.address_1 = '94A Town Street'
        address2.address_2 = 'Horsforth'
        person.addresses.append(address2)

        self.assertEquals(person.get_constituency_postal_address().address_1, '94A Town Street')

    def test_get_constituency_postal_address_2(self):
        """Test not getting Constituency address when it is not publicised."""
        person = ModelMP()

        address1 = ModelMPAddress()
        address1.type = 'Parliamentary'
        address1.address_1 = 'House of Commons'
        person.addresses.append(address1)

        address2 = ModelMPAddress()
        address2.type = 'Constituency'
        address2.address_1 = 'No constituency office publicised'
        person.addresses.append(address2)

        self.assertEquals(person.get_constituency_postal_address(), None)

if __name__ == '__main__':
    unittest.main()
