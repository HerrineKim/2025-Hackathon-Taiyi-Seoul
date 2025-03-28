require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-ethers");
require("@nomiclabs/hardhat-etherscan");
require("dotenv").config();

// 환경 변수에서 값을 가져옵니다.
const PRIVATE_KEY = process.env.PRIVATE_KEY || "";
const HSK_RPC_URL = process.env.HSK_RPC_URL || "https://mainnet.hsk.xyz";
const BLOCKSCOUT_API_KEY = process.env.BLOCKSCOUT_API_KEY || "";
const BLOCKSCOUT_URL = process.env.BLOCKSCOUT_URL || "https://hashkey.blockscout.com";

// 네트워크 설정
module.exports = {
  solidity: "0.8.20",
  networks: {
    // HSK 메인넷 설정
    hskMainnet: {
      url: HSK_RPC_URL,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
      chainId: 177 // HSK 네트워크의 실제 체인 ID: 177
    },
    // 로컬 개발 네트워크
    hardhat: {
      chainId: 31337
    }
  },
  // Blockscout 검증 설정
  etherscan: {
    apiKey: {
      hskMainnet: BLOCKSCOUT_API_KEY
    },
    customChains: [
      {
        network: "hskMainnet",
        chainId: 177, // HSK 네트워크의 실제 체인 ID: 177
        urls: {
          apiURL: `${BLOCKSCOUT_URL}/api`,
          browserURL: BLOCKSCOUT_URL
        }
      }
    ]
  },
  // 컴파일러 설정
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  }
};
