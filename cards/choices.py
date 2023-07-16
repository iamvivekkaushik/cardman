from django.utils.translation import gettext_lazy as _

VISA = "VISA"
RUPAY = "RUPY"
MASTER_CARD = "MSTR"

CARD_TYPE_CHOICES = (
    (VISA, _("Visa")),
    (RUPAY, _("RuPay")),
    (MASTER_CARD, _("Master Card")),
)