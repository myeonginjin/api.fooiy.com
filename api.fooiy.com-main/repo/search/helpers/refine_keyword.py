from re import sub, compile

convert_keywords = {
    " 맛집": "",
    " 핫플": "",
    " 먹거리": "",
    " ": "",
}


def refine_keyword(keyword):
    for convert_keyword, refine_keyword in convert_keywords.items():
        keyword = keyword.replace(convert_keyword, refine_keyword)
    keyword = sub("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`'…》]", "", keyword)
    keyword = compile("[|ㄱ-ㅎ|ㅏ-ㅣ]+").sub("", keyword)
    return keyword
