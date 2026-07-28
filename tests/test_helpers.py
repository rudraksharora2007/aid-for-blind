from src.utils.helpers import clean_text, position_for_box


def test_text_cleaning_and_position():
    assert clean_text("  EXIT   ->  90% ") == "EXIT 90%"
    assert position_for_box((0, 0, 20, 20), 300) == "left"
    assert position_for_box((140, 0, 160, 20), 300) == "center"
    assert position_for_box((280, 0, 300, 20), 300) == "right"
