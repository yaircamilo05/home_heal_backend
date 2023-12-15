# Este es el Backend de la Plataforma Home-Heal

¡Bienvenido al repositorio del Backend de la Plataforma Home-Heal! Este componente es esencial para la lógica de negocio y la gestión de datos, proporcionando el soporte necesario para el funcionamiento de la aplicación Home-Heal.

## Requisitos Adicionales

Para el completo funcionamiento del backend, también son necesarios los siguientes proyectos:

1. *Frontend Home-Heal:*
   Asegúrate de tener el Frontend de Home-Heal correctamente configurado y desplegado. Puedes encontrar el repositorio [aquí](https://github.com/yaircamilo05/home_heal_frontend).

2. *Socket Home-Heal:*
   El Socket de Home-Heal es crucial para la comunicación en tiempo real. Asegúrate de tenerlo instalado y funcionando correctamente. Puedes encontrar el repositorio [aquí](https://github.com/yaircamilo05/home_heal_socket).

## Configuración del Backend

Asegúrate de seguir estos pasos para la correcta configuración del backend:

1. Crea un ambiente virtual de Python con la versión 3.11.3.

    bash
    python3.11 -m venv myenv
    

2. Activa el ambiente virtual.

    - En Linux/macOS:
      bash
      source myenv/bin/activate
      

    - En Windows:
      bash
      myenv\Scripts\activate
      

3. Instala las dependencias necesarias.

    bash
    pip install -r requirements.txt
    

4. Para obtener las variables de entorno necesarias, consulta la documentación [aquí](https://unmarred-sunfish-d33.notion.site/Variables-de-entorno-de-home-heal-f34f260e4eb649ab86fb07332ab74b2a).

5. Inicia el backend.

    bash
    uvicorn main:app --reload
    

¡Listo! El Backend de la Plataforma Home-Heal está ahora configurado y listo para su uso.

## Contribuciones

Si deseas contribuir a este proyecto, ¡te damos la bienvenida! Por favor, consulta nuestras pautas de contribución antes de enviar cualquier solicitud.

¡Gracias por ser parte de Home-Heal!
