def decode_token_middleware(token: str):
    from src.auth.handler import decode_jwt

    try:
        payload = decode_jwt(token)
        return payload
    except Exception as e:
        raise Exception(f"Authentication failed: {str(e)}")