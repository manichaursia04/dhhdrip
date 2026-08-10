from .models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session

        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, size, quantity=1):
        """Add a product/size combination to the cart."""
        cart_key = f"{product.id}_{size}"

        if cart_key not in self.cart:
            self.cart[cart_key] = {
                "product_id": product.id,
                "quantity": 0,
                "size": size,
            }

        self.cart[cart_key]["quantity"] += quantity
        self.save()

    def remove(self, cart_key):

        if cart_key in self.cart:

            del self.cart[cart_key]

        self.save()

    def decrease(self, cart_key):

        if cart_key not in self.cart:
            return

        self.cart[cart_key]["quantity"] -= 1

        if self.cart[cart_key]["quantity"] <= 0:
            del self.cart[cart_key]

        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):

        product_ids = [item["product_id"] for item in self.cart.values()]
        products = Product.objects.in_bulk(product_ids)

        # Copy each item before adding product/price data.  The session itself
        # must contain only simple values, not Django model objects.
        for cart_key, stored_item in self.cart.items():
            product = products.get(stored_item["product_id"])

            if product is None:
                continue

            item = stored_item.copy()
            item["cart_key"] = cart_key
            item["product"] = product
            item["price"] = product.discount_price or product.price
            item["total"] = item["price"] * item["quantity"]

            yield item

    def get_total_price(self):

        total = 0

        for item in self:
            total += item["total"]

        return total

    def get_total_quantity(self):

        total = 0

        for item in self.cart.values():
            total += item["quantity"]

        return total

    def clear(self):

        self.session["cart"] = {}
        self.save()
