def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return str(e) if str(
                e) else "Invalid input. Please check your arguments."
        except KeyError as e:
            return f"Contact {e} not found."

    return inner
