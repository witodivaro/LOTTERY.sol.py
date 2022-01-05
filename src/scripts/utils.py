from brownie import accounts, config, network

DEV_NETWORKS = ['development']

def is_dev():
    return network.show_active() in DEV_NETWORKS

def get_account(index):
    if (is_dev()):
        return accounts[index]
    account_name = 'account_' + str(index)
    
    return accounts.add(config["accounts"][account_name])