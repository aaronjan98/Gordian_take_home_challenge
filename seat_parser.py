import xml.etree.ElementTree as ET

xmlfiles = ['seatmap1.xml', 'seatmap2.xml']
ns = {  'ns1': 'http://www.iata.org/IATA/EDIST/2017.2',
        'ns2': 'http://www.iata.org/IATA/EDIST/2017.2/CR129'
     }

# parse the XML seatmap files seatmap1.xml and seatmap2.xml into a standardized JSON format that outputs the seatmap (by row)
def main():
    tree = ET.parse(xmlfiles[1])
    root = tree.getroot()
    for value in root.findall('./ns1:SeatMap/ns1:Cabin/ns1:Row', ns):
        print(value.find('./ns1:Number', ns).text)
        for col in value.findall('./ns1:Seat/ns1:Column', ns):
            print(col.text)
      
if __name__ == "__main__":
    main()
