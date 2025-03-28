from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from app.db.database import get_db, init_db
from app.routers import auth, users, api_keys
from app.auth.dependencies import get_current_user

app = FastAPI(
    title="HashScope API",
    description="""HashScope - 실시간 크립토 시장 데이터 API 플랫폼

HashScope는 AI 에이전트에 실시간 크립토 시장 데이터를 제공하는 API 플랫폼입니다.

## 주요 기능

* 블록체인 지갑 인증: HSK 체인 기반 지갑으로 로그인
* API 키 관리: HSK 토큰 예치 후 API 키 발급 및 관리
* 데이터 API: 다양한 크립토 데이터 제공 (온체인 데이터, 거래소 데이터, SNS 데이터 등)
* 토큰 예치 및 과금: 사용량에 따른 자동 과금 시스템
* 데이터 제공자 보상: 데이터 소스 등록 및 보상 시스템

## 인증 방식

1. 지갑 인증: `/auth/nonce`와 `/auth/verify` 엔드포인트를 통해 지갑 서명 기반 인증
2. API 키 인증: 데이터 API 호출 시 발급받은 API 키 사용

## 지갑 로그인 플로우

1. Nonce 요청: 사용자의 지갑 주소로 `/auth/nonce` API를 호출하여 서명할 메시지를 받습니다.
2. 메시지 서명: 받은 메시지를 MetaMask 등의 지갑으로 서명합니다.
3. 서명 검증: 서명된 메시지와 지갑 주소를 `/auth/verify` API로 전송하여 검증합니다.
4. JWT 토큰 발급: 서명이 유효하면 JWT 토큰이 발급됩니다.
5. 인증된 요청: 이후 모든 API 요청에 `Authorization: Bearer {token}` 헤더를 포함시킵니다.

### 코드 예시 (프론트엔드)

```javascript
// 1. Nonce 요청
async function requestNonce(walletAddress) {
  const response = await fetch('/auth/nonce', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ wallet_address: walletAddress })
  });
  return await response.json();
}

// 2. 메시지 서명 (MetaMask 사용)
async function signMessage(message, walletAddress) {
  try {
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    const signature = await ethereum.request({
      method: 'personal_sign',
      params: [message, walletAddress]
    });
    return signature;
  } catch (error) {
    console.error('Error signing message:', error);
    throw error;
  }
}

// 3. 서명 검증 및 JWT 토큰 발급
async function verifySignature(walletAddress, signature) {
  const response = await fetch('/auth/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      wallet_address: walletAddress,
      signature: signature
    })
  });
  return await response.json();
}

// 4. 전체 로그인 플로우
async function login() {
  // 지갑 연결
  const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
  const walletAddress = accounts[0];
  
  // Nonce 요청
  const { message } = await requestNonce(walletAddress);
  
  // 메시지 서명
  const signature = await signMessage(message, walletAddress);
  
  // 서명 검증 및 토큰 발급
  const { access_token } = await verifySignature(walletAddress, signature);
  
  // 토큰 저장
  localStorage.setItem('token', access_token);
  
  return access_token;
}

// 5. 인증된 API 요청 예시
async function fetchUserProfile() {
  const token = localStorage.getItem('token');
  const response = await fetch('/users/me', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
}
```
""",
    version="0.1.0",
    docs_url=None,  # 기본 /docs 경로 비활성화
    redoc_url=None,  # 기본 /redoc 경로 비활성화
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(api_keys.router, prefix="/api-keys", tags=["API Keys"])

@app.get("/")
def read_root():
    return {"message": "Welcome to HashScope API", "status": "online"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Custom Swagger UI
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API 문서",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
        swagger_favicon_url="/favicon.ico",
    )

# Custom OpenAPI schema
@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
