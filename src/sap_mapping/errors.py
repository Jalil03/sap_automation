class MappingContractError(ValueError):
    """The canonical object or interface registry violates the mapper contract."""


class BlockedObjectError(MappingContractError):
    """A BLOCKED canonical object was submitted outside structural-fixture mode."""


class UnsupportedObjectTypeError(MappingContractError):
    """No writable core mapper is authorized for the canonical object type."""


class PayloadValidationError(MappingContractError):
    """A payload violates its strict local Phase 2C schema."""
