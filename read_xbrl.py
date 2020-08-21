import re
from dateutil import parser
from bs4 import BeautifulSoup as BS  

# August 2020
# Parse iXBRL reports, published as .html or .xhtml file from local
# Minimal example: Use of imports is kept to an absolute minimum 
# Tested on GLEIF annual report: https://www.gleif.org/en/about/governance/annual-report/

# Define path and import html or xhtml from local
mypath = "C:/yourpath/xbrl/"

# To read from online source just change this part
soup = BS(open(mypath+"gleif-19ar.signed4.xhtml", "rb"), "html.parser")
#soup = BS(open(mypath+"evonik.xhtml", "rb"), "html.parser")

# Set up a file to store the results
outFile = open(mypath+"myxbrltable.csv", 'w', newline='', encoding='utf8')
outFile.write("position;tag;tagtype;content;numeric_content;unit;date1;date2;identi;dim;decimals;sign;form;scale \n")

# Loop over elements in html/xhtml
position = 0
for c, element in enumerate(soup.find_all()):
    # Iterate over all XBLR content (identif. by "contextref")
    if "contextref" in element.attrs:
        # See all relevant attributes of an XBRL tag
        #print(element.attrs)

        #################################################
        # Retrieve content per tag

        # Name of entry (aka name of XBLR tag)
        tag = str(element.attrs['name'])
        
        # Tagtype (standard ifrs vs. custom)
        if "ifrs-full" in tag:
            tagtype="IFRS"
        else:
            tagtype="custom"        
        tag = tag[tag.rfind(":")+1:]

        # Get content (text in tag)
        # This is e.g. the numeric value of a position
        content = element.text
        content = content.replace('\n', '').replace('\r', '').lstrip()

        # Get unit (like USD or EUR)
        try:
            # Somewhere hidden at top of file
            #  <xbrli:unit id="ibee02267a6cf4a178ffe2b57731cf158_0f1b2a3d-0585-35e4-9bf4-b4f1337c8ffb">
            #  <xbrli:measure>iso4217:USD</xbrli:measure>
            unit = str(soup.find(id=element['unitref']).text)
            unit = unit.strip().replace('\n', '').replace('\r', '')
        except:
            unit = "nn"
        
        # Get time and identity reference 
        # !!! Possibly instable solution -> to be tested
        try:
            identi="nn"
            date1="nn"
            date2="nn"
            dim="nn"
            #print(soup.find(id=element['contextref']))
            for c in soup.find_all(id=element['contextref']):
                # To plain text
                res = c.text
                res = res.replace('\n', '').replace('\r', '').lstrip()
                # Find date by regex
                match = re.search(r'\d{4}-\d{2}-\d{2}', res)
                date1 = match.group()
                # Remove date from string
                res = res.replace(date1,"")
                # Find second date
                match = re.search(r'\d{4}-\d{2}-\d{2}', res)
                date2 = match.group()
                # Remove second date
                res = res.replace(date2,"")
                # Find ifrs-ref if present
                dim = res[res.find("ifrs"):]
                if len(dim)>2:
                    res = res.replace(dim,"")
                else:
                    dim = "nn"
                # Remove ifrs reference if prsent
                identi = res
        except:
            pass

        # Internal ID of tag
        try:
            cid = str(element.attrs['id'])
        except:
            cid = "nn"
        
        # Number of decimals
        try:
            decimals = str(element.attrs['decimals'])
        except:
            decimals = "nn"

        # Sign of numeric value (only if negative, aka. "minus")
        try:
            sign = str(element.attrs['sign'])
        except:
            sign = ""

        # Format of numerical content (decimal separator et al.)
        # https://www.xbrl.org/Specification/inlineXBRL-transformationRegistry/REC-2015-02-26/inlineXBRL-transformationRegistry-REC-2015-02-26.html
        try:
            form = str(element.attrs['format'])
        except:
            form = "nn"
        
        # Scale of numerical content
        # E.g. when figures are expressed in "million EUR"
        # Numerical values to be transformed by: numcontent * 10**int(scale)
        try:
            scale = str(element.attrs['scale'])
        except:
            scale = "nn"
        
        #################################################
        ## Prepare content
        content = sign + content

        # Check if content is a number if true assign numerical value to separate variable
        numcontent = "0"
        try:
            x=content.replace(",","").replace(".","").replace("-","")
            if x.isdigit()==True: 
                # If number... do formating
                
                # !!! ALTERNATIVE FORMATS POSSIBLE -> to be tested
 
                # CASE: Comma decimal separatot to UK/US
                if form=="ixt:numcomma" or form=="ixt:numdotcomma" or form=="numspacecomma":
                    numcontent = content.replace(".","")
                    numcontent = content.replace(",",".")
                # CASE: UK/US format
                if form=="ixt:numcommadot" or form=="ixt:numspacedot" or form=="ixt:num-dot-decimal":
                    numcontent = content.replace(",","")
                else:
                    pass
                
                # As float
                numcontent = float(numcontent)
                # Scale (using "10 to the power of" scale)
                if scale!="nn":
                    numcontent = numcontent * 10**int(scale)
                    numcontent = str(numcontent)
            
            position = position+1
        except:
            pass

        # Write to csv file
        outFile.write(str(position) +";"+ tag +";"+ tagtype +";"+ content +";"+ numcontent +";"+ unit +";"+date1 +";"+date2 + ";" +identi +";"+dim +";"+decimals +";"+sign +";"+form +";"+scale+"\n")

outFile.close()
