def calculate_percentage(attended, total):

    if total == 0:
        return 0

    return (attended / total) * 100


def calculate_safe_bunks(attended, total, target):

    if total == 0:
        return 0

    bunks = int((attended / (target / 100)) - total)

    if bunks < 0:
        bunks = 0

    return bunks


def get_warning_status(percentage, target):

    if percentage < target:
        return "WARNING"

    return "SAFE"