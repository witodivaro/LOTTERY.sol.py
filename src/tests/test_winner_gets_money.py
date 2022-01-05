import pytest
from brownie import exceptions

from scripts.utils import get_account
from scripts.deploy import deploy_lottery
     
def test_participant_got_correct_eth():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    account3 = get_account(3)

    initial_account_balances = [x.balance() for x in [account, account2, account3]]

    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    owners_fee_percentage = lottery.ownersFeePercentage()
    owners_fee_decimals = lottery.ownersFeeDecimals()
    owners_fee = owners_fee_percentage / 10 ** (2 + owners_fee_decimals)
    
    lottery.enter({ "from": account, "value": entrance_fee })
    lottery.enter({ "from": account2, "value": entrance_fee })
    lottery.enter({ "from": account3, "value": entrance_fee })
    
    total_paid = entrance_fee * 3
    expected_win = total_paid - entrance_fee - total_paid * owners_fee
    
    
    lottery.endLottery({ "from": owner })
    
    final_account_balances = [x.balance() for x in [account, account2, account3]]
    
    assert True in [final_account_balances[i] - initial_account_balances[i] == expected_win for i in range(0, len(final_account_balances))]
    
    
    
def test_owners_gets_fee():
    lottery = deploy_lottery()
    
    owner = get_account(0)
    account = get_account(1)
    account2 = get_account(2)
    account3 = get_account(3)
    
    balance = owner.balance()

    lottery.startLottery({ "from": owner })
    
    entrance_fee = lottery.getEntranceFee()
    owners_fee_percentage = lottery.ownersFeePercentage()
    owners_fee_decimals = lottery.ownersFeeDecimals()
    owners_fee = owners_fee_percentage / 10 ** (2 + owners_fee_decimals)
    
    lottery.enter({ "from": account, "value": entrance_fee })
    lottery.enter({ "from": account2, "value": entrance_fee })
    lottery.enter({ "from": account3, "value": entrance_fee })
    
    total_paid = entrance_fee * 3
    
    lottery.endLottery({ "from": owner })
    
    assert owner.balance() - balance == total_paid * owners_fee