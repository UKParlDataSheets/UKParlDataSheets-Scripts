import unittest
from funcs import *


class TestTwitter(unittest.TestCase):


    def test_noCrashOnNone1(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        person.addresses.append(address1)

        self.assertEqual(person.getTwitter(), None)
        self.assertEqual(person.getFacebook(), None)



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



if __name__ == '__main__':
    unittest.main()
