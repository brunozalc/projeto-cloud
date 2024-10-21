import httpx
from fastapi import HTTPException


async def get_external_data(current_user: dict):
    """
    Busca um fato aleatório sobre cães da API Dog Facts.

    Args:
        current_user (dict): O usuário logado

    Returns:
        dict: Um fato aleatório sobre cães
    """

    url = "https://dog-api.kinduff.com/api/facts"
    params = {
        "number": 3,  # três fatos sobre cachorros
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data and "facts" in data and isinstance(data["facts"], list) and len(data["facts"]) >= 3:
                return {"facts": data["facts"][:3]}
            else:
                return {"facts": "não foi possível obter um fato sobre cães neste momento."}

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code,
                                detail=f"Erro ao acessar a API externa: {e.response.text}")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503,
                                detail=f"Erro ao acessar a API externa: {str(e)}")
