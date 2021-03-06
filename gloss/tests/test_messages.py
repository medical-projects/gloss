from hl7.client import MLLPClient
import hl7
from gloss.conf import settings
from gloss.utils import import_from_string


PATIENT_UPDATE = """
MSH|^~\&|CARECAST|UCLH|ELCID||201412061201||ADT^A31|PLW21228462730556545|P|2.2|||AL|NE
EVN|A31|201412061201||CREG|U440208^KHATRI^BHAVIN|
PID|||50092915^^^^UID~^^^^NHS||TESTING MEDCHART^MEDHCART FIRSTNAME^MEDCHART JONES^^MR||19870612|M|||12 THE DUNTINGDON ROAD,&^SECOND STREET, ADDRESS&^LINE 3, FORTH^ADDRESS, LONDON^N2 9DU^^^^EAST FINCHLEY^~12 THE DUNTINGDON ROAD&SECOND STREET^ADDRESS LINE 3&FORTH ADDRESS^LONDON^^N2 9DU^^^^EAST FINCHLEY^||020811128383~07000111122~EMAI@MEDCHART.COM|02048817722|F1^^^I|M|1A|||||A||||||||
PD1|||NU^^^^^&&^^&&|375883^CURZON^RN^^^DR^^^&&^^^^^G8903132&&~P816881^43 DERBE ROAD^ST.ANNES-ON-SEA^LANCASHIRE^^^^FY8 1NJ^^01253 725811^^^^P81688&1&~410605^PATEL^A^^^^^^^^^^^D2639749&&~V263972^234 DENTAL CARE^234 EDGEWARE ROAD^LONDON^^^^W2  1DW^^^^^^V26397&2||9||||||
NK1|1|MEDCHART BROTHERNOK^NOK FIRST NAME^NOK SECONDNAME^^|BROTHER|65 ADDRESS ONE, ADDRESS&^TWO, NOK ADDRESS THREE,&^NOK ADDRESS FOUR,^LONDON,^N2 9DU^^^^MIDDLESEX^~65 ADDRESS ONE&ADDRESS TWO^NOK ADDRESS THREE&NOK ADDRESS FOUR^LONDON^^N2 9DU^^^^MIDDLESEX^|0809282822|0899282727|"""

PATIENT_DEATH = """
MSH|^~\&|CARECAST|UCLH|ELCID||201412061201||ADT^A31|PLW21228462730556545|P|2.2|||AL|NE
EVN|A31|201412061201||CREGS|U440208^KHATRI^BHAVIN|
PID|||50092915^^^^UID~^^^^NHS||TESTING MEDCHART^MEDHCART FIRSTNAME^MEDCHART JONES^^MR||19870612|M|||12 THE DUNTINGDON ROAD,&^SECOND STREET, ADDRESS&^LINE 3, FORTH^ADDRESS, LONDON^N2 9DU^^^^EAST FINCHLEY^~12 THE DUNTINGDON ROAD&SECOND STREET^ADDRESS LINE 3&FORTH ADDRESS^LONDON^^N2 9DU^^^^EAST FINCHLEY^||020811128383~07000111122~EMAI@MEDCHART.COM|02048817722|F1^^^I|M|1A|||||A|||||||20141101|Y
PD1|||NU^^^^^&&^^&&|375883^CURZON^RN^^^DR^^^&&^^^^^G8903132&&~P816881^43 DERBE ROAD^ST.ANNES-ON-SEA^LANCASHIRE^^^^FY8 1NJ^^01253 725811^^^^P81688&1&~410605^PATEL^A^^^^^^^^^^^D2639749&&~V263972^234 DENTAL CARE^234 EDGEWARE ROAD^LONDON^^^^W2  1DW^^^^^^V26397&2||9||||||
NK1|1|MEDCHART BROTHERNOK^NOK FIRST NAME^NOK SECONDNAME^^|BROTHER|65 ADDRESS ONE, ADDRESS&^TWO, NOK ADDRESS THREE,&^NOK ADDRESS FOUR,^LONDON,^N2 9DU^^^^MIDDLESEX^~65 ADDRESS ONE&ADDRESS TWO^NOK ADDRESS THREE&NOK ADDRESS FOUR^LONDON^^N2 9DU^^^^MIDDLESEX^|0809282822|0899282727|"""

