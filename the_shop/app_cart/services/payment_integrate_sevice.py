from app_cart.models import Order


def job(card, order_id):
    print(order_id)
    order = Order.objects.filter(id=order_id).first()
    if card % 10 != 0:
        order.status = 'Оплачен'
        order.error = ''
        order.save()
        return f'Заказ номер {order.id} оплачен.'
    else:
        print(order.id)
        order.status = 'Ошибка'
        order.error = 'Случилась странная фигня'
        order.save()
        return 'Оплата не прошла'
