# 订单状态 已下单，已付款，已提车
# 等待到款, 等待审核, 等待提货，交易成功, 已取消
# 等待付预约款, 等待提货, 等待付款, 交易成功
APPOINTMENT_STATUS = {
    "0": "待付预约款",
    "1": "待提货",
    # "2": "待付款",
    "4": "交易成功",

    "-1": "取消",
    "-2": "已过期"
}

# 租车订单状态
RENT_APPOINTMENT_STATUS = {
    "0": "待付预约款",
    "1": "待提货",
    # "2": "待付款",
    "3": "待归还",
    "4": "交易成功",

    "-1": "取消",
    "-2": "已过期"
}

DEFAULT_DEPOSIT = 199.0


# 电动车类型 小龟、酷车，租车
E_BIKE_MODEL_CATEGORY = {
    "0": "小龟",
    "1": "酷车",
    "2": "租车",
}

DELIVERY = {
    "0": "自提",
    "1": "商家配送"
}

MAXIMUM_APPOINTMENT = 5

# 7 days
APPOINTMENT_EXPIRED_DAYS = 7

# 租期 years
RENT_TIME_PERIOD = {
    "学期": 0.5,
    "年": 1
}





