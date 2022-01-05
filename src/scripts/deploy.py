from brownie import Lottery, MockV3Aggregator, config
from scripts.utils import get_account, is_dev, network
from scripts.mocks import deploy_mocks

def deploy_lottery():
    account = get_account(0)
    
    current_network = network.show_active();
    if (current_network == 'development'):
        print('Deploying mocks..')
        deploy_mocks()
        print('Deployed mocks!')
        eth_usd_address = MockV3Aggregator[-1].address
    else:
        eth_usd_address = config["networks"][current_network]["eth_usd_price_feed"]
    
    print('Deploying lottery..')
    lottery = Lottery.deploy(eth_usd_address, { "from": account })
    print('Deployed lottery!')
    
    return lottery;

def main():
    deploy_lottery()