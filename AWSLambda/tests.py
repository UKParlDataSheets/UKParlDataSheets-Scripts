import unittest
from funcs import *


class TestTwitter(unittest.TestCase):


    def test_noCrashOnNone1(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        person.addresses.append(address1)

        self.assertEqual(person.getTwitter(), None)



    def test_1(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'https://twitter.com/LizBarkerLords'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'LizBarkerLords')


    def test_2(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: TariqBt1'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'TariqBt1')



    def test_3(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter: @lordphilofbrum'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'lordphilofbrum')

    def test_4(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.address1 = 'https://twitter.com/LordRoyKennedy?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'LordRoyKennedy')



    def test_5(self):
        person = ModelBase()

        address1 = ModelAddressBase()
        address1.address1 = 'My House'
        address1.address2 = 'My Street'
        person.addresses.append(address1)

        address2 = ModelAddressBase()
        address2.note = 'Twitter - @delythjmorgan'
        person.addresses.append(address2)

        self.assertEqual(person.getTwitter(), 'delythjmorgan')

if __name__ == '__main__':
    unittest.main()
