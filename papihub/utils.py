import emoji


def trim_emoji(text):
    """
    去掉字符串中的emoji表情
    :param text:
    :return:
    """
    return emoji.demojize(text)
