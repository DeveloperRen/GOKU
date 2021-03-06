"""

@author: Bingwei Chen

@time: 8/17/17

@desc: 退款表格

"""
from datetime import datetime
from server.database.model import RefundTable


def get_all(username=None):
    refund_table = RefundTable.select()
    if username:
        refund_table = refund_table.where(
            RefundTable.user == username
        )
    refund_table = refund_table.order_by(RefundTable.date.desc())
    return refund_table


def modify_status(refund_table_id, status):
    refund_table = RefundTable.get(id=refund_table_id)
    refund_table.status = status
    return refund_table.save()


def add(**kwargs):
    date = datetime.utcnow()
    return RefundTable.create(
        date=date,
        **kwargs)
