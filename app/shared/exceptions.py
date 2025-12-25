
class DomainException(Exception):
    """Lỗi chung cho toàn bộ ứng dụng"""
    pass

class ValidationException(DomainException):
    """Lỗi khi dữ liệu đầu vào không hợp lệ"""
    pass

class DuplicatedEntityException(DomainException):
    """Lỗi khi dữ liệu đã tồn tại (ví dụ: trùng email)"""
    pass

class NotFoundException(DomainException):
    """Lỗi khi không tìm thấy dữ liệu"""
    pass
