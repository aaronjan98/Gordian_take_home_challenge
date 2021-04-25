import xml.etree.ElementTree as ET

xmlfiles = ['seatmap1.xml', 'seatmap2.xml']
ns = {
        'ns1': 'http://www.iata.org/IATA/EDIST/2017.2',
        'ns2': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ns3': 'http://www.opentravel.org/OTA/2003/05/common/'
     }

# parse the XML seatmap files seatmap1.xml and seatmap2.xml into a standardized JSON format that outputs the seatmap (by row)
def seatmap2():
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
            row_num = row.find('./ns1:Number', ns).text
            # numeral prefix for seat ID
            for seat in row.findall('./ns1:Seat', ns):
                # seat_ids = []
                for col in seat.findall('./ns1:Column', ns):
                    col_num = col.text
                    # seat_ids.append(row_num + col_num)
                    print(row_num + col_num)
                    for seat_def in seat.findall('./ns1:SeatDefinitionRef', ns):
                        print('seat definition: ', service_definition[seat_def.text])
                # print(seat_ids)

def seatmap1():
    tree = ET.parse(xmlfiles[0])
    root = tree.getroot()
    
    seatmap = {}

    for cabin in root.findall('./ns2:Body/ns3:OTA_AirSeatMapRS/ns3:SeatMapResponses/ns3:SeatMapResponse/ns3:SeatMapDetails/ns3:CabinClass/ns3:RowInfo[@CabinType]', ns):
        seatmap[cabin.attrib['RowNumber']] = {}
        row_num = cabin.attrib['RowNumber']
        cabin_class = cabin.attrib['CabinType']
        print('cabin class: ', cabin_class)
        for seat_info in cabin.findall('./ns3:SeatInfo', ns):
            summary = seat_info.find('./ns3:Summary', ns)
            seat_num = summary.attrib['SeatNumber']
            availability = summary.attrib['AvailableInd']
            seatmap[row_num].update({ seat_num: {
                'available': availability,
                'cabin class': cabin_class
            }})
            price = seat_info.find('./ns3:Service', ns)
            if price == None:
                price = 'N/A'
                print('price: ', price)
            else:
                price = price.find('./ns3:Fee', ns).attrib['Amount']
            seatmap[row_num][seat_num]['price'] = price

            for feature in seat_info.findall('./ns3:Features', ns):
                if feature.text == 'Other_':
                    extension = feature.attrib['extension']
                    seatmap[row_num][seat_num]['extension'] = extension
                else:
                    feature = feature.text
                    seatmap[row_num][seat_num]['feature'] = feature
    print(seatmap)

      
if __name__ == "__main__":
    # seatmap2()
    seatmap1()
