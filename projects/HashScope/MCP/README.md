# HashScope MCP - LangChain Tool Integration

HashScope MCP는 AI Agent가 HashScope API를 통해 암호화폐 데이터에 쉽게 접근할 수 있도록 하는 LangChain Tool 통합 라이브러리입니다.

## 설치 방법

```bash
pip install hashscope-mcp
```

## 사용 방법

### 기본 사용법

```python
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from hashscope_mcp import HashScopeToolkit

# HashScope API 키 설정
api_key_id = "hsk_your_api_key_id"
api_key_secret = "sk_your_api_key_secret"

# HashScope 도구 초기화
toolkit = HashScopeToolkit(api_key_id=api_key_id, api_key_secret=api_key_secret)
tools = toolkit.get_tools()

# LangChain Agent 초기화
llm = OpenAI(temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Agent 실행
agent.run("비트코인의 현재 가격과 최근 시장 동향을 알려줘")
```

### 개별 도구 사용

```python
from hashscope_mcp import (
    get_crypto_price_tool,
    get_crypto_market_data_tool,
    get_crypto_onchain_data_tool
)
from hashscope_mcp.hashscope_client import HashScopeClient

# HashScope 클라이언트 초기화
client = HashScopeClient(
    api_key_id="hsk_your_api_key_id",
    api_key_secret="sk_your_api_key_secret"
)

# 개별 도구 생성
price_tool = get_crypto_price_tool(client)
market_tool = get_crypto_market_data_tool(client)
onchain_tool = get_crypto_onchain_data_tool(client)

# 도구 사용
btc_price = price_tool.run({"symbol": "BTC", "currency": "USD"})
print(btc_price)

btc_market = market_tool.run({"symbol": "BTC"})
print(btc_market)
```

## 사용 가능한 도구

HashScope MCP는 다음과 같은 도구를 제공합니다:

1. **get_crypto_price**: 암호화폐의 현재 가격 조회
2. **get_crypto_historical_prices**: 암호화폐의 과거 가격 데이터 조회
3. **get_crypto_market_data**: 시가총액, 거래량 등 시장 데이터 조회
4. **get_trending_coins**: 인기 있는 암호화폐 목록 조회
5. **get_crypto_onchain_data**: 온체인 데이터(활성 주소, 트랜잭션 수 등) 조회
6. **get_wallet_balance**: 지갑 주소의 잔액 조회
7. **get_crypto_social_data**: 소셜 미디어 감성 분석 데이터 조회
8. **get_crypto_news**: 암호화폐 관련 최신 뉴스 조회

## 예제: LangChain과 함께 사용하기

```python
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from hashscope_mcp import HashScopeToolkit

# API 키 설정
api_key_id = "hsk_your_api_key_id"
api_key_secret = "sk_your_api_key_secret"

# HashScope 도구 초기화
toolkit = HashScopeToolkit(api_key_id=api_key_id, api_key_secret=api_key_secret)
tools = toolkit.get_tools()

# LangChain Agent 초기화
llm = ChatOpenAI(model="gpt-4", temperature=0)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 복잡한 질문에 대한 응답
response = agent.run("""
다음 질문에 답해줘:
1. 비트코인과 이더리움의 현재 가격은 얼마인가?
2. 지난 30일 동안 비트코인의 가격 변화는 어떠했는가?
3. 현재 가장 인기 있는 암호화폐 3개는 무엇인가?
4. 비트코인에 대한 소셜 미디어 감성은 어떠한가?
""")

print(response)
```

## API 키 발급 방법

HashScope API 키를 발급받으려면:

1. [HashScope 웹사이트](https://hashscope.io)에 방문하여 계정을 생성합니다.
2. 대시보드에서 "API 키 관리" 섹션으로 이동합니다.
3. "새 API 키 생성" 버튼을 클릭합니다.
4. API 키 ID와 시크릿을 안전하게 저장합니다.

## 주의사항

- API 키 시크릿은 절대로 공개 저장소에 커밋하지 마세요.
- 환경 변수나 안전한 시크릿 관리 도구를 사용하여 API 키를 관리하세요.
- API 사용량에 따라 과금될 수 있으므로 사용량을 모니터링하세요.

## 라이선스

MIT License
