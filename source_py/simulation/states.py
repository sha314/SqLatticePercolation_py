import enum

class SelectionState(enum.Enum):
   SUCESS = 0
   CURRENT_SITE_NOT_EMPTY = 1
   EMPTY_SITE_LIST = -1
   pass
