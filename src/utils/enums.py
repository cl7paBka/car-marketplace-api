import enum


class Role(enum.Enum):
    """Defines roles for users in the system."""
    customer = 'customer'
    manager = 'manager'
    admin = 'admin'


class EngineType(enum.Enum):
    """Types of engines for cars."""
    gasoline = 'gasoline'
    electric = 'electric'
    diesel = 'diesel'


class TransmissionType(enum.Enum):
    """Transmission types available for cars."""
    manual = 'manual'
    automatic = 'automatic'


class OrderStatus(enum.Enum):
    """Statuses for orders."""
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'
