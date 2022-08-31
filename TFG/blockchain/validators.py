from django.core.exceptions import ValidationError


def validar_gt_0(value):
    if value < 0:
        raise ValidationError(
                "Debe tener un valor válido (mayor o igual que 0)"
            )


def validar_lt_10(value):
    if value > 10:
        raise ValidationError(
                "Debe tener un valor válido (menor o igual que 10)"
            )
