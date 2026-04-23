#!/usr/bin/env python3
"""
测试客户端模块
"""

import pytest
from ima_mcp.client import IMAClient


def test_client_initialization():
    """测试客户端初始化"""
    client = IMAClient()
    assert client is not None
    assert client.credentials is not None
    assert client.session is not None


def test_check_credentials():
    """测试凭证检查"""
    client = IMAClient()
    result = client.check_credentials()
    assert isinstance(result, dict)
    assert 'valid' in result
    assert 'message' in result
