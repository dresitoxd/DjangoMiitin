
//Contador de cerrar sesion

    let countdown = 3; // Contador de 3 segundos
    const swalMessage = Swal.fire({
        icon: 'success',
        title: 'Has cerrado sesión correctamente',
        text: 'Redirigiendo al inicio en ' + countdown + ' segundos...',
        showConfirmButton: false,
        timer: 3000, // Duración de la alerta (en milisegundos)
        willClose: () => {
            window.location.href = "{% url 'index' %}";
        },
        customClass: {
            popup: 'swal-popup',
            title: 'swal-title',
            text: 'swal-text',
        }
    });

    // Actualizar el mensaje del contador
    const updateCountdown = setInterval(function() {
        countdown--;
        swalMessage.update({
            text: 'Redirigiendo al inicio en ' + countdown + ' segundos...'
        });

        if (countdown <= 0) {
            clearInterval(updateCountdown);
        }
    }, 1000); // Actualiza cada 1 segundo