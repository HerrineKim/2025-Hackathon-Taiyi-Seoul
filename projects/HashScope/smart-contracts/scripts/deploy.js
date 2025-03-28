// scripts/deploy.js
const { ethers } = require("hardhat");
require('dotenv').config();

async function main() {
  console.log("Deploying updated HSK Deposit contract to HSK Network...");
  console.log("Network URL:", process.env.HSK_RPC_URL || "https://mainnet.hsk.xyz");
  console.log("Block Explorer:", process.env.BLOCKSCOUT_URL || "https://hashkey.blockscout.com");

  console.log("Using native HSK for deposits and withdrawals");

  // 예치 컨트랙트 배포
  const HSKDeposit = await ethers.getContractFactory("HSKDeposit");
  console.log("Deploying updated HSK Deposit contract for native HSK");
  const hskDeposit = await HSKDeposit.deploy();
  await hskDeposit.deployed();
  console.log("Updated HSK Deposit contract deployed to:", hskDeposit.address);

  console.log("Deployment completed!");
  console.log("-----------------------------------");
  console.log("New HSK Deposit address:", hskDeposit.address);
  console.log("-----------------------------------");
  console.log("Don't forget to update your .env file with the new deposit address!");
  console.log("To verify contract on HSK block explorer:");
  console.log(`npx hardhat verify --network hsk ${hskDeposit.address}`);
  console.log("-----------------------------------");
  console.log("Note: Verification may take a few minutes to complete.");
  console.log(`You can check the verification status at: ${process.env.BLOCKSCOUT_URL || "https://hashkey.blockscout.com"}/address/${hskDeposit.address}#code`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
