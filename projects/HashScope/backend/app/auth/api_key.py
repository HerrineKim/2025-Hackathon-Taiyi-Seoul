from fastapi import Depends, HTTPException, Header, status, Request
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models import APIKey, APIUsage

def verify_api_key(
    api_key: str = Header(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """
    API 키 검증 함수
    
    Args:
        api_key (str): API 키
        request (Request): 요청 객체 (경로 및 메서드 추적용)
        db (Session): 데이터베이스 세션
        
    Returns:
        APIKey: 검증된 API 키 객체
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API 키가 필요합니다"
        )
    
    # 데이터베이스에서 API 키 조회
    db_api_key = db.query(APIKey).filter(APIKey.key_id == api_key).first()
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 API 키입니다"
        )
    
    if not db_api_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비활성화된 API 키입니다"
        )
    
    # API 키 사용량 업데이트
    db_api_key.call_count += 1
    db_api_key.last_used_at = datetime.utcnow()
    
    # 요청 경로 및 메서드 추적 (요청 객체가 제공된 경우)
    if request:
        # API 사용 기록 저장
        endpoint = request.url.path
        method = request.method
        
        # 새 API 사용 기록 생성
        api_usage = APIUsage(
            api_key_id=db_api_key.id,
            endpoint=endpoint,
            method=method,
            timestamp=datetime.utcnow()
        )
        db.add(api_usage)
    
    db.commit()
    
    return db_api_key

def get_api_key_with_tracking(
    api_key: str = Header(...),
    request: Request = None,
    db: Session = Depends(get_db)
):
    """
    API 키 검증 및 사용량 추적 함수
    
    Args:
        api_key (str): API 키
        request (Request): 요청 객체
        db (Session): 데이터베이스 세션
        
    Returns:
        APIKey: 검증된 API 키 객체
    """
    return verify_api_key(api_key, request, db)
