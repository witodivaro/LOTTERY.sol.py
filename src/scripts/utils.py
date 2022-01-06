from brownie import accounts, config, network

DEV_NETWORKS = ['development']
FORK_NETWORKS = ['mainnet-fork']

def is_dev():
    return network.show_active() in DEV_NETWORKS

def is_fork():
    return network.show_active() in FORK_NETWORKS

def get_account(index):
    if (is_dev() or is_fork()):
        return accounts[index]
    account_name = 'account_' + str(index)
    
    return accounts.add(config["accounts"][account_name])