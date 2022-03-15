from unittest import TestCase

from domain.helpers.validate_document_helper import validate_cpf


class TestValidateDocumentHelper(TestCase):
    def test_validate_cpf_ok(self):
        result = validate_cpf(cpf="161.146.282-76")
        self.assertTrue(result)

    def test_validate_cpf_no_punctuation(self):
        result = validate_cpf(cpf="16114628276")
        self.assertFalse(result)

    def test_validate_cpf_repeated_numbers(self):
        result = validate_cpf(cpf="111.111.111-11")
        self.assertFalse(result)

    def test_validate_cpf_invalid(self):
        result = validate_cpf(cpf="161.146.282-77")
        self.assertFalse(result)
