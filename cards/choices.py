from django.utils.translation import gettext_lazy as _

VISA = "VISA"
RUPAY = "RUPY"
MASTER_CARD = "MSTR"
DREAMFOLKS = "DMFK"
PRIORITY_PASS = "PRPS"
METRO_CARD = "MTRO"

CARD_TYPE_CHOICES = (
    (VISA, _("Visa")),
    (RUPAY, _("RuPay")),
    (MASTER_CARD, _("Master Card")),
    (DREAMFOLKS, _("DreamFolks")),
    (PRIORITY_PASS, _("Priority Pass")),
    (METRO_CARD, _("Metro Card")),
)

CREDIT_CARD = "CC"
DEBIT_CARD = "DC"
PREPAID_CARD = "PP"
VIRTUAL_CARD = "VC"

CARD_ACCOUNT_CHOICES = (
    (CREDIT_CARD, _("Credit Card")),
    (DEBIT_CARD, _("Debit Card")),
    (PREPAID_CARD, _("Prepaid Card")),
    (VIRTUAL_CARD, _("Virtual Card")),
)