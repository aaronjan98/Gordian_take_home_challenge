import xml.etree.ElementTree as ET

xmlfiles = ['seatmap1.xml', 'seatmap2.xml']
ns = {
        'ns1': 'http://www.iata.org/IATA/EDIST/2017.2',
        'ns2': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ns3': 'http://www.opentravel.org/OTA/2003/05/common/'
     }

# parse the XML seatmap files seatmap1.xml and seatmap2.xml into a standardized JSON format that outputs the seatmap (by row)
def main():
    tree = ET.parse(xmlfiles[1])
    root = tree.getroot()
    seat_position = {
        'A': None,
        'B': None,
        'C': None,
        'D': None,
        'E': None,
        'F': None
    }
    # SeatDefinitionID map to values
    service_definition = {}

    service_def_list = root.find('./ns1:DataLists', ns)
    # for service_def in service_def_list.findall('./ns1:SeatDefinitionList/SeatDefinition', ns):
    for service_def in service_def_list.findall('./ns1:SeatDefinitionList/', ns):
        service_definition[service_def.attrib['SeatDefinitionID']] = service_def.find('./ns1:Description/', ns).text
    print(service_definition)

    # cabin wraps every row
    for cabin in root.findall('./ns1:SeatMap/ns1:Cabin', ns):
        pos_a = pos_b = pos_c = pos_d = pos_e = pos_f = None
        # get seat position in the cabin layout
        for layout in cabin.findall('./ns1:CabinLayout', ns):
            for col_pos in layout.findall('./ns1:Columns', ns):
                if col_pos.text == None:
                    seat_position[col_pos.attrib['Position']] = 'Middle'
                    continue
                seat_position[col_pos.attrib['Position']] = col_pos.text
        for row in cabin.findall('./ns1:Row', ns):
            # aggregate the seat IDs in each row
            seat_ids = []
            row_num = row.find('./ns1:Number', ns).text
            # numeral prefix for seat ID
            for seat in row.findall('./ns1:Seat/ns1:Column', ns):
                col_num = seat.text
                seat_ids.append(row_num + col_num)
            print(seat_ids)

def seatmap1():
    tree = ET.parse(xmlfiles[0])
    root = tree.getroot()

    for cabin_class in root.findall('./ns2:Body/ns3:OTA_AirSeatMapRS/', ns):
        print(cabin_class.tag)
      
if __name__ == "__main__":
    # main()
    seatmap1()