PATIENT_MERGE = """
MSH|^~\&|CARECAST|UCLH|ELCID||201212211522||ADT^A34|PLW21222286335931524|P|2.2|||AL|NE||
EVN|A34|201212211522||SEDEP|U440208^KHATRI^BHAVIN|
PID|||MV 19823^^^^UID~1287464666^^^^NHS||TESTSOA^SPACEINHOSPIDCHANGE^MIDNAMEADDED^^MR||19861112|M||C|11 DEBORAH CLOSE, SECOND^LINE, THRID LINE, FOURTH^LINE, ISLEWORTH,^MIDDLESEX^TW7 4NY||02081112121~07192932914~TESTSPACE@SOA.COM|011290930323|^^^A||1A|930569||||||||||||
MRG|50028000^^^UCLH|"""

INPATIENT_ADMISSION = """
MSH|^~\&|CARECAST|UCLH|CIDR||201511181757||ADT^A01|PLW21231462945754065|P|2.2|||AL|NE
EVN|A01|201511181757||ADM|U440979^BOTTA^KIRAN|
PID|||50099878^^^^UID~9949657660^^^^NHS||TUCKER^ANN^ANN^^||196203040000|F|||12 MAIN STREET, HALIFAX^^^^NW3 3AA^^^^||||^^^|||940358||||||||||||
PD1|||NU|367113^BENDOR^AM^^^DR^^^^^^^^G9810354~F830031^THE PARK END SURGERY^3 PARK END^(OFF SOUTH HILL PARK)^LONDON^^^NW3 2SE^^020 74357282^^^^F83003&1||11||||||NK1||||||
PV1||I|BBNU^BCOT^BCOT-02B|~I||^^|C2224532^CASSONI^A^M^^RABBI^AC3|367113^BENDOR^AM^^^DR||8008A||||19|||371928^CASSONI^ A^M^^RABBI||||||||||||||||||||||NU||2|||201511181756|
PV2||W|TEST NON ELECTIVE PATIENT||||||||||3
OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW- HL7|||^^^^^|||||N|||20151118
OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW- HL7||~~~~11~1|^^^^^|||||N|||
OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW- HL7||2|D^^^^^|||||N|||
ZUK|Q05|5K7|N||F83043^^|GOWER PLACE PRACTICE 1&3 GOWER PLACE^LONDON&^^^WC1E 6BN^^^^^|020 73876306|||N N^^||11||||^^^^^|^^|||||||||||F83003^2.16.840.1.113883.2.1.4.3|G9810354^2.16.840.1.113883.2.1.4.2|U440979^2.16.8 40.1.113883.2.1.3.2.4.11||8008A||||||||||^^|^^^^^^^^||||||||"""


ALLERGY = """
MSH|^~\&|ePMA|WS|ELCID|WS|201511190916043||ADT^A31|201511190916043||2.4||||AL
EVN|A31|201511190916043
PID|||97995111^^^PAS^MR||TESTPATIENT2^SABINE^MATHILDE^^MISS||19720221|F|||||||||||||||||||||||||||||Allergies Known and Recorded
AL1||1^Product Allergy^^CERT-1^Definite|CO-CODAMOL (Generic Manuf)^CO-CODAMOL (Generic Manuf) : ^UDM^8f75c6d8-45b7-4b40-913f-8ca1f59b5350|1^Active^^^201511190916||201511191200"""

MULTIPLE_ALLERGIES = r"""
MSH|^~\&|ePMA|WS|ELCID|WS|201603170313026||ADT^A31|201603170313026||2.4||||AL
EVN|A31|201603170313026
PID|||1234322333^^^PAS^MR||TEST1^TEST2||19521104|F|||||||||||||||||||||||||||||Allergies Known and Recorded
AL1||5^Non-Drug Allergy^^CERT-1^Definite|^Feathers : |1^Active^^^201603170142||201603171200
AL1||4^Class Allergy^^CERT-1^Definite|ANGIOTENSIN-II RECEPTOR ANTAGONISTS^ANGIOTENSIN-II RECEPTOR ANTAGONISTS : rash^UDM^7896c6a0-f69b-4a97-aa4a-13ca28812713|1^Active^^^201603170313||201603171200
"""

