# -*- coding: UTF-8 -*-
"""
@author: larry.shuoren@outlook.com
@time: 8/10/17
@desc: virtual card route
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from peewee import DoesNotExist
from server.service import virtual_card_service

from playhouse.shortcuts import model_to_dict
from server.utility.json_utility import models_to_json, custom_models_to_json
from server.utility.exception import *


PREFIX = '/virtual_card'

virtual_card_app = Blueprint("virtual_card", __name__, url_prefix=PREFIX)


# ***************************** 虚拟卡 ***************************** #
# 获取虚拟卡
@virtual_card_app.route('', methods=['GET'])
def get_virtual_card():
    username = request.args.get("username")
    try:
        virtual_card = virtual_card_service.get_virtual_card(
            card_no=username
        )
        virtual_card = model_to_dict(virtual_card, recurse=False)
        return jsonify({'response': virtual_card}), 200

    except DoesNotExist as e:
        return jsonify({
            'response': {
                'error': e.args,
                'message': '未开通虚拟消费卡'
            }
        }), 400


# ***************************** 押金 ***************************** #
# # 获取押金数额
# @virtual_card_app.route('/deposit', methods=['GET'])
# def get_deposit():
#     """
#     check if the card deposited
#     :param card_no: card number
#     :return: True of False
#     """
#     username = request.args.get("username")
#     try:
#         deposit = virtual_card_service.get_deposit(
#             card_no=username
#         )
#         return jsonify({'response': deposit}), 200
#
#     except DoesNotExist as e:
#         return jsonify({
#             'response': {
#                 'error': e.args,
#                 'message': '未开通虚拟消费卡'
#             }
#         })


# 支付押金
@virtual_card_app.route('/deposit', methods=['POST'])
def pay_deposit():
    """
    pay deposit

    eg = {
    "card_no": "bingwei",
    "deposit_fee": 199
    }
    :return:
    """
    data = request.get_json()
    try:
        result, record = virtual_card_service.pay_deposit(
            card_no=data["card_no"],
            deposit_fee=data["deposit_fee"],
        )
        return jsonify({'response': {
            "result": result,
            "record": model_to_dict(record, recurse=False)
        }}), 200
    except Error as e:
        return jsonify({
            'response': {
                'error': e.args,
                'message': '%s' % e.args
            }
        })


# 退还押金
@virtual_card_app.route('/deposit/return_deposit', methods=['POST'])
def return_deposit():
    """
    eg = {
    "username": "bingwei",
    "card_no": "bingwei",
    "account": "BingweiChen",
    "account_type": "wechat",
    "comment": "test",
    }

    return deposit
    :return:
    """
    data = request.get_json()
    try:
        result, record, refund_record =\
            virtual_card_service.return_deposit(
                username=data.pop("username"),
                card_no=data.pop("card_no"),
                account=data.pop("account"),
                account_type=data.pop("account_type"),
                comment=data.pop("comment"),
                **data
            )
        return jsonify({
            'response': {
                "result": result,
                "record": model_to_dict(record, recurse=False),
                "refund_record": model_to_dict(refund_record, recurse=False)
            }}), 200
    except Error as e:
        return jsonify({
            'response': {
                'error': e.args,
                'message': '%s' % e.args
            }
        })


# ***************************** 余额 ***************************** #
# # 获取余额
# @virtual_card_app.route('/balance', methods=['GET'])
# def get_card_balance():
#     """
#     get card balance
#
#     :return: balance
#     """
#     username = request.args.get("username")
#     try:
#         balance = virtual_card_service.get_card_balance(
#             card_no=username
#         )
#         return jsonify({
#             'response': {
#                 'balance': balance,
#             }
#         })
#     except DoesNotExist as e:
#         return jsonify({
#             'response': {
#                 'error': e.args,
#                 'message': '未开通虚拟消费卡'
#             }
#         })


# # 消费余额
# @virtual_card.route('/balance/consume', methods=['POST'])
# def consume_virtual_card():
#     """
#     consume virtual card
#
#     eg = {
#     "username": "bingwei",
#     "amount": 120
#     }
#     :return:
#     """
#     data = request.get_json()
#     result, record = virtual_card_service.consume_virtual_card(
#         card_no=data["username"],
#         amount=data["amount"],
#     )
#     return jsonify({'response': {
#         "result": result,
#         "record": model_to_dict(record)
#     }}), 200


# 充值
@virtual_card_app.route('/balance/top_up', methods=['POST'])
def top_up():
    """
    top up virtual card

    eg = {
    "username": "bingwei",
    "top_up_fee": 120
    }
    :return:
    """
    data = request.get_json()
    result, record = virtual_card_service.top_up(
        card_no=data["username"],
        top_up_fee=data["top_up_fee"],
    )
    return jsonify({'response': {
        "result": result,
        "record": model_to_dict(record, max_depth=1)
    }}), 200


# ***************************** 消费记录 ***************************** #
# 获取消费记录
@virtual_card_app.route('/consume_record', methods=['GET'])
def get_consume_record():
    """
    get consume records
    :param card_no: card number
    :return: consume records
    """
    username = request.args.get("username")
    record = virtual_card_service.get_consume_record(
        card_no=username
    )
    new_records = custom_models_to_json(record, [
        "consume_date_time",
        "consume_event",
        "consume_fee",
        "id"
    ])
    if record:
        return jsonify({'response': new_records}), 200
    else:
        return jsonify({'response': 'No record found'}), 404
