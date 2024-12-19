from orders.models import Order


def request_email(serial_nomer):
    orders = Order.objects.filter(robot_serial=serial_nomer)
    return [order.customer.email for order in orders]