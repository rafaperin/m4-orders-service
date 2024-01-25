from src.config.errors import DomainError


class OrderItemError(DomainError):
    @classmethod
    def modification_blocked(cls) -> "OrderItemError":
        return cls("Order already confirmed, modification not allowed!")
