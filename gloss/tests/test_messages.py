from hl7.client import MLLPClient
import hl7
import time


PATIENT_UPDATE = """
MSH|^~\&|CARECAST|UCLH|ELCID||201412061201||ADT^A31|PLW21228462730556545|P|2.2|||AL|NE
EVN|A31|201412061201||CREG|U440208^KHATRI^BHAVIN|
PID|||50092915^^^^UID~^^^^NHS||TESTING MEDCHART^MEDHCART FIRSTNAME^MEDCHART JONES^^MR||19870612|M|||12 THE DUNTINGDON ROAD,&^SECOND STREET, ADDRESS&^LINE 3, FORTH^ADDRESS, LONDON^N2 9DU^^^^EAST FINCHLEY^~12 THE DUNTINGDON ROAD&SECOND STREET^ADDRESS LINE 3&FORTH ADDRESS^LONDON^^N2 9DU^^^^EAST FINCHLEY^||020811128383~07000111122~EMAI@MEDCHART.COM|02048817722|F1^^^I|M|1A|||||A||||||||
PD1|||NU^^^^^&&^^&&|375883^CURZON^RN^^^DR^^^&&^^^^^G8903132&&~P816881^43 DERBE ROAD^ST.ANNES-ON-SEA^LANCASHIRE^^^^FY8 1NJ^^01253 725811^^^^P81688&1&~410605^PATEL^A^^^^^^^^^^^D2639749&&~V263972^234 DENTAL CARE^234 EDGEWARE ROAD^LONDON^^^^W2  1DW^^^^^^V26397&2||9||||||
NK1|1|MEDCHART BROTHERNOK^NOK FIRST NAME^NOK SECONDNAME^^|BROTHER|65 ADDRESS ONE, ADDRESS&^TWO, NOK ADDRESS THREE,&^NOK ADDRESS FOUR,^LONDON,^N2 9DU^^^^MIDDLESEX^~65 ADDRESS ONE&ADDRESS TWO^NOK ADDRESS THREE&NOK ADDRESS FOUR^LONDON^^N2 9DU^^^^MIDDLESEX^|0809282822|0899282727|"""

PATIENT_DEATH = """
MSH|^~\&|CARECAST|UCLH|ELCID||201412061201||ADT^A31|PLW21228462730556545|P|2.2|||AL|NE
EVN|A31|201412061201||CREGS|U440208^KHATRI^BHAVIN|
PID|||50092915^^^^UID~^^^^NHS||TESTING MEDCHART^MEDHCART FIRSTNAME^MEDCHART JONES^^MR||19870612|M|||12 THE DUNTINGDON ROAD,&^SECOND STREET, ADDRESS&^LINE 3, FORTH^ADDRESS, LONDON^N2 9DU^^^^EAST FINCHLEY^~12 THE DUNTINGDON ROAD&SECOND STREET^ADDRESS LINE 3&FORTH ADDRESS^LONDON^^N2 9DU^^^^EAST FINCHLEY^||020811128383~07000111122~EMAI@MEDCHART.COM|02048817722|F1^^^I|M|1A|||||A|||||||2014110 1|Y
PD1|||NU^^^^^&&^^&&|375883^CURZON^RN^^^DR^^^&&^^^^^G8903132&&~P816881^43 DERBE ROAD^ST.ANNES-ON-SEA^LANCASHIRE^^^^FY8 1NJ^^01253 725811^^^^P81688&1&~410605^PATEL^A^^^^^^^^^^^D2639749&&~V263972^234 DENTAL CARE^234 EDGEWARE ROAD^LONDON^^^^W2  1DW^^^^^^V26397&2||9||||||
NK1|1|MEDCHART BROTHERNOK^NOK FIRST NAME^NOK SECONDNAME^^|BROTHER|65 ADDRESS ONE, ADDRESS&^TWO, NOK ADDRESS THREE,&^NOK ADDRESS FOUR,^LONDON,^N2 9DU^^^^MIDDLESEX^~65 ADDRESS ONE&ADDRESS TWO^NOK ADDRESS THREE&NOK ADDRESS FOUR^LONDON^^N2 9DU^^^^MIDDLESEX^|0809282822|0899282727|"""

PATIENT_MERGE = """
MSH|^~\&|CARECAST|UCLH|ELCID||201212211522||ADT^A34|PLW21222286335931524|P|2.2|||AL|NE||
EVN|A34|201212211522||SEDEP|U440208^KHATRI^BHAVIN|
PID|||MV 19823^^^^UID~1287464666^^^^NHS||TESTSOA^SPACEINHOSPIDCHANGE^MIDNAMEADDED^^MR||19861112| M||C|11 DEBORAH CLOSE, SECOND^LINE, THRID LINE, FOURTH^LINE, ISLEWORTH,^MIDDLESEX^TW7 4NY||02081112121~07192932914~TESTSPACE@SOA.COM|011290930323|^^^A||1A|930569|||||||||||| MRG|50028000^^^UCLH|"""