NO_ALLERGY = """
MSH|^~\&|ePMA|WS|ELCID|WS|201511190731003||ADT^A31|201511190731003||2.4||||AL
EVN|A31|201511190731003
PID|||97995000^^^PAS^MR||TESTPATIENT^PETER^^^MR||19610128|M|||||||||||||||||||||||||||||No Known Allergies"""

INPATIENT_DISCHARGE = """
MSH|^~\&|CARECAST|UCLH|CIDR||201511181617||ADT^A03|PLW21231462346320789|P|2.2|||AL|NE
EVN|A03|201511181617||DISCH|U440979^BOTTA^KIRAN|
PID|||50099886^^^^UID~6667309751^^^^NHS||TOMLINSON^ELIZABETH^ELI ZABETH^^||193508040000|F|||16 CHESTER ROAD, SANDY^LANE^^^NW3 3DE^^^^||||^^^|||940347||||||||||||
PD1|||NU|367113^BENDOR^AM^^^DR^^^^^^^^G9810354~F830031^THE PARK END SURGERY^3 PARK END^(OFF SOUTH HILL PARK)^LONDON^^^NW3 2SE^^020 74357282^^^^F83003&1||11||||||
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

INPATIENT_TRANSFER = """
MSH|^~\&|CARECAST|UCLH|ELCID||201212141354||ADT^A02|PLW21222225325867969|P|2.2|||AL|NE
EVN|A02|201212141354|201212141100|XFER|U440006^POWELL^DAVE|
PID|||50009026^^^^UID~^^^^NHS||POWELL^DEMONSTRATION^^^MR||196805120000|M|||3 STUDLAND ROAD, KINGSTON&^UPON THAMES, SURREY&^^^KT2 5HJ^^^^||||^^^|||930375||||||||||||
PD1||||417748^SACKVILLE-WEST^J^^^DR^^^^^^^^&~F830231^JAMES WIGG GROUP PRACTICE^KENTISH TOWN HEALTH CTR^2 BARTHOLOMEW ROAD^LONDON^^^NW5 2AJ^^0171 5304747^^^^&||N||||||NK1|
PV1||I|T06^T06A^T06-04|~I||T06^T06A|C3469817^HADDAD^FS^^^MR^|417748^SACKVILLE- WEST^J^^^DR~G9901629^MACSHARRY^MJ^^^DR||11016||||1|||^^^^^||||||||||||||||||||||NU||2|||201206281331
PV2|||VVVF||||||||||1OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW-HL7||||||||N|||20120628OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW-HL7||~~~~9~1||||||N|||OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW- HL7||7|D|||||N|||ZUK|Q05|5K7|N||M83049^^|HOLMCROFT SURGERY&HOLMCROFT ROAD^STAFFORD^^^ST16 1JG^^^^^|01785 242172|||N21T^^||1||||^^^^^|^^|||||||||||F83023^2.16.840.1.113883.2.1.4.3|G9504541^2.16.840.1.113883.2.1.4.2|U4400 06^2.16.840.1.113883.2.1.3.2.4.11||11016||||||||||RRV03^5K700^000P10|^^^^^^^^||||||||"""

INPATIENT_AMEND = r"""
MSH|^~\&|CARECAST|UCLH|ELCID||201212091535||ADT^A08|PLW21222182734338861|P|2.2|||AL|NE
EVN|A08|201212091535||CDIS|U439966^WYATT^CLARE|
PID|||50030204^^^^UID~^^^^NHS||CEW^LEA^^^^||198508200000|F|||UNKNOWN&^^^^^^^^||||^^^|||930882||||||||||||
PD1||||P439691^UNKNOWN^GP^^^^^^^^^^^G9999998&~G439692^PLEASE ASK PATIENT^FOR GP DETAILS,^UNLESS OVERSEAS PATIENT.^TEXT PRACTICE^^^^^^^^^V81999&2||N||||||
NK1|
PV1||I|T03^T03A^T03-14|~I|||C2224532^CASSONI^AM^^^DR^|P439691^UNKNOWN^GP^^^~G8713384^ELLIOTT^CA^^^DR||37082||||1|||^^^^^|||||||||||||||||||19|2||NU||2|||201209191822|201212081430
PV2|||ANY FOR TESTING||||||||||1
OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW-HL7||||||||N|||20120919OBX|2|ST|^^^LRRF^REG REQUIRED FLAGS^PLW-HL7||~~~~9~1||||||N|||OBX|3|ST|^^^DALOS^DISCHARGE AUTHORIZED LENGTH OF STAY^PLW-HL7||5|D|||||N|||
ZUK|||N||F83043^^|GOWER PLACE PRACTICE 1&3 GOWER PLACE^LONDON&^^^WC1E 6BN^^^^^|02073876306|||N N^^||1||||^^^^^|^^|||||||||||V81999^2.16.840.1.113883.2.1.4.3|G9999998^2.16.840.1.113883.2.1.4.2|U439966^2.16.840.1.113883.2. 1.3.2.4.11||37082||||||||||RRV20^TDH00^11HH10|^^^^^^^^||||||||
"""

INPATIENT_SPELL_DELETE = """
MSH|^~\&|CARECAST|UCLH|ELCID||201303141108||ADT^A07|PLW21223001929858442|P|2.2|||AL|NE
EVN|A07|201303141108||ADTDE|U442534^BRYAN^CHANTELLE|
PID|||40716752^^^^UID~4365248359^^^^NHS||WALKER^DARREN^^^MR ||198603020000|M|||47 KINGS DRIVE, EDGWARE,&^MIDDLESEX&^^^HA8 8ED^^^^||0208 9310096~NONE~NONE|NONE|^^^|U|7C|4449234||||||||||||N
PD1||||424104^SUMNERS^SM^^^DR^^^^^^^^~E830181^LONDON ROAD SURGERY^42 LONDON ROAD^STANMORE^MIDDLESEX^^^HA7 4NU^^0208 958 4237^0208 905 4809^^^||N||||||
NK1|1|.^EILEEN^|MOTHER|47 KINGS DRIVE, EDGWARE,&^MIDDLESEX&^^^HA8 8ED|0208 931 0096|07761 923 194
PV1||O|||||^FERSHT^N^L^^DR^|424104^SUMNERS^SM^^^DR~C2922926^GAVALAS^M^C^^MR||37067||||1|||||||||||||||||||||||| |NU||2|||201303140000|201303140000
PV2|||VOMITING UNWELL||||||||||3OBX|1|ST|^^^ABC^ASSIGN BENEFITS^PLW-HL7||||||||N|||20130314
OBX|2|ST|^^^CLCGF^CLIENT CHANGEABLE FLAGS^PLW-HL7||~1||||||N|||OBX|3|ST|^^^LRRF^REG REQUIRED FLAGS^PLW- HL7||~~~~9~1||||||N|||
ZUK|Q05|5A9|N||^^|^^^^^^^^||||N30^^|T|16||||^^^^^|^^|||||||||||E83018^2.16.840.1.113883.2.1.4.3|G3429778^ 2.16.840.1.113883.2.1.4.2|U442534^2.16.840.1.113883.2.1.3.2.4.11||4449234||||||||||RRV03^5A900^000P10|^^^^^^^^|||||||NO ASSESS + ESCORT. RI :25/1/13F 7/2/13DB,28/12FR03/01AO|"""

RESULTS_MESSAGE = r"""
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

