from djchoices import DjangoChoices, ChoiceItem


class PaymentCategoryChoices(DjangoChoices):
    UPI = ChoiceItem('UPI')
    CC = ChoiceItem('CREDIT CARD')
    DC = ChoiceItem('DEBIT CARD')
    Paypal = ChoiceItem('paypal')
    NB = ChoiceItem('Net Banking')
    OTHERS = ChoiceItem('Others')


class PaymentGatewayChoices(DjangoChoices):
    CASHFREE = ChoiceItem('cashfree')
    RAZORPAY = ChoiceItem('razorpay')


class PaymentStatusChoices(DjangoChoices):
    INITIATED = ChoiceItem('Initiated')
    FAILED = ChoiceItem('Failed')
    SUCCESS = ChoiceItem('Success')
    CANCELLED = ChoiceItem('Cancelled')
    REFUND_INITIATED = ChoiceItem('Refund_Initiated')
    REFUNDED = ChoiceItem('Refunded')


class PaymentCurrencyChoices(DjangoChoices):
    INR = ChoiceItem('INR')