INPATIENT_ADMISSION = """
MSH|^~\&|CARECAST|UCLH|CIDR||201511181757||ADT^A01|PLW21231462945754065|P|2.2|||AL|NE
EVN|A01|201511181757||ADM|U440979^BOTTA^KIRAN|
PID|||50099878^^^^UID~9949657660^^^^NHS||TUCKER^ANN^ANN^^||196203040000|F|||12 MAIN STREET, HALIFAX^^^^NW3 3AA^^^^||||^^^|||940358||||||||||||
PD1|||NU|367113^BENDOR^AM^^^DR^^^^^^^^G9810354~F830031^THE PARK END SURGERY^3 PARK END^(OFF SOUTH HILL PARK)^LONDON^^^NW3 2SE^^020 74357282^^^^F83003&1||11||||||NK1||||||
PV1||I|BBNU^BCOT^BCOT- 02B|~I||^^|C2224532^CASSONI^A^M^^RABBI^AC3|367113^BENDOR^AM^^^DR||8008A||||19|||371928^CASSONI^ A^M^^RABBI||||||||||||||||||||||NU||2|||201511181756|
PV2||W|TEST NON ELECTIVE PATIENT||||||||||3
OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW- HL7|||^^^^^|||||N|||20151118
OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW- HL7||~~~~11~1|^^^^^|||||N|||
OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW- HL7||2|D^^^^^|||||N|||
ZUK|Q05|5K7|N||F83043^^|GOWER PLACE PRACTICE 1&3 GOWER PLACE^LONDON&^^^WC1E 6BN^^^^^|020 73876306|||N N^^||11||||^^^^^|^^|||||||||||F83003^2.16.840.1.113883.2.1.4.3|G9810354^2.16.840.1.113883.2.1.4.2|U440979^2.16.8 40.1.113883.2.1.3.2.4.11||8008A||||||||||^^|^^^^^^^^||||||||"""


ALLERGY = """
MSH|^~\&|ePMA|WS|ELCID|WS|201511190916043||ADT^A31|201511190916043||2.4||||AL
EVN|A31|201511190916043
PID|||97995111^^^PAS^MR||TESTPATIENT2^SABINE^MATHILDE^^MISS||19720221|F|||||||||||||||||||||||||||||Allergies Known and Recorded
AL1||1^Product Allergy^^CERT-1^Definite|CO-CODAMOL (Generic Manuf)^CO-CODAMOL (Generic Manuf) : ^UDM^8f75c6d8-45b7-4b40-913f-8ca1f59b5350|1^Active^^^201511190916||201511191200
MSH|^~\&|ePMA|WS|ELCID|WS|201511190731003||ADT^A31|201511190731003||2.4||||AL
EVN|A31|201511190731003
PID|||97995000^^^PAS^MR||TESTPATIENT^PETER^^^MR||19610128|M|||||||||||||||||||||||||||||No Known Allergies
"""

INPATIENT_DISCHARGE = """
MSH|^~\&|CARECAST|UCLH|CIDR||201511181617||ADT^A03|PLW21231462346320789|P|2.2|||AL|NE
EVN|A03|201511181617||DISCH|U440979^BOTTA^KIRAN|
PID|||50099886^^^^UID~6667309751^^^^NHS||TOMLINSON^ELIZABETH^ELI ZABETH^^||193508040000|F|||16 CHESTER ROAD, SANDY^LANE^^^NW3 3DE^^^^||||^^^|||940347||||||||||||PD1|||NU|367113^BENDOR^AM^^^DR^^^^^^^^G9810354~F830031^THE PARK END SURGERY^3 PARK END^(OFF SOUTH HILL PARK)^LONDON^^^NW3 2SE^^020 74357282^^^^F83003&1||11||||||
NK1||||||
PV1||I|F3NU^F3SR^F3SR-36|1~I||^^|C2224532^CASSONI^A^M^^RABBI^AC3|367113^BENDOR^AM^^^DR||8008A||||19|||C2224532^CASSONI^A^M^^RABBI|||||||||||||||||||19|1||NU||2|||201511181217|201511181615
PV2||W|ELECTIVE ADMISSION||||||||||3
OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW-HL7|||^^^^^|||||N|||20151118OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW- HL7||~~~~11~1|^^^^^|||||N|||OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW- HL7||2|D^^^^^|||||N|||
ZUK|Q05|5K7|N||^^|^^^^^^^^||||N U^^||11||||^^^^^|^^|||||||||||F83003^2.16.840.1.113883.2.1.4.3|G9810354^2.16.840.1.113883.2.1.4.2|U440979^2.16.8 40.1.113883.2.1.3.2.4.11||8008A||||||||||RRV03^5K700^000P10|^^^^^^^^||||||||"""

