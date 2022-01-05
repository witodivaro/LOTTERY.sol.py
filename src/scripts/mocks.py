from brownie import MockV3Aggregator
from scripts.utils import get_account

DECIMALS = 8
INITIAL_ETH_PRICE = 10000 * 10 ** 8

def deploy_mocks():
    account = get_account(0)

    try:
        MockV3Aggregator[-1]
    except:
        MockV3Aggregator.deploy(DECIMALS, INITIAL_ETH_PRICE, {"from": account.address})
        
    