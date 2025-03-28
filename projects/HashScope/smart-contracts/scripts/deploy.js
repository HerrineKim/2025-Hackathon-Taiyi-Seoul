// scripts/deploy.js
const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying HSK Token and Deposit contracts to HSK Network...");
  console.log("Network URL:", process.env.HSK_RPC_URL || "https://mainnet.hsk.xyz");
  console.log("Block Explorer:", process.env.BLOCKSCOUT_URL || "https://hashkey.blockscout.com");

  // HSK 토큰 배포
  const HSKToken = await ethers.getContractFactory("HSKToken");
  const initialSupply = 1000000; // 초기 발행량 (예: 1,000,000 HSK)
  console.log("Deploying HSK Token with initial supply:", initialSupply);
  const hskToken = await HSKToken.deploy(initialSupply);
  await hskToken.deployed();
  console.log("HSK Token deployed to:", hskToken.address);

  // 예치 컨트랙트 배포
  const HSKDeposit = await ethers.getContractFactory("HSKDeposit");
  console.log("Deploying HSK Deposit contract with token address:", hskToken.address);
  const hskDeposit = await HSKDeposit.deploy(hskToken.address);
  await hskDeposit.deployed();
  console.log("HSK Deposit contract deployed to:", hskDeposit.address);

  console.log("Deployment completed!");
  console.log("-----------------------------------");
  console.log("HSK Token address:", hskToken.address);
  console.log("HSK Deposit address:", hskDeposit.address);
  console.log("-----------------------------------");
  console.log("Don't forget to update your .env file with these addresses!");
  console.log("To verify contracts on HSK block explorer:");
  console.log(`npx hardhat verify --network hskMainnet ${hskToken.address} ${initialSupply}`);
  console.log(`npx hardhat verify --network hskMainnet ${hskDeposit.address} ${hskToken.address}`);
  console.log("-----------------------------------");
  console.log("Note: Verification may take a few minutes to complete.");
  console.log(`You can check the verification status at: ${process.env.BLOCKSCOUT_URL || "https://hashkey.blockscout.com"}/address/${hskToken.address}#code`);
  console.log(`You can check the verification status at: ${process.env.BLOCKSCOUT_URL || "https://hashkey.blockscout.com"}/address/${hskDeposit.address}#code`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