INPATIENT_CANCEL_DISCHARGE = """
MSH|^~\&|CARECAST|UCLH|CIDR||201511181626||ADT^A13|PLW21231462400600527|P|2.2|||AL|NE
EVN|A13|201511181626||CDIS|U440979^BOTTA^KIRAN|
PID|||50099886^^^^UID~6667309751^^^^NHS||TOMLINSON^ELIZABETH^ELIZABETH^^||193508040000|F|||16 CHESTER ROAD, SANDY^LANE^^^NW3 3DE^^^^||||^^^|||940347||||||||||||
PD1|||NU|367113^BENDOR^AM^^^DR^^^^^^^^G9810354~F830031^THE PARK END SURGERY^3 PARK END^(OFF SOUTH HILL PARK)^LONDON^^^NW3 2SE^^020 74357282^^^^F83003&1||11||||||
NK1||||||
PV1||I|F3NU^F3SR^F3SR-36|1~I||^^|C2224532^CASSONI^A^M^^RABBI^AC3|367113^BENDOR^AM^^^DR||8008A||||19|||371928^CASSONI^ A^M^^RABBI||||||||||||||||||||1||NU||2|||201511181217|
PV2||W|ELECTIVE ADMISSION||||||||||3
OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW- HL7|||^^^^^|||||N|||20151118OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW- HL7||~~~~11~1|^^^^^|||||N|||OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW- HL7||2|D^^^^^|||||N|||
ZUK|Q05|5K7|N||^^|^^^^^^^^||||N U^^||11||||^^^^^|^^|||||||||||F83003^2.16.840.1.113883.2.1.4.3|G9810354^2.16.840.1.113883.2.1.4.2|U440979^2.16.8 40.1.113883.2.1.3.2.4.11||8008A||||||||||RRV03^5K700^000P10|^^^^^^^^||||||||"""


RESULTS_MESSAGE = """
MSH|^~\&|WINPATH|UCLH|ELCID|UCLH|201401172357||ORU^R01|0117235810U1119701|P|2.2|||AL|AL
PID||1234567890^^|12345678^^HOSP^2||ISURNAME^FIRSTNAME MNAME||19820515|F|||
PV1|||OPDP1^OPD 1st Floor Podium UCH^^^^^^^OP||||||DAI^ISENBERG PROF DA
ORC|RE|10U111970|10U111970||CM||||201401172357|||GP39BRU||||
OBR|1|10U111970|10U111970|ELU^RENAL PROFILE^WinPath||201401172045|201401171700|||||||201401172045||DAI^ISENBERG PROF DA||||10U111970||201401172258||CC|F
OBX|1|NM|NA^Sodium^Winpath||143|mmol/L|135-145||||F|||201401172358
OBX|2|NM|K^Potassium^Winpath||3.9|mmol/L|3.5-5.1||||F|||201401172358
OBX|3|NM|UREA^Urea^Winpath||3.9|mmol/L|1.7-8.3||||F|||201401172358
OBX|4|NM|CREA^Creatinine^Winpath||61|umol/L|49-92||||F|||201401172358
OBX|5|NM|GFR^Estimated GFR^Winpath||>90|.|||||F|||201401172358
NTE|1||Units: mL/min/1.73sqm
NTE|1||Multiply eGFR by 1.21 for people of African
NTE|1||Caribbean origin. Interpret with regard to
NTE|1||UK CKD guidelines: www.renal.org/CKDguide/ckd.html
NTE|1||Use with caution for adjusting drug dosages -
NTE|1||contact clinical pharmacist for advice.
"""

URINE_CULTURE_RESULT_MESSAGE = """
MSH|^~\&|OADD|WINPATHTDLDIR|DADD|XXXXXX|201205211101||ORU^R01|0821110112V7778331|P|2.1|
PID||^^|C2088885408^^HOSP^2||GRECE^POPEDULE||19880608|M||||||||||11239933|
PV1|||MMB^MORTIMER MKT - BLOOMSBURY^^^||GUM||IGW||IGW^WILLIAMS DR IG
ORC|RE||12V777833||CM||||201205211101|||IGW||||
OBR|1||12V777833|URNC^URINE CULTURE^WinPath||201205201715|201205201413|||||||201205201715|URIN^Urine|IGW^WILLIAMS DR IG||||12V777833||201205211100||MC|F|||||
OBX|1|FT|URNC^URINE CULTURE^Winpath||URINE CULTURE REPORT||||||F|||201205211101||^^
OBX|2|FT|UPRE^Culture^Winpath||Screening culture negative.||||||F|||201205211101||^^
OBX|3|FT|URST^STATUS^Winpath||COMPLETE: 21/08/13||||||F|||201205211101||^^"""

