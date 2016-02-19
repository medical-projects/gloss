from hl7.client import MLLPClient
import hl7
import time


patient_update = """
MSH|^~\&|CARECAST|UCLH|ELCID||201412061201||ADT^A31|PLW21228462730556545|P|2.2|||AL|NE
EVN|A31|201412061201||CREG|U440208^KHATRI^BHAVIN|
PID|||50092915^^^^UID~^^^^NHS||TESTING MEDCHART^MEDHCART FIRSTNAME^MEDCHART JONES^^MR||19870612|M|||12 THE DUNTINGDON ROAD,&^SECOND STREET, ADDRESS&^LINE 3, FORTH^ADDRESS, LONDON^N2 9DU^^^^EAST FINCHLEY^~12 THE DUNTINGDON ROAD&SECOND STREET^ADDRESS LINE 3&FORTH ADDRESS^LONDON^^N2 9DU^^^^EAST FINCHLEY^||020811128383~07000111122~EMAI@MEDCHART.COM|02048817722|F1^^^I|M|1A|||||A||||||||
PD1|||NU^^^^^&&^^&&|375883^CURZON^RN^^^DR^^^&&^^^^^G8903132&&~P816881^43 DERBE ROAD^ST.ANNES-ON-SEA^LANCASHIRE^^^^FY8 1NJ^^01253 725811^^^^P81688&1&~410605^PATEL^A^^^^^^^^^^^D2639749&&~V263972^234 DENTAL CARE^234 EDGEWARE ROAD^LONDON^^^^W2  1DW^^^^^^V26397&2||9||||||
NK1|1|MEDCHART BROTHERNOK^NOK FIRST NAME^NOK SECONDNAME^^|BROTHER|65 ADDRESS ONE, ADDRESS&^TWO, NOK ADDRESS THREE,&^NOK ADDRESS FOUR,^LONDON,^N2 9DU^^^^MIDDLESEX^~65 ADDRESS ONE&ADDRESS TWO^NOK ADDRESS THREE&NOK ADDRESS FOUR^LONDON^^N2 9DU^^^^MIDDLESEX^|0809282822|0899282727|"""

patient_death = """
MSH|^~\&|CARECAST|UCLH|ELCID||201412061201||ADT^A31|PLW21228462730556545|P|2.2|||AL|NE
EVN|A31|201412061201||CREGS|U440208^KHATRI^BHAVIN|
PID|||50092915^^^^UID~^^^^NHS||TESTING MEDCHART^MEDHCART FIRSTNAME^MEDCHART JONES^^MR||19870612|M|||12 THE DUNTINGDON ROAD,&^SECOND STREET, ADDRESS&^LINE 3, FORTH^ADDRESS, LONDON^N2 9DU^^^^EAST FINCHLEY^~12 THE DUNTINGDON ROAD&SECOND STREET^ADDRESS LINE 3&FORTH ADDRESS^LONDON^^N2 9DU^^^^EAST FINCHLEY^||020811128383~07000111122~EMAI@MEDCHART.COM|02048817722|F1^^^I|M|1A|||||A|||||||2014110 1|Y
PD1|||NU^^^^^&&^^&&|375883^CURZON^RN^^^DR^^^&&^^^^^G8903132&&~P816881^43 DERBE ROAD^ST.ANNES-ON-SEA^LANCASHIRE^^^^FY8 1NJ^^01253 725811^^^^P81688&1&~410605^PATEL^A^^^^^^^^^^^D2639749&&~V263972^234 DENTAL CARE^234 EDGEWARE ROAD^LONDON^^^^W2  1DW^^^^^^V26397&2||9||||||
NK1|1|MEDCHART BROTHERNOK^NOK FIRST NAME^NOK SECONDNAME^^|BROTHER|65 ADDRESS ONE, ADDRESS&^TWO, NOK ADDRESS THREE,&^NOK ADDRESS FOUR,^LONDON,^N2 9DU^^^^MIDDLESEX^~65 ADDRESS ONE&ADDRESS TWO^NOK ADDRESS THREE&NOK ADDRESS FOUR^LONDON^^N2 9DU^^^^MIDDLESEX^|0809282822|0899282727|"""

patient_merge = """
MSH|^~\&|CARECAST|UCLH|ELCID||201212211522||ADT^A34|PLW21222286335931524|P|2.2|||AL|NE||
EVN|A34|201212211522||SEDEP|U440208^KHATRI^BHAVIN|
PID|||MV 19823^^^^UID~1287464666^^^^NHS||TESTSOA^SPACEINHOSPIDCHANGE^MIDNAMEADDED^^MR||19861112| M||C|11 DEBORAH CLOSE, SECOND^LINE, THRID LINE, FOURTH^LINE, ISLEWORTH,^MIDDLESEX^TW7 4NY||02081112121~07192932914~TESTSPACE@SOA.COM|011290930323|^^^A||1A|930569|||||||||||| MRG|50028000^^^UCLH|"""

inpatient_admission = """
MSH|^~\&|CARECAST|UCLH|CIDR||201511181757||ADT^A01|PLW21231462945754065|P|2.2|||AL|NEEVN|A01|20151118175 7||ADM|U440979^BOTTA^KIRAN|
PID|||50099878^^^^UID~9949657660^^^^NHS||TUCKER^ANN^ANN^^||1962030 40000|F|||12 MAIN STREET, HALIFAX^^^^NW3 3AA^^^^||||^^^|||940358||||||||||||
PD1|||NU|367113^BENDOR^AM^^^DR^^^^^^^^G9810354~F830031^THE PARK END SURGERY^3 PARK END^(OFF SOUTH HILL PARK)^LONDON^^^NW3 2SE^^020 74357282^^^^F83003&1||11||||||NK1||||||
PV1||I|BBNU^BCOT^BCOT- 02B|~I||^^|C2224532^CASSONI^A^M^^RABBI^AC3|367113^BENDOR^AM^^^DR||8008A||||19|||371928^CASSONI^ A^M^^RABBI||||||||||||||||||||||NU||2|||201511181756|
PV2||W|TEST NON ELECTIVE PATIENT||||||||||3OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW- HL7|||^^^^^|||||N|||20151118OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW- HL7||~~~~11~1|^^^^^|||||N|||OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW- HL7||2|D^^^^^|||||N|||ZUK|Q05|5K7|N||F83043^^|GOWER PLACE PRACTICE 1&3 GOWER PLACE^LONDON&^^^WC1E 6BN^^^^^|020 73876306|||N N^^||11||||^^^^^|^^|||||||||||F83003^2.16.840.1.113883.2.1.4.3|G9810354^2.16.840.1.113883.2.1.4.2|U440979^2.16.8 40.1.113883.2.1.3.2.4.11||8008A||||||||||^^|^^^^^^^^||||||||"""


MESSAGES = [i.replace("\n", "\r") for i in [patient_update, patient_death, patient_merge]]
HOST = "localhost"
PORT = 2575


def send_messages():
    start_time = time.time()
    with MLLPClient(HOST, PORT) as client:
        for i in xrange(400):
            for message in MESSAGES:
                ack = client.send_message(message)
                print ack

    print "end time %s" % (time.time() - start_time)


def read_message():
    return hl7.parse(MESSAGES[-1])

if __name__ == "__main__":
    send_messages()
