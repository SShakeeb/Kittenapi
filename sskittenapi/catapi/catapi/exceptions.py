class CatapiError(Exception):
    pass


class EventException(CatapiError):
    pass


class DuplicateEntityError(CatapiError):
    pass


class DuplicateCatError(DuplicateEntityError):
    pass


class EmptyResultsFilter(CatapiError):
    pass


class EntityNotFoundError(CatapiError):
    pass


class CatNotFoundError(EntityNotFoundError):
    pass
