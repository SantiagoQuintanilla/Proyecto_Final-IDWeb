// Validación formulario de contacto
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.contacto-form form');
    if(form){
        form.addEventListener('submit', (e) => {
            const email = form.querySelector('input[type="email"]');
            const nombre = form.querySelector('input[placeholder="*Nombre(s)"]');
            if(!email.value.includes('@') || nombre.value.length < 2){
                alert("Por favor completa correctamente los campos requeridos");
                e.preventDefault();
            }
        });
    }

    // Menú dinámico: resaltar link activo
    const links = document.querySelectorAll('nav a');
    links.forEach(link => {
        if(link.href === window.location.href){
            link.classList.add('activo');
        }
    });

    // Animación en tarjetas de portafolio o servicios
    const tarjetas = document.querySelectorAll('.tarjeta');
    tarjetas.forEach(tarjeta => {
        tarjeta.addEventListener('mouseenter', () => {
            tarjeta.style.transform = 'scale(1.05)';
            tarjeta.style.transition = '0.3s';
        });
        tarjeta.addEventListener('mouseleave', () => {
            tarjeta.style.transform = 'scale(1)';
        });
    });
});