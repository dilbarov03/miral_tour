from datetime import datetime

from payze.client import Payze
from payze.param import PayzeOPS, request as payze_req

import os
import requests
import math

def convert_to_uzs(amount):
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://cbu.uz/oz/arkhiv-kursov-valyut/json/USD/{today}/"
    response = requests.get(url)
    data = response.json()
    rate = float(data[0]["Rate"])

    return float(math.floor(amount * rate))


def generate_pay_link(order):
    ops = PayzeOPS(
        url="https://payze.io",
        auth_token=os.getenv("PAYZE_AUTH_TOKEN"),
        hooks=payze_req.Hooks(
            web_hook_gateway=os.getenv("PAYZE_WEBHOOK_URL"),
            error_redirect_gateway=os.getenv("PAYZE_ERROR_URL"),
            success_redirect_gateway=os.getenv("PAYZE_SUCCESS_URL"),
        )
    )

    payze = Payze(ops=ops)

    if order.currency == "UZS":
        payment_amount = convert_to_uzs(order.total_price)
    else:
        payment_amount = float(order.total_price)

    metadata = payze_req.Metadata(
        order=payze_req.Order(order.id),
    )

    req_params = payze_req.JustPay(
        amount=payment_amount,
        metadata=metadata,
        currency=order.currency,
    )

    resp = payze.just_pay(
        req_params=req_params,
        reason="for_trip",
    )

    return {
        "pay_link": resp.data.payment.payment_url
    }
