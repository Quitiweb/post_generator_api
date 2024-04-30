from .samples.sample_get_items_api import get_items


def get_product_title_and_description(asin):
    product_title = ""
    product_description = ""
    amazon_product = get_items([asin])

    if amazon_product is None:
        raise Exception("Amazon PAAPI is not working. Please, check it from affiliates website.")

    item_info = amazon_product[asin].item_info
    for title_word in item_info.title.display_value:
        product_title += title_word

    for description_word in item_info.features.display_values:
        product_description += description_word

    return product_title, product_description
