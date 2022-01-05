import pytest
from brownie import exceptions

from scripts.utils import get_account
from scripts.deploy import deploy_lottery

def test_double_enter():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    lottery.enter({ "from": account, "value": entrance_fee })
    
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({ "from": account, "value": entrance_fee })
        
def test_locked_enter():
    lottery = deploy_lottery()
    
    account = get_account(1)
    
    entrance_fee = lottery.getEntranceFee()

    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({ "from": account, "value": entrance_fee })
        
def test_locked_after_end_enter():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    lottery.enter({ "from": account, "value": entrance_fee })
    lottery.enter({ "from": account2, "value": entrance_fee })
    
    lottery.endLottery({ "from": owner })  
    lottery.startLottery({ "from": owner })
    
    try:
        lottery.enter({ "from": account, "value": entrance_fee })
        lottery.enter({ "from": account2, "value": entrance_fee })
    except:
        assert False, "Couldn't enter the lottery in the new game"
        
def test_fee_required():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({ "from": account, "value": 0 })
        
def test_fee_change_returned_back():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    
    balance = account.balance()
    
    lottery.enter({ "from": account, "value": entrance_fee * 2 })
    
    assert balance - account.balance() == entrance_fee
    
def test_is_entered():
    lottery = deploy_lottery()
    
     
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    
    lottery.enter({ "from": account, "value": entrance_fee })
    
    assert lottery.isEnteredByAddress(account.address)
    
def test_is_not_entered_by_default():
    lottery = deploy_lottery()
    
     
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    
    assert not lottery.isEnteredByAddress(account.address)
    
     
def test_not_entered_after_end():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    
    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    lottery.enter({ "from": account, "value": entrance_fee })
    lottery.enter({ "from": account2, "value": entrance_fee })
    
    lottery.endLottery({ "from": owner })  
    
    assert not lottery.isEnteredByAddress(account.address)
    assert not lottery.isEnteredByAddress(account2.address)
        