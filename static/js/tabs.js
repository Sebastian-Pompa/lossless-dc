document.addEventListener('DOMContentLoaded', function () {
    // Obtener las pestañas y el contenido
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.content');

    // Función para cambiar a la pestaña activa
    function changeTab(event) {
        // Eliminar la clase 'tab_active' de todas las pestañas
        tabs.forEach(tab => tab.classList.remove('tab_active'));

        // Añadir la clase 'tab_active' a la pestaña seleccionada
        event.target.classList.add('tab_active');

        // Ocultar todo el contenido
        contents.forEach(content => content.classList.remove('content_active'));

        // Mostrar el contenido correspondiente a la pestaña seleccionada
        if (event.target.id === 'tab_home') {
            document.getElementById('home_content').classList.add('content_active');
        } else if (event.target.id === 'tab_tutorial') {
            document.getElementById('tutorial_content').classList.add('content_active');
        } else if (event.target.id === 'tab_documentation') {
            document.getElementById('documentation_content').classList.add('content_active');
        }
    }

    // Asignar evento a cada pestaña
    tabs.forEach(tab => {
        tab.addEventListener('click', changeTab);
    });
});