RESULTS_CANCELLATION_MESSAGE = """
MSH|^~\&|WINPATH|UCLH|ELCID|UCLH|201401180344||ORU^R01|0118034408J1234561|P|2.2|||AL|AL
PID||0918111222|12345678^^HOSP^2||PATEL^MIKE JOHNE||19891211|M|||^^^^UU8 9SJ|||
PV1|||HASU^HYPER ACUTE STROKE UNIT (T07)^^^^^^^IP||IP||NL||NL^LOSSEFF DR N
ORC|RE||08J123456||CM||||201401180344|||NL||||
OBR|1||08J123456|FBCY^FULL BLOOD COUNT^WinPath||201401172327|201401171055|||||||201401172327||NL^LOSSEFF DR N||||08J123456||201401180331||H1|F
OBX|1|FT|WCC^White cell count^Winpath||Cancelled - FBC Request entered in error|x10\S\9/L|||||F|||201401180344
OBX|2|FT|RCC^Red cell count^Winpath||Request entered in error|x10\S\12/L|||||F|||201401180344
OBX|3|FT|HGB^Haemoglobin^Winpath||Request entered in error|g/dl|||||F|||201401180344
OBX|4|FT|HCTU^HCT^Winpath||Request entered in error|L/L|||||F|||201401180344
OBX|5|FT|MCVU^MCV^Winpath||Request entered in error|fL|||||F|||201401180344
OBX|6|FT|MCHU^MCH^Winpath||Request entered in error|pg|||||F|||201401180344
OBX|7|FT|CHCU^MCHC^Winpath||Request entered in error|g/dl|||||F|||201401180344
OBX|8|FT|RDWU^RDW^Winpath||Request entered in error|%|||||F|||201401180344
OBX|9|FT|PLT^Platelet count^Winpath||Request entered in error|x10\S\9/L|||||F|||201401180344
OBX|10|FT|MPVU^MPV^Winpath||Request entered in error|fL|||||F|||201401180344"""


CYTOPATHOLOGY_RESULTS_MESSAGE = """
MSH|^~\&|OADD||DADD||20120920142301||ORU^R01|20120350348973|P|2.1||||
PID|||C1130045684^^^2||BOYLE^SUSECCA^||19881107|F|^^|||||||||||
PV1||CFP|BPHC^||||O10070^Neilson^Nurse^M.|^||||||||||CFP||||||||||||||||||||||||||201308160000||
ORC|RE|UG13-33365|UG13-33365|||||||||O10070^Neilson^Nurse^M.|LAB|||^|||
OBR||UG13-33365|UG13-33365|C^Cytopathology|||201209141719|||||||201309151719|^CervicalSample|O10070^Neilson^Nurse^M.||||UG13-33365||||AP|F||^^^^^R|^~^~^||||||||
OBX|1|ST|CPRpt^|1|(NOTE)||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|2|LAST SMEAR||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|3|2010 - normal||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|4|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|5|DATE OF LAST MENSTRUAL PERIOD:||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|6|5/12 ago - pre menop||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|7|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|8|CLINICAL DATA:||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|9|Cx visualised with difficulty however ox appears to be closed . Minimal contact||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|10|bleeding .||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|11|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|12|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|13|CERVICAL SAMPLE REPORT||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|14|Diagnosis: Cytology negative Recommendation: Normal recall.||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|15|Action Code 2A||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|16|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|17|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|18|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|19|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|20|ELECTRONICALLY SIGNED OUT BY:||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|21|Pippa Horsey||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|22|||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|23|REPORTED:||||||F|||201209201423||^^
OBX|1|ST|CPRpt^|24|20/08/2013||||||F|||201209201423||^^"""

MESSAGES = [i.replace("\n", "\r") for i in [
    PATIENT_UPDATE, PATIENT_DEATH, PATIENT_MERGE,
    INPATIENT_ADMISSION, RESULTS_MESSAGE
]]
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


def read_message(some_msg):
    return hl7.parse(some_msg.replace("\n", "\r"))

def test_message_read():
    pass



if __name__ == "__main__":
    send_messages()
