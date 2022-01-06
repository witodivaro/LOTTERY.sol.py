from brownie import Lottery
from scripts.utils import get_account, is_dev, is_fork
from scripts.deploy import deploy_lottery


def run_lottery():
    lottery = Lottery[-1]

    admin = get_account(0)
    participant1 = get_account(1)
    participant2 = get_account(2)
    participant3 = get_account(3)
    participant4 = get_account(4)
    
    participants = [participant1, participant2, participant3, participant4]
    

    is_locked = lottery.isLocked()

    if is_locked:    
        start_txn = lottery.startLottery(3536, { "from": admin })
        start_txn.wait(1)
    
    enter_txns = []

    entrance_fee = lottery.getEntranceFee()
    print(entrance_fee)
    
    
    for participant in participants:
        is_entered = lottery.isEnteredByAddress(participant.address)

        if not is_entered:
            enter_txn = lottery.enter({"from": participant, "value": entrance_fee, 'required_confs': 0 })
            enter_txns.append(enter_txn)    

    if (len(enter_txns) > 0):
        enter_txns[-1].wait(1)
        
    lottery.endLottery({"from": admin })

    winner_address = lottery.lastWinner()

    print("The winner is:", winner_address)
    
    winner = list(filter(lambda x: x.address == winner_address, participants))[0]
    
    lottery.withdraw({ "from": winner })


def main():
    if (is_dev() or is_fork()):
        deploy_lottery()
    run_lottery()
