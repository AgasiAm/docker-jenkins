class XmlCsvConvert:


        import xml.etree.ElementTree as ET
        import csv as csv
        import re as re
        import os as os
        import sys as sys
        import datetime as datetime

 

        def __init__(self, v_xmlpath):
            self.v_xmlpath = v_xmlpath
            self.xml_file_name=''
            self.error_file=self.os.path.join(self.v_xmlpath,'error.log')

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


        def Run(self):
            try:
                self.GetFileList()
            except:
                err = self.sys.exc_info()
                print err
                with open(self.error_file,'a') as fd_err:
                    fd_err.write('\n'+str(self.datetime.datetime.now())+'\n')
                    for index in range(len(err)):
                        fd_err.write(str(err[index])+'\n')
                        index=index+1


        def InitXMLTree(self,fd):
            tree = self.ET.parse(fd)
            root = tree.getroot()
            self.FillCsv(root)


        def GetFileList(self):
            for file in self.os.listdir(self.v_xmlpath):
                if file.endswith(".xml"):
                    self.xml_file_name=self.os.path.join(self.v_xmlpath, file)
                    if self.os.access(self.xml_file_name,self.os.R_OK):
                        if len(self.os.popen("lsof %r" % self.xml_file_name).readline()):
                            print 'File %r in use' % self.xml_file_name
                        else:
                            with open(self.xml_file_name,'r') as fd:
                                self.InitXMLTree(fd)
                                self.os.rename(self.xml_file_name,self.xml_file_name+'.done')
                    else:
                        print 'File %r not accessible' % self.xml_file_name



        def FillCsv(self,root):
            for rng in range(len(root.getchildren())):
                audit = []
                stmt_type=root[rng].findtext('{http://xmlns.oracle.com/oracleas/schema/dbserver_audittrail-11_2.xsd}Stmt_Type')
                for child in root[rng].iter():
                    if child.text is not None and child.text is not '\n': 
                        audit.append(child.text)
                self.__WriteToFile(stmt_type,audit)
            audit = []




        def __WriteToFile(self,stmt_type,audit):
                if stmt_type=='1':
                   file_name=self.xml_file_name+'_select.csv'
                elif stmt_type=='2':
                   file_name=self.xml_file_name+'_insert.csv'
                elif stmt_type=='4':
                   file_name=self.xml_file_name+'_update.csv'
                elif stmt_type=='8':
                   file_name=self.xml_file_name+'_delete.csv'
                else:
                   file_name=self.xml_file_name+'_uncknown.csv'
                
                audit_data = open(file_name, 'a')
                csvwriter = self.csv.writer(audit_data)
                csvwriter.writerow(audit)
                audit_data.close()



        def PrintVars(self):
            print 'XML_FILE ->', self.v_xmlpath
#            print 'CSV_FILE ->', self.v_csvfile
