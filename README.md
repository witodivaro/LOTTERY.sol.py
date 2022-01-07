# ETH Smart Contract Lottery

## Warning! 

Please <b>DO NOT</b> use this lottery code in PRODUCTION. The `Randomizer.sol` contract provides predictable values, so the lottery game itself is exploitable.
<br>To fix the randomizer, you should implement the [Chainlink VRF](https://docs.chain.link/docs/chainlink-vrf/) integration.


### Description

<p>ETH Smart Contract Lottery application implements the <code>Lottery</code> game on the decentralized blockchain Ethereum. It uses <code>Solidity</code> language to implement the smart contracts. Deployment & interaction with the contract is achieved with the help of the <code>ETH-Brownie</code> Python Framework for Solidity interactions.</p>

<p>
  The owner of the contract (=the address which deployed the contract) is automatically set to be the <code>admin</code>. The <code>admin</code> can call a   <code>startLottery</code> function to unlock the registrations. The <code>admin</code> must specify the entrance fee in <code>USD</code> by passing the <code>usd _amount</code> as a <code>startLottery</code> function argument.
</p>
<p>
  Any address can enter the lottery by transfering the required value to the <code>enter</code> function. The entrance fee in WEI can be determined by calling the <code>getEntranceFee</code> function. If a user passes the value above the <code>required fee</code>, he will be returned a <code>change = value - required_fee</code>. An address can enter the lottery only <code>once</code> per game. At any given time, the <code>admin</code> can call an <code>endLottery</code> function to determine the winner. The owner of the contract will receive a fee of <code>2.5%</code> of the total prize. The left amount of <code>97.5%</code> will be kept on the contract until the actual winner calls a <code>withdraw</code> function.
</p>


### Navigation

<ul>
  <li><a href="#start">Requirements</a></li>
  <li><a href="#run_local">Deploy & Run the smart contract locally</a></li>
  <li><a href="#run_testnet">Deploy & Run the smart contract on a test network</a></li>
</ul>

<h2 id="start">Requirements</h2>
<ol>
  <li>Install the <code>eth-brownie</code> python Solidity framework. It is better to install it globally using <code>pipx install eth-brownie</code></li>
  <li>Activate your python environment.</li>
  <li>Install the requirements with the <code>pip install requirements.txt</code> command in the root folder</li>
  <li>Install the <code>ganache-cli</code> globally with <code>npm i -g ganache-cli</code> to run the blockchain locally</li>
  <li>Navigate to the <code>src</code> folder. Now you are able to use any brownie command you want</li>
</ol>

<h2 id="run_local">Deploy & Run the smart contract locally</h2>
<ol>
  <li>Make sure you have brownie, ganache-cli & python packages installed</li>
  <li>Navigate to the <code>src</code> folder</li>
  <li>Deploy the contract to the local blockchain with <code>brownie run scripts/deploy.py</code></li>
  <li>Use <code>brownie run scripts/run_lottery.py</code> to deploy & run the lottery</li>
</ol>

<h2 id="run_testnet">Deploy & Run the smart contract on a test network</h2>
<ol>
  <li>Make sure you have brownie, ganache-cli & python packages installed</li>
  <li>List your network in <code>brownie-config.yaml</code> under the <code>networks</code> field and add the respective ETH/USD Price Feed address. Use this <a href="https://docs.chain.link/docs/ethereum-addresses/">data feeds</a> list to find your network feed</li>
  <li>Make sure the 5 <b>private keys</b> specified in <code>brownie-config.yaml</code> under <code>accounts/account_[index]</code> fields are linked to the accounts that have enough ETH (>= 0.1) on a wanted network. You can fund your accounts using public faucets like the <a href="https://faucets.chain.link/rinkeby">Rinkeby faucet</a>
  <li>Run <code>brownie compile</code> to compile the contract and check if the solidity code has no syntax errors</li>
  <li>Run <code>brownie run scripts/deploy.py --network={YOUR_NETWORK}</code> to deploy the contract to your test network</li>
  <li>Run <code>brownie run scripts/run_lottery.py --network={YOUR_NETWORK}</code> to initiate a test lottery-game flow</li>
</ol>
