    // Mostrar el input de archivo al hacer clic en "Reemplazar Imagen"
    document.getElementById('replace-image-btn').addEventListener('click', function () {
        // Mostrar el input de archivo de imagen
        document.getElementById('id_profile_picture').click();
    });

    // Optional: Mostrar el nombre del archivo seleccionado después de elegir una imagen
    document.getElementById('id_profile_picture').addEventListener('change', function () {
        if (this.files && this.files[0]) {
            alert('Imagen seleccionada: ' + this.files[0].name); // Puedes mostrar este nombre en un lugar específico si lo prefieres
        }
    });