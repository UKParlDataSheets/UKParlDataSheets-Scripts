import unittest
from funcs import *


#
# License 3 clause BSD https://github.com/UKParlDataSheets/UKParlDataSheets-Scripts
#


class TestTwitter(unittest.TestCase):


    def test_noCrashOnNone1(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        person.addresses.append(address1)

        self.assertEqual(person.getTwitter(), None)
        self.assertEqual(person.getFacebook(), None)
        self.assertEqual(person.getEmail(), None)



    def test_twitter1(self):
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
        person = ModelPeer()

        address1 = ModelPeerAddress()
        address1.email = 'contactholmember@parliament.uk'
        person.addresses.append(address1)

        address2 = ModelPeerAddress()
        address2.email = 'victor@leadershipinmind.co.uk'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'victor@leadershipinmind.co.uk')


    def test_emailPeer2(self):
        person = ModelPeer()

        address1 = ModelPeerAddress()
        # note space at end - real data
        address1.email = 'contactholmember@parliament.uk '
        person.addresses.append(address1)

        address2 = ModelPeerAddress()
        address2.email = 'victor@leadershipinmind.co.uk'
        person.addresses.append(address2)

        self.assertEqual(person.getEmail(), 'victor@leadershipinmind.co.uk')



if __name__ == '__main__':
    unittest.main()
