import xml.etree.ElementTree as ET

xmlfiles = ['seatmap1.xml', 'seatmap2.xml']
ns = {
        'ns1': 'http://www.iata.org/IATA/EDIST/2017.2',
        'ns2': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ns3': 'http://www.opentravel.org/OTA/2003/05/common/'
     }

seatmap = {}

# parse the XML seatmap files seatmap1.xml and seatmap2.xml into a standardized JSON format that outputs the seatmap (by row)
def seatmap2():
    tree = ET.parse(xmlfiles[1])
    root = tree.getroot()
    # SeatDefinitionID map to values
    service_definition = {}

    service_def_list = root.find('./ns1:DataLists', ns)
    for service_def in service_def_list.findall('./ns1:SeatDefinitionList/', ns):
        service_definition[service_def.attrib['SeatDefinitionID']] = service_def.find('./ns1:Description/', ns).text

    # cabin wraps every row
    for cabin in root.findall('./ns1:SeatMap/ns1:Cabin', ns):
        for row in cabin.findall('./ns1:Row', ns):
            # aggregate the seat IDs in each row
            row_num = row.find('./ns1:Number', ns).text
            # numeral prefix for seat ID
            for seat in row.findall('./ns1:Seat', ns):
                for col in seat.findall('./ns1:Column', ns):
                    col_num = col.text
                    seat_num = row_num + col_num
                    for seat_def in seat.findall('./ns1:SeatDefinitionRef', ns):
                        if seat_def.text == 'SD3' or seat_def.text == 'SD4' or seat_def.text == 'SD5':
                            continue
                        seat_definition = service_definition[seat_def.text]
                        try:
                            seatmap[row_num][seat_num]
                        except KeyError:
                            continue
                        try:
                            seatmap[row_num][seat_num]['seat_type'] += ', '+seat_definition
                        except:
                            seatmap[row_num][seat_num]['seat_type'] = seat_definition

def seatmap1():
    tree = ET.parse(xmlfiles[0])
    root = tree.getroot()

    for cabin in root.findall('./ns2:Body/ns3:OTA_AirSeatMapRS/ns3:SeatMapResponses/ns3:SeatMapResponse/ns3:SeatMapDetails/ns3:CabinClass/ns3:RowInfo[@CabinType]', ns):
        row_num = cabin.attrib['RowNumber']
        seatmap[row_num] = {}
        cabin_class = cabin.attrib['CabinType']
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
            else:
                price = '$'+price.find('./ns3:Fee', ns).attrib['Amount']
            seatmap[row_num][seat_num]['price'] = price

            for feature in seat_info.findall('./ns3:Features', ns):
                if feature.text != 'Other_':
                    position = feature.text
                    seatmap[row_num][seat_num]['position'] = position
                elif feature.text == 'Other_':
                    extension = feature.attrib['extension']
                    seatmap[row_num][seat_num]['extension'] = extension

      
if __name__ == "__main__":
    seatmap1()
    seatmap2()
