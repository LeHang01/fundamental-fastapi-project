from sqlalchemy.orm import Session
from app.model import Order

class PaymentRepo:
    @staticmethod
    def update_payment_status(db: Session, order_id: int, payment_status: str):
        try:
            # Lấy đơn hàng từ cơ sở dữ liệu
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                # Kiểm tra xem trạng thái thanh toán hợp lệ
                if payment_status in ["unpaid", "paid", "pending"]:
                    # Cập nhật trạng thái thanh toán
                    order.payment_status = payment_status
                    db.commit()
                    return order
                else:
                    raise ValueError("Invalid payment status")
            else:
                raise ValueError("Order not found")
        except Exception as e:
            db.rollback()
            raise e
