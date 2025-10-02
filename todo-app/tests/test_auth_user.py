
import pytest
from unittest.mock import Mock, patch
from utils.auth_user import *
from sqlalchemy.orm import Session
from fastapi import HTTPException
from jose import JWTError

def test_authenticate_user_valid_credentials():
    # Test successful authentication
    mock_db = Mock(spec=Session)
    mock_user = Mock()
    mock_user.password = "hashed_password"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    with patch('utils.auth_user.verify_password', return_value=True):
        result = authenticate_user(mock_db, 'test_user', 'correct_password')
        assert result == mock_user

def test_authenticate_user_invalid_username():
    # Test authentication with non-existent username
    mock_db = Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = authenticate_user(mock_db, 'invalid_user', 'any_password')
    assert result is False

def test_authenticate_user_wrong_password():
    # Test authentication with wrong password
    mock_db = Mock(spec=Session)
    mock_user = Mock()
    mock_user.password = "hashed_password"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_user

    with patch('utils.auth_user.verify_password', return_value=False):
        result = authenticate_user(mock_db, 'test_user', 'wrong_password')
        assert result is False

def test_authenticate_user_empty_credentials():
    # Test authentication with empty credentials
    mock_db = Mock(spec=Session)
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    result = authenticate_user(mock_db, '', '')
    assert result is False

def test_authenticate_user_special_characters():
    # Test authentication with special characters in credentials
    mock_db = Mock(spec=Session)
    mock_user = Mock()
    mock_user.password = "hashed_password"
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    
    with patch('utils.auth_user.verify_password', return_value=True):
        result = authenticate_user(mock_db, 'test@user!', 'pass#word$')
        assert result == mock_user

def test_create_access_token():
    data = {"sub": "test_user"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0        

def test_get_current_user_invalid_token():
    mock_db = Mock(spec=Session)
    with patch('utils.auth_user.jwt.decode', side_effect=JWTError):
        with pytest.raises(HTTPException) as exc_info:
            import asyncio
            asyncio.run(get_current_user(token="invalid.token.here", db=mock_db))
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Could not validate credentials"