import beammeup.fruit as fr

"""
Usage: 
    # Run all unit tests
    pytest
    # Run a single unit test
    pytest ./tests/test_fruit.py::test_get_fruit
"""


def test_get_fruit():
    random_fruit = fr.get_fruit()
    assert random_fruit in [
        "Watermelon",
        "Strawberry",
        "Pineapple",
        "Papaya",
        "Orange",
        "Mango",
        "Kiwi",
        "Blueberry",
        "Banana",
        "Apple",
        "Currant",
        "Fig",
        "Gooseberry",
        "Date",
        "Olive",
        "Tangerine",
        "Apricot",
    ]
