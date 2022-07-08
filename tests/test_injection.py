from nisa_di.inject import mock_dependency, get_dependency

class Abaca:
    msg: str = ''


class MockAbaca:
    msg: str = 'test'
    
def test_mockingan():
    
    mock_dependency(Abaca, MockAbaca())

    cc = get_dependency(Abaca)
    assert cc.msg == 'test'