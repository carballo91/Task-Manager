from main import format_date, validate_strings, menu_border
from datetime import date
    
def test_format_date():
    assert format_date("cat") == False
    assert format_date("September 21, 2024") == False
    assert format_date("09-21-2024") == False
    assert format_date("09/21/2024") == False
    assert format_date("2024-09-21") == date(2024,9,21)
    
def test_validate_strings():
    assert validate_strings("") == False
    assert validate_strings("    ") == False
    assert validate_strings("Finish CS50p Final Project") == True
    
def test_menu_border():
    assert menu_border(2,char=2) == "**"
    assert menu_border(2) == "**"
    assert menu_border(4,char="$") == "$$$$"
    