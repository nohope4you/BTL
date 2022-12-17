def cart_stats(cart):
    total_amount, total_quantity = 0,0

    if cart:
        for c in cart.values():
            total_quantity +=c['quantity']
            total_amount += c['price']
            if (c['quantity'] < 0 ):
                total_amount = 0
            if (c['quantity'] > 2 ):
                total_amount += (c['quantity']-2)* c['price'] * 0.25

    return {
        'total_amount': total_amount,
        'total_quantity':total_quantity
    }