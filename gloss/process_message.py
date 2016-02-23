from datetime import datetime
import logging

from models import session_scope, is_known, is_subscribed

DATETIME_FORMAT = "%Y%m%d%H%M"



def get_fields(msg):
    ''' figures out what type of message it is based on the fields
    '''
    return [i[0][0] for i in msg]



class Segment(object):
    pass


class MSH(Segment):
    def __init__(self, segment):
        self.trigger_event = segment[9][0][1][0]
        self.message_type = segment[9][0][0][0]
        self.message_datetime = datetime.strptime(segment[7][0], DATETIME_FORMAT)


class EVN(Segment):
    pass


class NK1(Segment):
    pass


class PID(Segment):
    def __init__(self, segment):
        self.nhs_number = segment[2][0]
        if isinstance(self.nhs_number, list):
            self.nhs_number = self.nhs_number[0][0]

        self.hospital_number = segment[3][0][0][0]
        self.surname = segment[5][0][0][0]
        self.forename = segment[5][0][1][0]
        self.date_of_birth = segment[7][0]
        self.gender = segment[8][0]


class OBR(Segment):
    STATUSES = {
        'F': 'FINAL',
        'I': 'INTERIM',
        'A': 'SOME RESULTS AVAILABLE'
    }
    def __init__(self, segment):
        self.lab_number = segment[3][0]
        self.profile_code = segment[4][0][0][0]
        self.profile_description = segment[4][0][1][0]
        self.request_datetime = segment[6][0]
        self.observation_datetime = segment[7][0]
        self.last_edited = segment[22][0]
        self.result_status = OBR.STATUSES[segment[25][0]]


class OBX(Segment):
    STATUSES = {
        'F': 'FINAL',
        'I': 'INTERIM'
    }
    def __init__(self, segment):
        self.test_code = segment[3][0][0][0]
        self.test_name = segment[3][0][1][0]
        self.observation_value = segment[5][0]
        self.units = segment[6][0]
        self.reference_range = segment[7][0]
        self.result_status = OBX.STATUSES[segment[11][0]]


class NTE(Segment):
    def __init__(self, segments):
        self.comments = "\n".join(
            s[3][0] for s in segments
        )


class MessageType(object):

    def __init__(self, msg):
        self.raw_msg = msg

    def process(self):
        with session_scope() as session:
            self.process_message(session)

    @property
    def pid(self):
        return PID(self.raw_msg.segment("PID"))

    @property
    def msh(self):
        return MSH(self.raw_msg.segment("MSH"))


class InpatientAdmit(MessageType):
    message_type = u"ADT"
    trigger_event = u"A01"


    def process_message(self, session):
        # shouldn't this be is known?
        if is_subscribed():
            pass


class WinPathResults(MessageType):
    message_type = u"ORU"
    trigger_event = u"R01"

    @property
    def obr(self):
        return OBR(self.raw_msg.segment('OBR'))

    @property
    def obx(self):
        return [OBX(s) for s in self.raw_msg.segments('OBX')]

    @property
    def nte(self):
        return NTE(self.raw_msg.segments("NTE"))

    def process_message(self, session):
        logging.debug('Processing WinPath Results Message')
        pass



class MessageProcessor(object):
    def get_msh_for_message(self, msg):
        """
        We need this because we don't know the correct messageType subclass to
        instantiate yet.
        """
        return MSH(msg.segment("MSH"))

    def get_message_type(self, msg):
        msh = self.get_msh_for_message(msg)

        for message_type in MessageType.__subclasses__():
            if msh.message_type == message_type.message_type:
                if msh.trigger_event == message_type.trigger_event:
                    return message_type


    def process_message(self, msg):
        message_type = self.get_message_type(msg)
        if not message_type:
            raise ValueError("unable to find message type for {}".format(message_type))
        message_type(msg).process()
