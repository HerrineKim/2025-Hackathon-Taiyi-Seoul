// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

contract HSKDeposit is Ownable {
    // 사용자별 예치 잔액
    mapping(address => uint256) public balances;
    
    // 예치 이벤트
    event Deposit(address indexed user, uint256 amount);
    // 인출 이벤트
    event Withdraw(address indexed user, uint256 amount);
    // 사용량 차감 이벤트
    event UsageDeducted(address indexed user, uint256 amount, address recipient);
    
    constructor() Ownable(msg.sender) {}
    
    // 토큰 예치 함수 (네이티브 HSK 사용)
    function deposit() external payable {
        require(msg.value > 0, "Amount must be greater than 0");
        
        // 잔액 업데이트
        balances[msg.sender] += msg.value;
        
        // 이벤트 발생
        emit Deposit(msg.sender, msg.value);
    }
    
    // 토큰 인출 함수 - 관리자만 호출 가능
    function withdraw(address user, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[user] >= amount, "Insufficient balance");
        require(address(this).balance >= amount, "Contract has insufficient balance");
        
        // 잔액 업데이트
        balances[user] -= amount;
        
        // 네이티브 HSK 전송
        (bool success, ) = user.call{value: amount}("");
        require(success, "Transfer failed");
        
        // 이벤트 발생
        emit Withdraw(user, amount);
    }
    
    // 사용량에 따라 토큰을 차감하는 함수 - 관리자만 호출 가능
    function deductForUsage(address user, uint256 amount, address recipient) external onlyOwner {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[user] >= amount, "Insufficient balance");
        require(address(this).balance >= amount, "Contract has insufficient balance");
        
        // 사용자 잔액 차감
        balances[user] -= amount;
        
        // 차감된 네이티브 HSK를 수신자에게 전송
        (bool success, ) = recipient.call{value: amount}("");
        require(success, "Transfer failed");
        
        // 이벤트 발생
        emit UsageDeducted(user, amount, recipient);
    }
    
    // 잔액 조회 함수
    function getBalance(address user) external view returns (uint256) {
        return balances[user];
    }
    
    // 컨트랙트 잔액 조회
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
    
    // 컨트랙트가 네이티브 HSK를 받을 수 있도록 receive 함수 구현
    receive() external payable {
        // 직접 전송된 HSK는 deposit 함수를 통해 예치하도록 권장
    }
}
