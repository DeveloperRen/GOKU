"""
@author: Bingwei Chen

@time: 8/4/17

@desc: 管理员

个人中心查询、

闪充使用情况（在使用闪充显示使用编号、没有使用闪充就显示未使用闪充）、
共享电动车的访问记录（记录访问时间)

? 个人中心全部都查看个人内容吗
？ 先暂时给所有人的表格吧
"""
from flask import Blueprint
from flask import jsonify
from flask import request

from peewee import DoesNotExist

from playhouse.shortcuts import model_to_dict
from flask_jwt_extended import jwt_required

from server.service import auth_decorator
from server.utility.json_utility import models_to_json
from server.service import user_service
from server.service import appointment_service
from server.service import refund_table_service
from server.service import report_table_service
from server.service import virtual_card_service
from server.service import battery_record_service
from server.service import battery_rent_service

from server.utility.exception import Error

PREFIX = '/manager/user_setting'

user_setting = Blueprint("user_setting", __name__, url_prefix=PREFIX)


# ***************************** 查看用户 ***************************** #
# 获取所有用户
@user_setting.route('/users/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_user():
    users = user_service.get_all()
    users = models_to_json(users, recurse=False)
    for i in range(len(users)):
        users[i].pop("password")
    return jsonify({
        'response': {
            "users": users
        }}), 200


# 更改用户密码
@user_setting.route('/user/change_password', methods=['POST'])
@jwt_required
@auth_decorator.check_admin_auth
def change_password():
    """

    eg = {
    "username": "",
    "password": ""
    }
    :return:
    :rtype:
    """
    data = request.get_json()
    result = user_service.change_password(
        username=data.pop("username"),
        password=data.pop("password")
    )
    return jsonify({
        'response': {
            "result": result
        }}), 200


# 获取所有虚拟消费卡
@user_setting.route('/virtual_cards/all', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_virtual_cards():
    virtual_cards = virtual_card_service.get_all()
    virtual_cards = models_to_json(virtual_cards, recurse=False)
    # for i in range(len(virtual_cards)):
    #     users[i].pop("password")
    return jsonify({
        'response': {
            "virtual_cards": virtual_cards
        }}), 200


# ***************************** 虚拟消费卡 ***************************** #
@user_setting.route('/virtual_card', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
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


# 冻结账号
@user_setting.route('/virtual_card/freeze', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def freeze():
    card_no = request.args.get("card_no")
    result = virtual_card_service.freeze(
        card_no=card_no,
        consume_event="后台手动冻结"
    )
    return jsonify({'response': result}), 200


# 解冻账号
@user_setting.route('/virtual_card/re_freeze', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def re_freeze():
    card_no = request.args.get("card_no")
    result = virtual_card_service.re_freeze(
        card_no=card_no
    )
    return jsonify({'response': result}), 200


# 虚拟消费卡实名认证
@user_setting.route('/virtual_card/real_name_authentication', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def real_name_authentication():
    card_no = request.args.get("card_no")
    result = virtual_card_service.real_name_authentication(
        card_no=card_no
    )
    return jsonify({'response': result}), 200


# ***************************** 个人订单 ***************************** #
# 获取用户的订单情况
@user_setting.route('/user/appointment', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_user_appointment():
    username = request.args.get("username")
    appointments = appointment_service.get_all(username=username)
    appointments = models_to_json(appointments, recurse=False)
    return jsonify({
        'response': {
            "appointments": appointments
        }}), 200


# ***************************** 个人消费记录 ***************************** #
@user_setting.route('/consume_record', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
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
    if record:
        return jsonify({'response': models_to_json(record, recurse=False)}), 200
    else:
        return jsonify({'response': 'No record found'}), 404


# ***************************** 个人退款 ***************************** #
@user_setting.route('/refund_table', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_refund_table():
    username = request.args.get("username")
    refund_tables = refund_table_service.get_all(username)
    return jsonify({
        'response': {
            "refund_tables": models_to_json(refund_tables, recurse=False)
        }}), 200


# ***************************** 个人电动车报修 ***************************** #
@user_setting.route('/report_table', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_report_table():
    username = request.args.get("username")
    report_tables = report_table_service.get_all(
        user=username
    )
    report_tables = models_to_json(report_tables, recurse=False)
    return jsonify({'response': report_tables}), 200


# ***************************** 个人闪充记录 ***************************** #
@user_setting.route('/battery_record', methods=['GET'])
def get_battery_record():
    username = request.args.get("username")
    battery_record = battery_record_service.get_all(
        username=username
    )
    battery_record = models_to_json(battery_record)
    return jsonify({'response': battery_record}), 200


# ***************************** 个人现在使用的闪充 ***************************** #
@user_setting.route('/on_load_battery', methods=['GET'])
@jwt_required
@auth_decorator.check_admin_auth
def get_on_load_battery():
    username = request.args.get("username")
    try:
        battery = battery_rent_service.get_on_load_battery(
            username=username
        )
        battery = model_to_dict(battery)
        return jsonify({'response': battery}), 200
    except Error as e:
        return jsonify({'response': {
            "message": "没有正在使用的电池",
            "error": e.args,
        }}), 400
