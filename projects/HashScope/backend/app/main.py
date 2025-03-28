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
    description="""
    # HashScope - 실시간 크립토 시장 데이터 API 플랫폼
    
    HashScope는 AI 에이전트에 실시간 크립토 시장 데이터를 제공하는 API 플랫폼입니다.
    
    ## 주요 기능
    
    * **블록체인 지갑 인증**: HSK 체인 기반 지갑으로 로그인
    * **API 키 관리**: HSK 토큰 예치 후 API 키 발급 및 관리
    * **데이터 API**: 다양한 크립토 데이터 제공 (온체인 데이터, 거래소 데이터, SNS 데이터 등)
    * **토큰 예치 및 과금**: 사용량에 따른 자동 과금 시스템
    * **데이터 제공자 보상**: 데이터 소스 등록 및 보상 시스템
    
    ## 인증 방식
    
    1. **지갑 인증**: `/auth/nonce`와 `/auth/verify` 엔드포인트를 통해 지갑 서명 기반 인증
    2. **API 키 인증**: 데이터 API 호출 시 발급받은 API 키 사용
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
