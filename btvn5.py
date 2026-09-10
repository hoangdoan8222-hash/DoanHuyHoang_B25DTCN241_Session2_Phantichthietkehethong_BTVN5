def process_rikkeimart_order(item_status, customer_response):
    """
    Mô phỏng xử lý đơn hàng RikkeiMart.

    item_status:
        - "available": sản phẩm còn hàng
        - "out_of_stock": sản phẩm hết hàng

    customer_response:
        - "accept": khách hàng đồng ý sản phẩm thay thế
        - "reject": khách hàng từ chối
        - "timeout": khách hàng không phản hồi trong 3 phút
        - "auto_substitute": hệ thống tự động chọn phương án thay thế an toàn
        - "auto_cancel": hệ thống tự động hủy phần hàng/đơn theo chính sách
        - giá trị khác: phản hồi không hợp lệ

    Hàm luôn trả về kết quả thay vì raise exception để mô phỏng
    có thể chạy an toàn, không bị crash.
    """
    try:
        status = str(item_status).strip().lower()
        response = str(customer_response).strip().lower()

        if status == "available":
            return {
                "status": "success",
                "message": "Sản phẩm còn hàng. Tài xế tiếp tục mua hàng.",
                "next_action": "continue_purchase"
            }

        if status != "out_of_stock":
            return {
                "status": "error",
                "message": "Trạng thái sản phẩm không hợp lệ.",
                "next_action": "stop_safely"
            }

        # Hết hàng: tài xế đề xuất sản phẩm tương đương.
        if response == "accept":
            return {
                "status": "success",
                "message": "Khách hàng đồng ý sản phẩm thay thế tương đương.",
                "next_action": "buy_substitute"
            }

        if response == "reject":
            return {
                "status": "handled",
                "message": "Khách hàng từ chối thay thế. Không mua sản phẩm này.",
                "next_action": "skip_item"
            }

        # Bẫy Timeout 3 phút:
        # Không cần sleep 180 giây trong mô phỏng; "timeout" đại diện cho
        # việc hệ thống đã xác định quá 3 phút mà không có phản hồi.
        if response == "timeout":
            return {
                "status": "timeout",
                "message": (
                    "Khách hàng không phản hồi trong 3 phút. "
                    "Kích hoạt chính sách an toàn để giải phóng tài xế."
                ),
                "next_action": "apply_timeout_policy"
            }

        if response == "auto_substitute":
            return {
                "status": "handled",
                "message": "Áp dụng sản phẩm thay thế tự động theo chính sách.",
                "next_action": "buy_substitute"
            }

        if response == "auto_cancel":
            return {
                "status": "handled",
                "message": "Tự động hủy phần hàng/đơn theo chính sách an toàn.",
                "next_action": "cancel_item_or_order"
            }

        return {
            "status": "error",
            "message": "Phản hồi khách hàng không hợp lệ.",
            "next_action": "stop_safely"
        }

    except (AttributeError, TypeError, ValueError) as exc:
        return {
            "status": "error",
            "message": f"Dữ liệu đầu vào không hợp lệ: {exc}",
            "next_action": "stop_safely"
        }


if __name__ == "__main__":
    test_cases = [
        ("available", "accept"),
        ("out_of_stock", "accept"),
        ("out_of_stock", "reject"),
        ("out_of_stock", "timeout"),
        ("out_of_stock", "auto_substitute"),
        ("out_of_stock", "auto_cancel"),
        ("unknown", "timeout"),
        (None, None),
    ]

    for item_status, customer_response in test_cases:
        result = process_rikkeimart_order(item_status, customer_response)
        print(
            f"item_status={item_status!r}, "
            f"customer_response={customer_response!r} -> {result}"
        )
