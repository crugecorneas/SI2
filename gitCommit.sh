#!/bin/bash

# Verifica si se pasó el mensaje de commit como argumento
if [ -z "$1" ]; then
    echo "Por favor, proporciona un mensaje de commit."
    exit 1
fi

# Inicializa las variables de usuario por defecto
user_email=""
user_name=""

# Verifica si se pasó el usuario a configurar
while getopts "IJ" opt; do
    case ${opt} in
        I)
            # Configura los datos de usuario para Iñaki
            user_email="innaki.delafuente@estudidante.uam.es"
            user_name="Iñaki"
            echo "Configuración de usuario: Iñaki"
            ;;
        J)
            # Configura los datos de usuario para Freddy
            user_email="freddy.serrano.zurita@gmail.com"
            user_name="Freddy Serrano Zurita"
            echo "Configuración de usuario: Freddy Serrano Zurita"
            ;;
        *)
            echo "Opción no válida. Usa -I para Iñaki o -J para Freddy."
            exit 1
            ;;
    esac
done

# Si no se seleccionó un usuario, muestra un error
if [ -z "$user_email" ] || [ -z "$user_name" ]; then
    echo "Debes seleccionar un usuario con -I o -J."
    exit 1
fi

# Configura los datos de usuario globalmente
git config --global user.email "$user_email"
git config --global user.name "$user_name"

# Agrega todos los cambios
git add .

# Realiza el commit con el mensaje proporcionado
git commit -m "$1"

# Realiza el push al repositorio remoto
git push

# Mensaje de éxito
echo "Cambios enviados con éxito con el mensaje: $1"
