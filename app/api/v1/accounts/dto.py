from dataclasses import dataclass

@dataclass
class RegisterRequest:
    email: str
    password: str
    
@dataclass
class LoginRequest:
    email: str
    password: str