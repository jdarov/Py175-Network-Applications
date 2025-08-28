MIN_TITLE_LEN = 1
MAX_TITLE_LEN = 100

def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
        return "The title must be unique"
    
    if not MIN_TITLE_LEN <= len(title) <= MAX_TITLE_LEN:
        return "The title must be between 1 and 100 characters"
    
    return None