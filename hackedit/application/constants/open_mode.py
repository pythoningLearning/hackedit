class OpenMode:
    """
    Enumerates the possible open modes
    """
    #: Always open path in a new window (no multiple project support)
    NEW_WINDOW = 0
    #: Always open path in current window (add to open projects)
    CURRENT_WINDOW = 1
    #: Always ask what do (default).
    ASK_EACH_TIME = 2