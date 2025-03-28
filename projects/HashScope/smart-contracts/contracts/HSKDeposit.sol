// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HSKDeposit is Ownable {
    IERC20 public hskToken;
    
    // 사용자별 예치 잔액
    mapping(address => uint256) public balances;
    
    // 예치 이벤트
    event Deposit(address indexed user, uint256 amount);
    // 인출 이벤트
    event Withdraw(address indexed user, uint256 amount);
    
    constructor(address _tokenAddress) Ownable(msg.sender) {
        hskToken = IERC20(_tokenAddress);
    }
    
    // 토큰 예치 함수
    function deposit(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        
        // 사용자로부터 토큰 전송
        require(hskToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");
        
        // 잔액 업데이트
        balances[msg.sender] += amount;
        
        // 이벤트 발생
        emit Deposit(msg.sender, amount);
    }
    
    // 토큰 인출 함수
    function withdraw(uint256 amount) external {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // 잔액 업데이트
        balances[msg.sender] -= amount;
        
        // 토큰 전송
        require(hskToken.transfer(msg.sender, amount), "Transfer failed");
        
        // 이벤트 발생
        emit Withdraw(msg.sender, amount);
    }
    
    // 잔액 조회 함수
    function getBalance(address user) external view returns (uint256) {
        return balances[user];
    }
}
