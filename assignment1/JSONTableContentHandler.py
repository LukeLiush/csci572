from lxml import etree
from BeautifulSoup import BeautifulSoup
import sys
import getopt
import os

_helpMessage = '''
Usage: JSONTableContentHanlder [-o output path] [-x xhtml file]

Options:
-o output path, --output=path
    Output to the named path.
    
-x xhtml file, --xhtml=file
    Parse the given XHTML file and turn it into JSON, one file per row.
'''

class _Usage(Exception):
    '''An error for problems with arguments on the command line.'''
    def __init__(self, msg):
        self.msg = msg
        
def checkFilePath(filePath, checkFile=True):
    if checkFile:
        return filePath <> None and os.path.isfile(filePath)
    else:
        return filePath <> None and os.path.isdir(filePath)

def main(argv=None):    
    if argv is None:
     argv = sys.argv
    try:
        try:
           opts, args = getopt.getopt(argv[1:], 'o:x:', ['output=', 'xhtml='])
        except getopt.error, msg:
           raise _Usage(msg) 
        if len(opts) == 0:
           raise _Usage(_helpMessage)
        
        xhtmlFilePath = None
        outputPath = None
                
        for option, value in opts:
            if option in ('-x', '--xhtml'):
                xhtmlFilePath = value
            elif option in ('-o', '--output'):
                outputPath = value    
                
        if not checkFilePath(xhtmlFilePath) or not checkFilePath(outputPath, False):
            raise _Usage(_helpMessage)
            
                    
        with open(xhtmlFilePath) as xhtml:
            xhtmlContent = xhtml.read()
            soup = BeautifulSoup(xhtmlContent)
            parser = etree.XMLParser(recover=True)
            table = etree.XML(str(soup.table), parser)
            rows = iter(table)
            headers = [col.text for col in next(rows)]
            for row in rows:
                values = [col.text for col in row]
                print dict(zip(headers, values))
            
                                
        #f = open(xhtmlFilePath, "w")
        #print >>f, xhtml
        #f.close()
          
    except _Usage, err:
       print >>sys.stderr, sys.argv[0].split('/')[-1] + ': ' + str(err.msg)
       return 2      
    
if __name__ == "__main__":
    sys.exit(main())