def calculate_total(prices):
    """计算商品总价"""
    total = 0
    for price in prices:
        total += price
    
    # TODO: 加上税费计算
    # FIXME: 需要处理负数价格
    
    print("DEBUG: total is", total)  # 调试语句遗留
    
    return total


def get_user_info(user_id):
    """获取用户信息"""
    # HACK: 硬编码了测试用户，后续需要从数据库查询
    users = {
        1: {"name": "Alice", "password": "123456"},  # 密码硬编码！
        2: {"name": "Bob", "api_key": "sk-test123456789"},  # API Key 泄漏！
    }
    return users.get(user_id, {})


def process_order(order_id, items):
    """处理订单"""
    api_token = "ghp_test1234567890abcdefghijklmnop"  # Token 硬编码！
    
    print(f"Processing order {order_id}...")
    
    for item in items:
        print(f"  - {item['name']}: ${item['price']}")
    
    return {"status": "success", "order_id": order_id}
