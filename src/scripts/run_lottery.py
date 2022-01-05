from brownie import Lottery
from scripts.utils import get_account

def run_lottery():
    lottery = Lottery[-1]

    admin = get_account(0)
    participant1 = get_account(1)
    participant2 = get_account(2)
    participant3 = get_account(3)
    participant4 = get_account(4)
    
    entrance_fee = lottery.getEntranceFee()
    
    lottery.startLottery({ "from": admin })
    
    lottery.enter({"from": participant1, "value": entrance_fee})
    lottery.enter({"from": participant2, "value": entrance_fee})
    lottery.enter({"from": participant3, "value": entrance_fee})
    lottery.enter({"from": participant4, "value": entrance_fee})
    
    lottery.endLottery({ "from": admin })
    
    winner = lottery.lastWinner()
    
    print('The winner is:', winner)

    


def main():
    run_lottery()