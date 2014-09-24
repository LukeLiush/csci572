from html import XHTML
import csv
import magic
import sys
import getopt
import os

_helpMessage = '''
Usage: TSVParser [-t tsv file] [-x xhtml file] [-c column headers txt file]

Options:
-t tsv file, --tsv=file
    Parse the given TSV file and turn it into JSON.
-x xhtml file --xhtml=file
    Output the named XHTML file.
-c column headers file --cols=file
    Use the provided column headers to parse the TSV and to name fields in the JSON.
'''

class _Usage(Exception):
    '''An error for problems with arguments on the command line.'''
    def __init__(self, msg):
        self.msg = msg
        
def checkFilePath(filePath, checkPath=True):
    if checkPath:
        return filePath <> None and os.path.isfile(filePath)
    else:
        return filePath <> None and not os.path.exists(filePath)

def main(argv=None):    
    if argv is None:
     argv = sys.argv
    try:
        try:
           opts, args = getopt.getopt(argv[1:], 't:x:c:', ['tsv=', 'xhtml=', 'cols='])
        except getopt.error, msg:
           raise _Usage(msg) 
        if len(opts) == 0:
           raise _Usage(_helpMessage)
        
        tsvFilePath = None
        xhtmlFilePath = None
        colHeaderFilePath = None
        cols = []
        
        for option, value in opts:
            if option in ('-t', '--tsv'):
                tsvFilePath = value
            elif option in ('-x', '--xhtml'):
                xhtmlFilePath = value
            elif option in ('-c', '--cols'):
                colHeaderFilePath = value    
                
        if not checkFilePath(tsvFilePath) or not checkFilePath(colHeaderFilePath):
            raise _Usage("")
            
        xhtml = XHTML()
        table = xhtml.table()
            
        with open(colHeaderFilePath) as headers:
            cols = headers.read().splitlines()
            
        tableHeader = table.tr()
        for col in cols:
            if ":" in col:
                continue
            tableHeader.th(col)
            
        theMagic = magic.Magic(mime_encoding=True)
            
        with open(tsvFilePath) as tsv:
            for line in csv.reader(tsv, dialect="excel-tab"):
                diff = len(cols) - len(line)
                if diff > 0:
                    print >>sys.stderr, "Column Headers and Row Values Don't Match up: numCols: [" + str(len(cols)) + "]: numRowValues: [" + str(len(line)) + "]"
            
                tableRow = table.tr()
                for num in range(0, len(cols)):
                    if ":" in cols[num]:
                        continue                    
                    
                    if line[num] <> None and line[num].lstrip() <> '':
                        val = line[num]                       
                    else:
                        val = ''
                    
                    tableRow.td(val)
                    
        f = open(xhtmlFilePath, "w")
        print >>f, xhtml
        f.close()
          
    except _Usage, err:
       print >>sys.stderr, sys.argv[0].split('/')[-1] + ': ' + str(err.msg)
       return 2      
    
if __name__ == "__main__":
    sys.exit(main())