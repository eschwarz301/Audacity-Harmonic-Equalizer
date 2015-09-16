__author__ = 'eschwarz'
'''
Creates an .xml file containing information for an equalization curve capable of isolating a user defined frequency and its
harmonics. The output file can be imported to Audacity with the "Save/Manage Curves" option under Effect/Equalization in the Audacity toolbar.
'''
import xml.etree.ElementTree as ET

class IsolateHarmonic(object):

    def __init__(self):
        self.eq_name = ''
        self.frequency = 0.0
        self.harmonics = 0
        self.reduction = 0.0

    def user_input(self):
        self.eq_name = input('Name this Equalizer: ')
        self.frequency = float(input('What is the fundamental frequency of the note you would like to isolate? '))
        self.harmonics = int(input('How many harmonics would you like to include? '))
        self.reduction = float(input('How much would you like to reduce non-harmonics (dB) by? '))

    def create_curve(self):
        self.root = ET.Element('equalizationeffect')
        self.EQ = ET.SubElement(self.root, 'curve', attrib={'name':self.eq_name})
        ET.SubElement(self.EQ, 'point f="20.000" d="-%f"' % self.reduction)

        for i in range(1, self.harmonics+2): 
            ET.SubElement(self.EQ, '{}{}{}{}{}'.format('point f="',i*self.frequency-1.5,'" d="-',self.reduction,'"'))
            ET.SubElement(self.EQ, '{}{}{}'.format('point f="',i*self.frequency-1,'" d="0.000"'))
            ET.SubElement(self.EQ, '{}{}{}'.format('point f="',i*self.frequency+1,'" d="0.000"'))
            ET.SubElement(self.EQ, '{}{}{}{}{}'.format('point f="',i*self.frequency+1.5,'" d="-',self.reduction,'"'))

        curve = ET.SubElement(self.EQ, 'point f="22000.000" d="-%f"' % self.reduction)

    def xml_format(self, xml_element, level=0):
        i = "\n" + level*"  "
        if len(xml_element):
            if not xml_element.text or not xml_element.text.strip():
                xml_element.text = i + "  "
            if not xml_element.tail or not xml_element.tail.strip():
                xml_element.tail = i
            for xml_element in xml_element:
                self.xml_format(xml_element, level+1)
            if not xml_element.tail or not xml_element.tail.strip():
                xml_element.tail = i
        else:
            if level and (not xml_element.tail or not xml_element.tail.strip()):
                xml_element.tail = i

# Example Program
A = IsolateHarmonic()
A.user_input()
A.create_curve()
A.xml_format(A.root)
tree = ET.ElementTree(A.root)
tree.write("%s.xml" % A.eq_name)