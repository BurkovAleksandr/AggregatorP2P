from .models import Listing


def save_parsed_order(order, source):
    # Уникальность по external_id + source
    listing, created = Listing.objects.update_or_create(
        external_id=order.external_id,
        source=source,
        defaults={
            "datetime": order.datetime,
            "bank": order.bank,
            "amount": order.amount,
            "recipient_details": order.recipient_details,
        },
    )
    return listing
