from twisted.logger import Logger
import settings
from txHL7.receiver import AbstractHL7Receiver
from twisted.internet import defer


from import_message import MessageProcessor


class OhcReceiver(AbstractHL7Receiver):
    log = Logger(namespace="receiver")

    def handleMessage(self, container):
        message = container.message
        self.log.info(str(message).replace("\r", "\n"))
        if settings.PROCESS_MESSAGES:
            message_processor = MessageProcessor()
            message_processor.process_message(message)

        # We succeeded, so ACK back (default is AA)
        return self.ack(container)

    def getCodec(self):
        # Our messages are encoded in Windows-1252
        # WARNING this is an example and is not universally true! You will
        # need to figure out the encoding you are receiving.
        return 'cp1252'

    def ack(self, container):
        ack_message = unicode(container.message.create_ack(
            application="ELCID", facility="UCLH"
        ))
        self.log.info(ack_message.replace("\r", "\n"))
        return defer.succeed(ack_message)
