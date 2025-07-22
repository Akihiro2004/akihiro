import base64

# Obfuscated API keys using Base64
_obfuscated_keys = [
    "QUl6YVN5Q1hlamtoSnZLTWZKV1laN1pCekVuMnhsRmdZU0poam1r",
    "QUl6YVN5QVJNN1pKM3BiOXFpVnUyR2tvQTFfaVpMYjR4dy1hR0VJ",
    "QUl6YVN5QnduRHlKbGVfYkV0c093WEVqWGlONjJ5UnN0LXpHUWs=",
    "QUl6YVN5QWRabjV4TUNVY0FfVG92RC1sQjM3V2FfampmTzNlTGIw",
    "QUl6YVN5QzVWRC1kM2xPaTdjaVlqT1dFVEozUzJ2cC0xQ3ZXcHM="
]

# Decode API keys
API_KEYS = [base64.b64decode(k).decode() for k in _obfuscated_keys]

__all__ = ['API_KEYS']