URINE_CULTURE_RESULT_MESSAGE = r"""
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


CYTOPATHOLOGY_RESULTS_MESSAGE = r"""
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

COMPLEX_WINPATH_RESULT = r"""
MSH|^~\&|Corepoint|TDL|UCLH|UCLH|201411261546||ORU^R01|1126154698U000057|P|2.3
PID||^^NHS|50031772^^HOSP|C2130015640^^OASIS|TEST^TEST||19870912|M
PV1|||HAEM^HAEMATOLOGY OUTPATIENTS^^^^^^^OP||||||HC1^COHEN DR H
ORC|RE|98U000057|98U000057||CM||||201411261546
OBR|1|98U000057|98U000057|FBCY^FULL BLOOD COUNT^WinPath||201411121606|201411121600|||||||||HC1^COHEN DR H||||||201411121608||H1|F
OBX|1|NM|WCC^White cell count^Winpath||8.00|x10\S\9/L|3.0-10.0||||F
OBX|2|NM|RCC^Red cell count^Winpath||3.20|x10\S\12/L|4.4-5.8|L|||F
OBX|3|NM|HBGL^Haemoglobin (g/L)^Winpath||87|g/L|||||F
OBX|4|NM|HCTU^HCT^Winpath||0.350|L/L|0.37-0.50|L|||F
OBX|5|NM|MCVU^MCV^Winpath||78.0|fL|80-99|L|||F
OBX|6|NM|MCHU^MCH^Winpath||28.0|pg|27.0-33.5||||F
OBX|7|NM|MCGL^MCHC (g/L)^Winpath||300|g/L|||||F
OBX|8|NM|RDWU^RDW^Winpath||17.0|%|11.5-15.0|H|||F
OBX|9|NM|PLT^Platelet count^Winpath||250|x10\S\9/L|150-400||||F
OBX|10|NM|MPVU^MPV^Winpath||10.0|fL|7-13||||F
OBR|2|98U000057|98U000057|FBCZ^DIFFERENTIAL^WinPath||201411121606|201411121600|||||||||HC1^COHEN DR H||||||201411121609||H1|F
OBX|1|NM|NE^Neutrophils^Winpath||55.0%  4.40|x10\S\9/L|2.0-7.5||||F
OBX|2|NM|LY^Lymphocytes^Winpath||25.0%  2.00|x10\S\9/L|1.2-3.65||||F
OBX|3|NM|MO^Monocytes^Winpath||15.0%  1.20|x10\S\9/L|0.2-1.0|H|||F
OBX|4|NM|EO^Eosinophils^Winpath||3.0%  0.24|x10\S\9/L|0.0-0.4||||F
OBX|5|NM|BA^Basophils^Winpath||2.0%  0.16|x10\S\9/L|0.0-0.1|H|||F
"""

