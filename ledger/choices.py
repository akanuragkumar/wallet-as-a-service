from djchoices import DjangoChoices, ChoiceItem


class TransactionTypesChoices(DjangoChoices):
    CREDIT = ChoiceItem('credit')
    DEBIT = ChoiceItem('debit')
