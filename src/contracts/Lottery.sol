// SPDX-License-Identifier: MIT

pragma solidity ^0.8.11;

import "./PriceOracle.sol";
import "./Randomizer.sol";

contract Lottery is PriceOracle, Randomizer {
    address payable[] public players;
    address public owner;
    address public lastWinner;

    uint256 requiredUsdValue = 50;
    uint256 requiredWeiValue;
    uint256 public lotteryBalance;

    // 2.50 %
    uint256 public ownersFeePercentage = 250;
    uint256 public ownersFeeDecimals = 2;

    bool isLocked = true;

    mapping(address => bool) public isEnteredByAddress;
    mapping(address => bool) isAdminByAddress;

    constructor(address _ethUsdPriceFeed) PriceOracle(_ethUsdPriceFeed) {
        owner = msg.sender;
        requiredWeiValue = convertUsdToWei(0, requiredUsdValue);
        isAdminByAddress[owner] = true;
    }

    modifier onlyWhenUnlocked() {
        if (isLocked) {
            revert("The contract is locked");
        } else {
            _;
        }
    }

    modifier withRequiredUsdValue(uint256 minUsdValue) {
        uint256 minWeiValue = convertUsdToWei(0, minUsdValue);
        require(msg.value >= minUsdValue, "Insufficient transfer amount");

        _;
    }

    modifier adminOnly() {
        require(isAdminByAddress[msg.sender], "Allowed to admins only");
        _;
    }

    modifier nonParticipantsOnly() {
        require(
            !isEnteredByAddress[msg.sender],
            "Not allowed for lottery participants"
        );
        _;
    }

    function enter()
        public
        payable
        onlyWhenUnlocked
        nonParticipantsOnly
        withRequiredUsdValue(requiredUsdValue)
    {
        require(
            !isEnteredByAddress[msg.sender],
            "You are already participating"
        );

        lotteryBalance += msg.value;
        isEnteredByAddress[msg.sender] = true;
        players.push(payable(msg.sender));
        sendChange(requiredWeiValue);
    }

    function getEntranceFee() public view returns (uint256) {
        uint256 weiEntranceFee = convertUsdToWei(0, requiredUsdValue);
        return weiEntranceFee;
    }

    function sendChange(uint256 requiredValue) internal {
        uint256 change = msg.value - requiredValue;
        address payable returnAddress = payable(msg.sender);
        returnAddress.transfer(change);
    }

    function startLottery() public adminOnly {
        isLocked = false;
    }

    function getTotalWinAndFee() public view returns (uint256, uint256) {
        uint256 ownersFee = (lotteryBalance * ownersFeePercentage) /
            (10**(2 + ownersFeeDecimals));

        uint256 totalWin = lotteryBalance - ownersFee;

        return (totalWin, ownersFee);
    }

    function endLottery() public onlyWhenUnlocked adminOnly {
        require(players.length > 1, "Not enough players");

        isLocked = true;

        uint256 winnerIndex = pickWinner(players.length);
        address payable winner = players[winnerIndex];

        (uint256 amountToSend, uint256 ownersFee) = getTotalWinAndFee();

        for (uint256 i = 0; i < players.length; i++) {
            isEnteredByAddress[players[i]] = false;
        }

        delete players;
        lotteryBalance = 0;
        lastWinner = winner;

        payable(owner).transfer(ownersFee);
        winner.transfer(amountToSend);
    }

    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    function pickWinner(uint256 arrayLength) internal view returns (uint256) {
        return getRandomValue(0, arrayLength - 1);
    }
}