GYNAECOLOGY = r"""
MSH|^~\&|Corepoint|TDL|UCLH|UCLH|201307290934||ORU^R01|0729093413V344364|P|2.3
PID||^^NHS|C2088282317^^HOSP||DELA CRUZ^ANNABELLE||19830114|F||||||||||11185243
PV1|||MMF^MORTIMER MKT - FEMALE CLINIC^^^^^^^GUM||||||AJR^ROBINSON, DR. A. J.
ORC|RE|13V344364|13V344364||CM||||201307290934
OBR|1|13V344364|13V344364|GYNC^GYNAECOLOGY CULTURE^WinPath||201307261005|201307251858||||||||SWVU^Swab - Vulva|AJR^ROBINSON, DR. A. J.||||||201307290933||MC|F
OBX|1|FT|GYNC^GYNAECOLOGY CULTURE^Winpath||GYNAECOLOGY CULTURE REPORT||||||F
OBX|2|FT|GPRE^Culture^Winpath||No significant growth.||||||F
OBX|3|FT|GYST^STATUS^Winpath||COMPLETE: 29/07/13||||||F
OBR|2|13V344364|13V344364|GYNM^GYNAECOLOGY MICROSCOPY^WinPath||201307261005|201307251858||||||||SWVU^Swab - Vulva|AJR^ROBINSON, DR. A. J.||||||201307271141||MC|F
OBX|1|FT|GYNM^GYNAECOLOGY MICROSCOPY^Winpath||GYNAECOLOGY MICROSCOPY REPORT||||||F
OBX|2|FT|GETV^T. vaginalis microscopy^Winpath||No Trichomonas vaginalis seen.||||||F
"""

