from typing import Optional

from pydantic import BaseModel, HttpUrl

a = {
    'access_token': 'ya29.a0AfB_byBY60vi0_kUfEkjkNt-NM_9U2uc7gG-o93PKurnOdVQrrR_edZYXNL0yJbuf4zj4FJamO_X667jH1uYLqSiAfzUeRQyikT08Cd7uKWdZld_aMEcaLyRh6raHtpEImyaCkj4NlNZbWQARBm8AqEGF4NyEu8sOjiZaCgYKAT0SARASFQHGX2MiesvH6KatBSM-uR542_Lm9Q0171',
    'expires_in': 3599,
    'scope': 'https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/userinfo.profile',
    'token_type': 'Bearer',
    'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjBhZDFmZWM3ODUwNGY0NDdiYWU2NWJjZjVhZmFlZGI2NWVlYzllODEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI2Njc2MDE0NzgwNDMtaDFvOGhkbG84djRlYXBlMzg3cW1kZWhnN2duOGppZ2EuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI2Njc2MDE0NzgwNDMtaDFvOGhkbG84djRlYXBlMzg3cW1kZWhnN2duOGppZ2EuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTQ5MTgzMjYxODIyOTk3NzIxNTIiLCJlbWFpbCI6Im1vbGFuZHJpb3VzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoiMEpRLU5hcDZkanlTVC1uY2lOMV94ZyIsIm5vbmNlIjoiT0dWQ3hmcmUycnF4eE95VEVudDYiLCJuYW1lIjoiRGFuaWxhIFNoYWtob3RraW4gKE1vbGFuZHJpb3VzKSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLcmpKTnVZQTNnTzFWMUxwR3NocHo4MXMzS1FDaTdMelJkUk82LUpRNnNiUT1zOTYtYyIsImdpdmVuX25hbWUiOiJEYW5pbGEiLCJmYW1pbHlfbmFtZSI6IlNoYWtob3RraW4iLCJsb2NhbGUiOiJlbi1HQiIsImlhdCI6MTcwMjc1NzA0NiwiZXhwIjoxNzAyNzYwNjQ2fQ.as-G4qP5P1Ve2V9NgYbIBWDlxh47NVxffUIIsn7Kxkb1mUGEM6SOpYn7xGHvtu9afJ2DiH6RnZfahC3XPJkJr6Bgprxzy1aCRalQ7Z4AX7lDbQhOMFsS8ZC8gTRBqhPN0GSsDspT9J_kLYYuUgLb9ofd2D2iYlDgjbS5T4HtFUuytVz0H1O2rKNrCFtMvyabBos_uHLpp6e0wXLfbpTAg5w6On6CMXpKJ7okaz9iIwWt1MlLYYR7laaG_RnOOssJepNA4b7SNdZHUPmzIwUqBVY91V0b-AOrrvYdoa6Wet6x8Nl63Ch_mET42R2z7n4pNAOz-QkxpwwONeEcxTjC1Q',
    'expires_at': 1702760645,
    'userinfo': {'iss': 'https://accounts.google.com',
                 'azp': '667601478043-h1o8hdlo8v4eape387qmdehg7gn8jiga.apps.googleusercontent.com',
                 'aud': '667601478043-h1o8hdlo8v4eape387qmdehg7gn8jiga.apps.googleusercontent.com',
                 'sub': '114918326182299772152', 'email': 'molandrious@gmail.com',
                 'email_verified': True, 'at_hash': '0JQ-Nap6djyST-nciN1_xg',
                 'nonce': 'OGVCxfre2rqxxOyTEnt6', 'name': 'Danila Shakhotkin (Molandrious)',
                 'picture': 'https://lh3.googleusercontent.com/a/ACg8ocKrjJNuYA3gO1V1LpGshpz81s3KQCi7LzRdRO6-JQ6sbQ=s96-c',
                 'given_name': 'Danila', 'family_name': 'Shakhotkin', 'locale': 'en-GB',
                 'iat': 1702757046, 'exp': 1702760646}}


class UserInfo(BaseModel):
    sub: str
    iss: str
    azp: str
    aud: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email: str
    email_verified: bool
    name: Optional[str] = None
    at_hash: str
    nonce: str
    locale: str
    picture: Optional[str] = None
    iat: int
    exp: int


class GoogleToken(BaseModel):
    access_token: str
    token_type: str
    scope: str
    id_token: str
    expires_in: int
    expires_at: int
    userinfo: UserInfo
