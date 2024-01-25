from src.config.errors import DomainError


class OrderError(DomainError):
    @classmethod
    def invalid_category(cls) -> "OrderError":
        return cls("Provided order is not valid!")