HEPD = r"""MSH|^~\&|Corepoint|TDL|UCLH|UCLH|201411261546||ORU^R01|1126154614U700101|P|2.3
PID||^^NHS|2470^^HOSP|C2130015640^^OASIS|TEST^BECKY||19530912|F||||||||||Y
PV1|||ARCH^ARCHWAY SEXUAL HEALTH CLINIC^^^^^^^GUM||||||DEM^MERCEY DR DE
ORC|RE|14U700101|14U700101||CM||||201411261546
OBR|1|14U700101|14U700101|HDV^HEPATITIS D (DELTA)^WinPath||201411181342|201411181200||||||TESTING DPL||CLB^Clotted blood|DEM^MERCEY DR DE||||||201411181346||V|F
OBX|1|FT|HDVT^Anti-HDV (Delta)^Winpath||Positive|||A|||F"""

FULL_BLOOD_COUNT = r"""MSH|^~\&|Corepoint|TDL|UCLH|UCLH|201411261546||ORU^R01|1126154698U000057|P|2.3
PID||^^NHS|50031772^^HOSP||TEST^TEST||19870912|M
PV1|||HAEM^HAEMATOLOGY OUTPATIENTS^^^^^^^OP||||||HC1^COHEN DR H
ORC|RE|98U000057|98U000057||CM||||201411261546
OBR|1|98U000057|98U000057|FBCY^FULL BLOOD COUNT^WinPath||201411121606|201411121600|||||||||HC1^COHEN DR H||||||201411121608||H1|F
OBX|1|NM|WCC^White cell count^Winpath||8.00|x10\S\9/L|3.0-10.0||||F
OBX|2|NM|RCC^Red cell count^Winpath||3.20|x10\S\12/L|4.4-5.8|L|||F
OBX|3|NM|HBGL^Haemoglobin (g/L)^Winpath||87|g/L|||||F
OBX|4|NM|HCTU^HCT^Winpath||0.350|L/L|0.37-0.50|L|||F
OBX|5|NM|MCVU^MCV^Winpath||78.0|fL|80-99|L|||F
OBX|6|NM|MCHU^MCH^Winpath||28.0|pg|27.0-33.5||||F
OBX|7|NM|MCGL^MCHC (g/L)^Winpath||300|g/L|||||F
OBX|8|NM|RDWU^RDW^Winpath||17.0|%|11.5-15.0|H|||F
OBX|9|NM|PLT^Platelet count^Winpath||250|x10\S\9/L|150-400||||F
OBX|10|NM|MPVU^MPV^Winpath||10.0|fL|7-13||||F
OBR|2|98U000057|98U000057|FBCZ^DIFFERENTIAL^WinPath||201411121606|201411121600|||||||||HC1^COHEN DR H||||||201411121609||H1|F
OBX|1|NM|NE^Neutrophils^Winpath||55.0%  4.40|x10\S\9/L|2.0-7.5||||F
OBX|2|NM|LY^Lymphocytes^Winpath||25.0%  2.00|x10\S\9/L|1.2-3.65||||F
OBX|3|NM|MO^Monocytes^Winpath||15.0%  1.20|x10\S\9/L|0.2-1.0|H|||F
OBX|4|NM|EO^Eosinophils^Winpath||3.0%  0.24|x10\S\9/L|0.0-0.4||||F
OBX|5|NM|BA^Basophils^Winpath||2.0%  0.16|x10\S\9/L|0.0-0.1|H|||F"""

ORDER_MESSAGE = r"""
MSH|^~\&|WINPATH|UCLH|ELCID|UCLH|201401180403||ORM^O01|0118040307R1234561|P|2.2|||AL|AL
PID||1234567890^^|12345678^^HOSP^2||SURNAME^FURNAME||19900809|F|||^^^^SQ1 1ED||||||||
PV1|||AE^A\T\E Secretariat, New UCLH^^^^^^^AE||AE||ST2||ST2^DR SJ TRIPPICK
ORC|NW||07R123456||IP||||201401180403|||ST2|||
OBR|1||07R123456|COAT^COAGULATION SCREEN -NEW^WinPath||201401180013|201401172340|||||||201401180013||ST2^DR SJ TRIPPICK||||07R123456||201401180051||HH|I
"""

