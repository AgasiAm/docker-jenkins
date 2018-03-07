class MyXmlCsvConvert:


        import xml.etree.ElementTree as ET
        import csv as csv
        import re as re

 

        def __init__(self, v_xmlfile, v_csvfile):
            self.v_xmlfile = v_xmlfile
            self.v_csvfile = v_csvfile
            self.tree = self.ET.parse(v_xmlfile)
            self.root = self.tree.getroot()

        def CreateHeader(self):
            audit_data = open(self.v_csvfile, 'a')
            csvwriter = self.csv.writer(audit_data)
            audit = []
            for text in self.root.iter():
                if '\n' not in text.text and text.text:
                    audit.append(self.re.compile("}").split(text.tag)[1])

            csvwriter.writerow(audit)

            audit_data.close()

            audit = []

 

        def FillCsv(self):
            audit_data = open(self.v_csvfile, 'a')
            csvwriter = self.csv.writer(audit_data)

            for rng in range(len(self.root.getchildren())):
                audit = []
                for child in self.root[rng].iter():
                   if child.text is not None and child.text is not '\n': 
                       audit.append(child.text)
                csvwriter.writerow(audit)
            audit_data.close()

            audit = []


        def PrintVars(self):
            print 'XML_FILE ->', self.v_xmlfile
            print 'CSV_FILE ->', self.v_csvfile
