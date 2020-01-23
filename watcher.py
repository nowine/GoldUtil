# coding: utf-8
from typing import List

import goldbot
import notifier


def watch():
    bgb = goldbot.BankGoldBot()
    data: List[goldbot.BaseGoldObject] = bgb.get_data()
    default_email = notifier.EmailNotifer()
    msg = []
    for item in data:
        #print(item.html())
        msg.append(item.html())

    msg_text = ''.join(msg)
    #print(msg_text)
    default_email.send_mail('黄金报价监控', msg_text)


if __name__ == '__main__':
    watch()
