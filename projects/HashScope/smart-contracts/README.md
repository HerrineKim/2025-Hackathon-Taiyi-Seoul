# HSK 토큰 및 예치 컨트랙트 프로젝트

이 프로젝트는 HSK 블록체인 네트워크에 배포할 HSK 토큰 및 예치 컨트랙트를 포함하고 있습니다.

## 프로젝트 구성

- `contracts/HSKToken.sol`: ERC-20 표준을 따르는 HSK 토큰 컨트랙트
- `contracts/HSKDeposit.sol`: 사용자가 HSK 토큰을 예치할 수 있는 예치 컨트랙트
- `scripts/deploy.js`: 컨트랙트 배포 스크립트

## 설치 및 설정

1. 의존성 패키지 설치:
```shell
npm install
```

2. `.env` 파일 생성 및 설정:
```
# 이더리움 지갑 개인키
PRIVATE_KEY=your_wallet_private_key_here

# HSK 네트워크 RPC URL (기본값: https://mainnet.hsk.xyz)
HSK_RPC_URL=https://mainnet.hsk.xyz

# Blockscout API 키 (https://hashkey.blockscout.com에서 발급)
BLOCKSCOUT_API_KEY=your_blockscout_api_key_here

# HSK 블록 탐색기 URL
BLOCKSCOUT_URL=https://hashkey.blockscout.com
```

## 컴파일 및 배포

1. 컨트랙트 컴파일:
```shell
npx hardhat compile
```

2. HSK 메인넷에 배포:
```shell
npx hardhat run scripts/deploy.js --network hskMainnet
```

3. 배포 후 `.env` 파일 업데이트:
```
HSK_TOKEN_ADDRESS=배포된_토큰_주소
DEPOSIT_CONTRACT_ADDRESS=배포된_예치_컨트랙트_주소
```

## 컨트랙트 검증

HSK 블록체인은 Blockscout 기반 블록 탐색기를 사용합니다. 컨트랙트를 검증하려면:

```shell
# HSK 토큰 컨트랙트 검증
npx hardhat verify --network hskMainnet <HSK_TOKEN_ADDRESS> 1000000

# 예치 컨트랙트 검증
npx hardhat verify --network hskMainnet <DEPOSIT_CONTRACT_ADDRESS> <HSK_TOKEN_ADDRESS>
```

검증 후 Blockscout 블록 탐색기에서 컨트랙트 코드와 상호작용할 수 있습니다:
- https://hashkey.blockscout.com/address/<HSK_TOKEN_ADDRESS>#code
- https://hashkey.blockscout.com/address/<DEPOSIT_CONTRACT_ADDRESS>#code

## 테스트

```shell
npx hardhat test
