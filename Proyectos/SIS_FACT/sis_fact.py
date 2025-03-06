import requests # Importa la librería requests para realizar peticiones HTTP
    import xml.etree.ElementTree as ET # Importa la librería ElementTree para trabajar con XML

    def obtener_cufd(nit, cuis, codigo_sistema, modalidad):
        """
        Función para obtener el Código Único de Facturación Diaria (CUFD) del SIN.

        Args:
            nit (str): Número de Identificación Tributaria del contribuyente.
            cuis (str): Código Único de Inicio de Sistemas.
            codigo_sistema (str): Código del sistema de facturación.
            modalidad (str): Modalidad de facturación (1 para electrónica en línea).

        Returns:
            str: El CUFD obtenido del SIN, o None si hay un error.
        """
        url = "URL_DEL_SERVICIO_WEB_DEL_SIN"  # Reemplazar con la URL real del servicio web del SIN
        headers = {'Content-Type': 'application/xml'} # Define el encabezado de la petición HTTP como XML
        payload = f"""
        <SolicitudCUFD>
            <nit>{nit}</nit>
            <cuis>{cuis}</cuis>
            <codigoSistema>{codigo_sistema}</codigoSistema>
            <modalidad>{modalidad}</modalidad>
        </SolicitudCUFD>
        """ # Define el cuerpo de la petición XML con los datos del contribuyente
        response = requests.post(url, headers=headers, data=payload) # Realiza la petición POST al servicio web del SIN
        if response.status_code == 200: # Verifica si la petición fue exitosa (código 200)
            root = ET.fromstring(response.content) # Convierte la respuesta XML en un objeto ElementTree
            cufd = root.find('CUFD').text # Extrae el valor del elemento CUFD del XML
            return cufd # Retorna el CUFD obtenido
        else:
            print(f"Error al obtener CUFD: {response.status_code}") # Imprime un mensaje de error si la petición falla
            return None # Retorna None en caso de error

    # Ejemplo de uso
    nit = "TU_NIT" # Reemplazar con el NIT del contribuyente
    cuis = "TU_CUIS" # Reemplazar con el CUIS del contribuyente
    codigo_sistema = "CODIGO_DE_TU_SISTEMA" # Reemplazar con el código del sistema de facturación
    modalidad = "1"  # 1 para facturación electrónica en línea
    cufd = obtener_cufd(nit, cuis, codigo_sistema, modalidad) # Llama a la función para obtener el CUFD
    if cufd:
        print(f"CUFD obtenido: {cufd}") # Imprime el CUFD obtenido si la petición fue exitosa