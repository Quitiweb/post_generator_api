from .samples.sample_get_items_api import get_items


def get_product_description(asin):
    product_description = ""
    amazon_product = get_items([asin])

    for description_word in amazon_product[asin].item_info.features.display_values:
        product_description += description_word

    return product_description
