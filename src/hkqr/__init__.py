import json, binascii, os

class HKQR:
    def __init__(self, fps_id):
        self.fps_id = fps_id
        self.debug = False


        # Load the specs first
        #self.specs_file = open("./specs.json", "r")
        path = os.path.join( os.path.dirname( os.path.abspath(__file__)) , 'specs.json' )

        with open( path, 'r') as specs_file:
            spec_string = specs_file.read().replace('\n', '')

        self.specs = json.loads(spec_string)['specs']
        self.templates = json.loads(spec_string)['templates']

    def __create_string_from_id_and_value( self, id, value ):
        length_zfill = ('%s' % len(value)).zfill(2)
        #return f'{id}{length_zfill}{value}'
        return '%s%s%s' % (id, length_zfill, value)

    def __substr(  self, s, index, length ):
        return s[index:(index + length)]

    def __payload_unwind( self,  qrcode_text, level="" ):
        index = 0
        textLen = len(qrcode_text)

        results = []

        while (index < textLen):
            id = self.__substr(qrcode_text, index, 2)
            length = self.__substr(qrcode_text, index + 2, 2)
            value = self.__substr(qrcode_text, index + 4, int(length))
            index += 4 + int(length)
            s = self.specs[id]
            return_dict = {
                'id': id,
                'name': s['name'],
                'length': length,
                'value': value,
                'comment': s['comment']
            }

            if self.debug:
                print("%sID: %s" % (level, id))
                print("%sLength: %s" % (level, length))
                print("%sComment: %s" % (level, s['comment']))
                print( '\033[1m' + "%svalue: %s" % (level, value) + '\033[0m')
                print("--------")

            if id in self.templates:
                if 'dataObjectsById' in self.templates[id]:
                    dataobjects = self.__payload_unwind(value, level="    ")
                    return_dict['dataobjects'] = dataobjects
            if id == '26':
                dataobjects = self.__payload_unwind(value, level="    ")
                return_dict['dataobjects'] = dataobjects

            results.append(return_dict)

        return results

    def decode_qrcode( self, qrcode_text):
        results = self.__payload_unwind(qrcode_text)

        return results

    def create_hkqr_code(self, amount, **kwargs ):
        # Use a template, with sample FPS ID: 9999999
        qrcode_9999999_with_amount = "00020101021226270012hk.com.hkicl0207999999952040000530334454031235802HK5902NA6002HK630484E1"
        results = self.decode_qrcode(qrcode_9999999_with_amount)

        # 26: Swap the Payment Number
        # Now, swap 07|9999999 to something else
        #fps_id = 'hsbc-fps@fleurhongkong.com'  # "8577991"

        if self.fps_id.startswith("+852"):
            fps_prefix = "03"
        elif self.fps_id.find("@") > 0:
            fps_prefix = "04"
        else:
            fps_prefix = "02"

        fps_value = self.__create_string_from_id_and_value( fps_prefix, self.fps_id)
        #extra = self.__create_string_from_id_and_value( "05", "181101111111")

        payload_26_value = '0012hk.com.hkicl%s' % fps_value

        payload_26 = {
            'id': '26',
            'length': ('%s' % len(payload_26_value)).zfill(2),
            'value': payload_26_value
        }

        # 54: Payment Amount
        payment_amount = str(amount)

        payload_54 = {
            'id': '54',
            'length': ('%s' % len(payment_amount)).zfill(2),
            'value': payment_amount
        }

        #
        # Now, swap payload 26 and 54
        #

        results_replacement = []
        for r in results:
            if r['id'] == '26':
                # print( f'id == 26: swapped!')
                results_replacement.append(payload_26)
            elif r['id'] == '54':
                # print(f'id == 54: swapped!')
                results_replacement.append(payload_54)
            elif r['id'] == '63':
                # print(f'Skipped checksum')
                pass
            else:
                # print( f"{r['id']}: {r['value']}")
                results_replacement.append(r)

        # Append 62 if there is bill number
        if 'bill_number' in kwargs:
            bill_number_62_value = self.__create_string_from_id_and_value( "01", kwargs['bill_number'] )
            results_replacement.append({
                'id' : '62',
                'length' : ('%s' % len(bill_number_62_value)).zfill(2),
                'value': bill_number_62_value
            })

        # Append 62 with ID 05 if there is reference id
        if 'reference_id' in kwargs:
            reference_id_62_reference_value = self.__create_string_from_id_and_value( "05", kwargs['reference_id'] )
            results_replacement.append({
                'id' : '62',
                'length' : ('%s' % len(reference_id_62_reference_value)).zfill(2),
                'value': reference_id_62_reference_value
            })

        encoded_value = ""
        for r in results_replacement:
            #encoded_value = f"{encoded_value}{r['id']}{r['length']}{r['value']}"
            encoded_value = "%s%s%s%s" % (encoded_value, r['id'], r['length'], r['value'])

        # Calculate the CRC 16 value
        crc16 = binascii.crc_hqx(str.encode('%s6304' % encoded_value), 0xffff)
        crc_value = ('6304%04x' % crc16).upper()

        encoded_value = '%s%s' % (encoded_value, crc_value) #f"{encoded_value}{crc_value}"
        return encoded_value


