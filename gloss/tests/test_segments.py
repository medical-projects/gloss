from gloss.message_segments import *
from unittest import TestCase
from gloss.tests.test_messages import (
    FULL_BLOOD_COUNT, read_message, CYTOPATHOLOGY_RESULTS_MESSAGE,
    ALLERGY, PATIENT_QUERY_RESPONSE, PATIENT_NOT_FOUND
)
from gloss.translators.hl7.hl7_translator import HL7Translator
from gloss.translators.hl7.segments import (
    MSH, ResultsPID, ResultsPV1, ORC, OBR, OBX, NTE, RepeatingField,
    AllergiesPID, PV2, MSA
)
from gloss.exceptions import TranslatorError


class WinPathResults(HL7Translator):
    message_type = u"ORU"
    trigger_event = u"R01"

    segments = (
        MSH, ResultsPID, ResultsPV1, ORC, RepeatingField(
            OBR,
            RepeatingField(OBX, section_name="obxs"),
            RepeatingField(NTE, section_name="ntes"),
            section_name="results"
            )
    )


class TestSegments(TestCase):
    def test_multi_levelled_message(self):
        hl7_msg = read_message(FULL_BLOOD_COUNT)
        msg = WinPathResults(hl7_msg)
        self.assertEqual(len(msg.results), 2)


class TestWithWrongMessage(TestCase):
    def test_with_wrong_message(self):
        class SomeMsg(HL7Translator):
            segments = (MSH, PV2,)

        with self.assertRaises(TranslatorError):
            SomeMsg(read_message(FULL_BLOOD_COUNT))


class TestResultsPID(TestCase):
    def test_with_no_date_of_birth(self):
        class SomeMsg(HL7Translator):
            segments = (MSH, ResultsPID,)

        no_dob = CYTOPATHOLOGY_RESULTS_MESSAGE.replace("19881107", "")
        result = SomeMsg(read_message(no_dob))
        self.assertIsNone(result.pid.date_of_birth)


class TestAllergiesPID(TestCase):
    def test_with_no_date_of_birth(self):
        class SomeMsg(HL7Translator):
            segments = (MSH, AllergiesPID,)

        no_dob = ALLERGY.replace("19720221", "")
        result = SomeMsg(read_message(no_dob))
        self.assertIsNone(result.pid.date_of_birth)


class TestMSH(TestCase):
    def test_deduce_error_code(self):
        class SomeMsg(HL7Translator):
            segments = (MSH, MSA,)

        msg = SomeMsg(read_message(PATIENT_QUERY_RESPONSE))

        self.assertIsNone(msg.msa.error_code)

        msg = SomeMsg(read_message(PATIENT_NOT_FOUND))

        self.assertEqual(
            msg.msa.error_code, "Patient Master details not found"
        )
