# API

a API é muito simples, e possui apenas três *endpoints*. a ideia é que, ao final, você consiga usá-la para ver três fatos aleatórios sobre cachorros, quando quiser! 🐶

o serviço tem um sistema de autenticação, baseado em [json web tokens (jwt)](https://jwt.io/). para que sua requisição `GET` seja aceita, você precisa fornecer um *token* válido

# 1. endpoint de registro

url: `/registrar`

método aceito: `POST`

**exemplo de requisição:**

```json
{
  "name": "string",
  "email": "user@string.com",
  "password": "string"
}
```

**exemplo de resposta:**

```json
{
  "access_token": "seu_token_jwt",
  "token_type": "bearer"
}
```

# 2. endpoint de login

url: `/login`

método aceito: `POST`

**exemplo de requisição:**

```json
{
  "name": "string",
  "password": "string"
}
```

**exemplo de resposta:**

```json
{
  "access_token": "seu_token_jwt",
  "token_type": "bearer"
}
```

# 3. endpoint de consulta a fatos caninos

url: `/consulta`

método aceito: `GET`

**exemplo de requisição (com token):**

```bash
curl -X 'GET' \
  'http://localhost:8000/consultar' \
  -H 'accept: application/json' \
  -H 'Authorization: seu_token_jwt'
```

**exemplo de resposta:**

```json
{
  "facts": [
    "fato canino 1",
    "fato canino 2",
    "fato canino 3"
  ]
}
```

 caso você esteja testando a API através da documentação interativa, é necessário que você:

1. copie o *token* gerado por alguma das requisições anteriores
2. aperte o botão "Authorize", localizado no canto superior direito da página
3. insira seu *token* e faça *login*
