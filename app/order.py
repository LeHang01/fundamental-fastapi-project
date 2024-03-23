from sqlalchemy.orm import Session
from app.model import Order, Product
from datetime import datetime

def create_order(db: Session, user_id: int, product_id: int, quantity: int):
    try:
        # Lấy thông tin sản phẩm từ cơ sở dữ liệu
        product = db.query(Product).filter(Product.id == product_id).first()

        # Kiểm tra xem số lượng hàng tồn kho có đủ không
        if product.stock_quantity < quantity:
            raise ValueError("Not enough stock available")

        # Tính tổng giá của đơn hàng
        total_price = product.price * quantity

        # Tạo đối tượng Order
        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            order_date=datetime.now()
        )

        # Giảm số lượng tồn kho của sản phẩm
        product.stock_quantity -= quantity

        # Lưu thay đổi vào cơ sở dữ liệu
        db.add(order)
        db.commit()

        return order
    except Exception as e:
        # Xử lý ngoại lệ nếu có
        db.rollback()
        raise
