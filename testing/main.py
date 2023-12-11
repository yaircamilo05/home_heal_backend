from fastapi.testclient import TestClient
from main import app
from schemas.user import UserCreate

client = TestClient(app)


def test_read_main():
    '''
    The function `test_read_main` tests if the response from the `/` endpoint is successful and returns
    the expected JSON message.
    '''
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'Welcome to Home Heal server!'}


# def test_create_user():
#     """
#     Test para verificar la creación de un nuevo usuario mediante el endpoint /user.
#     """

#     # Datos de prueba para crear un nuevo usuario
#     user_data = {
#         "name": "pepe",
#         "lastname": "perez",
#         "email": "pepeperez@mail.com",
#         "image_url": "",
#         "rol_id": 3,
#         "cc": "1002460321",
#         "phone": "3193513308",
#         "password": "Hola123*"
#     }
#     # Agrega otros campos necesarios según tu modelo de usuario

#     # Hacer una solicitud POST al endpoint /user
#     response = client.post("/user/create_user", json=user_data)

#     # Verificar que la respuesta es la esperada
#     assert response.status_code == 201, "La creación del usuario debería ser exitosa"
#     response_data = response.json()

    # assert response_data["data"]["name"] == user_data["name"], \
    #     "El nombre del usuario debe coincidir con el enviado"
    # assert response_data["data"]["lastname"] == user_data["lastname"], \
    #     "el nombre del usuario debe coincidir con el enviado"
    # assert response_data["data"]["email"] == user_data["email"], \
    #     "el correo del usuario debe coincidir con el enviado"
    # assert response_data["data"]["rol_id"] == user_data["rol_id"], \
    #     "el rol del usuario debe coincidir con el enviado"
    # assert response_data["data"]["cc"] == user_data["cc"], \
    #     "la cc del usuario debe coincidir con el enviado"
    # assert response_data["data"]["phone"] == user_data["phone"], \
    #     "el telefono del usuario debe coincidir con el enviado"
