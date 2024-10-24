from dateutil import parser

def format_date(date_string):
    """
    日付文字列をYYYY-MM-DD形式に変換する。
    変換できない場合はNoneを返す。
    """
    if not date_string:
        return None
    try:
        return parser.parse(date_string).strftime('%Y-%m-%d')
    except Exception as e:
        print(f"Date formatting error: {e}")
        return None