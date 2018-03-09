class MyXmlCsvConvert:


        import xml.etree.ElementTree as ET
        import csv as csv
        import re as re

 

        def __init__(self, v_xmlfile):
            self.v_xmlfile = v_xmlfile
            self.tree = self.ET.parse(v_xmlfile)
            self.root = self.tree.getroot()

        def CreateHeader(self):
#            audit_data = open(self.v_csvfile, 'a')
            csvwriter = self.csv.writer(audit_data)
            audit = []
            for text in self.root.iter():
                if '\n' not in text.text and text.text:
                    audit.append(self.re.compile("}").split(text.tag)[1])

            csvwriter.writerow(audit)

            audit_data.close()

            audit = []

 

        def FillCsv(self):
            for rng in range(len(self.root.getchildren())):
                audit = []
                stmt_type=self.root[rng].findtext('{http://xmlns.oracle.com/oracleas/schema/dbserver_audittrail-11_2.xsd}Stmt_Type')
                for child in self.root[rng].iter():
                    if child.text is not None and child.text is not '\n': 
                        audit.append(child.text)
                self.__WriteToFile(stmt_type,audit)
            audit = []

 
        def __WriteToFile(self,stmt_type,audit):
                if stmt_type=='1':
                   file_name=self.v_xmlfile+'_select.csv'
                elif stmt_type=='2':
                   file_name=self.v_xmlfile+'_insert.csv'
                elif stmt_type=='4':
                   file_name=self.v_xmlfile+'_update.csv'
                elif stmt_type=='8':
                   file_name=self.v_xmlfile+'_delete.csv'
                else:
                   file_name=self.v_xmlfile+'_uncknown.csv'
                
                audit_data = open(file_name, 'a')
                csvwriter = self.csv.writer(audit_data)
                csvwriter.writerow(audit)
                audit_data.close()



        def PrintVars(self):
            print 'XML_FILE ->', self.v_xmlfile
#            print 'CSV_FILE ->', self.v_csvfile