PATIENT_QUERY_RESPONSE = r"""
MSH|^~\&|CDR|ACPT|ELCID|LIVE|20160404103009||ADR^A19|201604041030090469|A|2.4|||NE|NE
MSA|AA|ELC42803992124131432|Call Successful|||00000
QAK||OK
QRD|201604041030|R|I||||1^RD|50013000^^^^^^^UCLH^^^^MR|DEM|||
PID|||50013000^^^UCLH^MR^UCLH~3841252907^^^NHS^NH||TESTSURNAME^TESTFIRSTNAME^^^MR||19800215|M|||20 TESTY GARDENS^^^^EN7 6AR^^^^||020 7898 6940|020 7880 8333X5965||S|Protestant|||||B||||||||0
PD1|||^^F83043|G8513694
ROL||UP|PP^Patient Primary Care Provider^HL70443|G8513694^ALIBHAI^AA^^^DR^^OCS^^^^GMC|||||GP^Registered GP^HL70182||GOWER PLACE PRACTICE 1^3 GOWER PLACE^LONDON^^^^B|
NK1|1|TESTWIFE WINPATH^^^^|WIFE^|20 TESTY GARDENS^^^^|020 7898 6940||
PV1|
""".replace("\n", "\r")

PATIENT_NOT_FOUND = r"""
MSH|^~\&|CDR|ACPT|ELCID|LIVE|20160404110401||ADR^A19|201604041104010063|A|2.4|||NE|NE
MSA|AA|ELC33894012248516544|Patient Master details not found|||01100
QAK||NF
QRD|201604041104|R|I||||1^RD|5001asdf^^^^^^^UCLH^^^^MR|DEM|||
PID|||^^^UCLH^MR^~^^^NHS^NH||^^^^||||||^^^^^^^^|||||||||||||||||||
PD1|||^^|
ROL|||^^|^^^^^^^^^^^|||||^^||^^^^^^|
NK1|1|^^^^|^|^^^^||
PV1|
""".replace("\n", "\r")

MESSAGE_TYPES = dict(
    # Demographics updates
    patient_update=PATIENT_UPDATE,
    patient_death=PATIENT_DEATH,
    patient_merge=PATIENT_MERGE,
    patient_amend=INPATIENT_AMEND,
    # Admission, Discharge and Transfer
    inpatient_admission=INPATIENT_ADMISSION,
    inpatient_discharge=INPATIENT_DISCHARGE,
    inpatient_cancel_discharge=INPATIENT_CANCEL_DISCHARGE,
    inpatient_transfer=INPATIENT_TRANSFER,
    # Allergies
    allergy=ALLERGY,
    multiple_allergies=MULTIPLE_ALLERGIES,
    no_allergy=NO_ALLERGY,
    # Results
    renal_profile=RESULTS_MESSAGE,
    urine_culture=URINE_CULTURE_RESULT_MESSAGE,
    cytopathology=CYTOPATHOLOGY_RESULTS_MESSAGE,
    fbc_and_fbcz_differential=COMPLEX_WINPATH_RESULT,
    gynaecology=GYNAECOLOGY,
    hepd=HEPD
)

MESSAGE_TYPES = {
    k: v.replace("\n", "\r") for k, v in MESSAGE_TYPES.iteritems()
}

MESSAGES = MESSAGE_TYPES.values()


def send_messages(messages):
    gloss_service = import_from_string(settings.GLOSS_SERVICE)
    port = gloss_service.receiver.ports[0]
    host = gloss_service.receiver.host
    with MLLPClient(host, port) as client:
        for message in messages:
            client.send_message(message)


def read_message(some_msg):
    return hl7.parse(some_msg.replace("\n", "\r"))
