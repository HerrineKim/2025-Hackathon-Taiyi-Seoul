# Project Name

HashScope

## Overview

https://hashscope.vercel.app/

This project builds an API platform on the HSK blockchain, providing real-time crypto market data for AI agents to predict market trends and execute automated trades. Users log in with their wallets, stake a certain amount of HSK tokens, and receive a Secret Key to access the API. Fees are charged based on API usage, deducted directly from staked tokens. Additionally, individuals can contribute their own data sources to the platform and earn HSK rewards when their data is utilized, creating a sustainable data economy.

## Tech Stack

- Frontend: Next.js, Tailwind CSS, Shadcn UI, Figma
- Backend: FastAPI, SQLite3, Open Zeppelin
- Other: Vercel, AWS EC2, Git

## Demo

- Demo Video: [YouTube link]
- Project Deck: [Google Slides link]

## Team

- SeungWoon Song - PM, Backend
- Hyerin Kim - Design, Frontend

## API Flow

1. **User Registration & Authentication**
   - Users connect their HSK wallet
   - Backend verifies wallet signature
   - User receives JWT token for authentication

2. **API Key Management**
   - Users can generate API keys through the dashboard
   - Each API key has a unique ID and secret
   - Rate limits can be configured per API key

3. **Token Staking & Fee Deduction**
   - Users stake HSK tokens to use the API
   - Fees are automatically deducted based on API usage
   - Every 10 API calls result in a 0.01 HSK deduction(Only for PoC, will be changed later)

4. **API Usage & Monitoring**
   - Users can monitor their API usage through the dashboard
   - Usage statistics include call counts, endpoints, and costs
   - Historical data is available for analysis

## Available APIs

### Cryptocurrency Data APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/crypto/btc/usd` | GET | Get BTC price in USD from Binance |
| `/crypto/btc/krw` | GET | Get BTC price in KRW from Upbit |
| `/crypto/usdt/krw` | GET | Get USDT price in KRW from Upbit |
| `/crypto/kimchi-premium` | GET | Get kimchi premium percentage between Korean and global markets |
| `/crypto/prices` | GET | Get major cryptocurrency prices (BTC, ETH, XRP) |

### Social Media APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/social/trump` | GET | Get Donald Trump's latest posts from Truth Social |
| `/social/elon` | GET | Get Elon Musk's latest posts from X (Twitter) |
| `/social/x/trends` | GET | Get current trending topics on X (Twitter) |

### Derivatives Market APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/derivatives/funding-rates` | GET | Get current funding rates for major cryptocurrency futures markets |
| `/derivatives/open-interest` | GET | Get open interest ratios for major cryptocurrency derivatives |

### Blockchain Projects APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/projects/hsk` | GET | Get latest updates and developments from HashKey Chain |
| `/projects/ethereum/standards` | GET | Get information about new Ethereum standards and proposals |
| `/projects/solana` | GET | Get latest updates and developments from Solana blockchain |

### Open Source APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/opensource/bitcoin` | GET | Get latest pull requests, stars, and activities from Bitcoin Core repository |
| `/opensource/ethereum` | GET | Get latest pull requests, stars, and activities from Ethereum Core repositories |

### API Management Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api-keys` | POST | Create a new API key |
| `/api-keys` | GET | List all API keys |
| `/api-keys/{key_id}` | GET | Get API key details |
| `/api-keys/{key_id}/usage` | GET | Get API key usage statistics |
| `/api-keys/{key_id}/history` | GET | Get detailed API usage history |

## Smart Contracts

The HashScope platform utilizes smart contracts built on the HSK blockchain to handle token staking, fee deduction, and reward distribution.

### HSKDeposit Contract

The main contract that handles HSK token deposits and usage fee deductions.

**Key Features:**
- Native HSK deposits and withdrawals
- Automated fee deduction based on API usage
- Event emission for tracking transactions
- Owner-controlled fee adjustment

**Main Functions:**
- `deposit()`: Allows users to deposit HSK tokens
- `withdraw(uint256 amount)`: Allows users to withdraw their HSK tokens
- `deductForUsage(address user, uint256 amount, address recipient)`: Deducts usage fees from user's balance
- `getBalance(address user)`: Returns the user's current balance

**Events:**
- `Deposited(address indexed user, uint256 amount)`
- `Withdrawn(address indexed user, uint256 amount)`
- `UsageDeducted(address indexed user, uint256 amount, address recipient)`

### Contract Deployment

The smart contracts are deployed on the HSK blockchain at the following addresses:
- HSKDeposit: `0x0D313B22601E7AD450DC9b8b78aB0b0014022269`
