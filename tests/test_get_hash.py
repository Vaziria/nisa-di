from main import get_hash

def test_hashing_any_data():
    
    assert get_hash(12)
    assert get_hash([1,2,3])
    # assert get_hash("asdasdasd")
    # assert get_hash({
    #     "name": "asdasdasd"
    # })
    
    # assert get_hash({
    #     "asdasd": {
    #         "asdasd": "asdasd",
    #         "asd": 123
    #     }
    # })
    

    # assert get_hash([1,2,3,4])
