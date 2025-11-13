$(document).ready(function() {
    const messages = [
        "* BIENVENIDO A MI JUEGO, AMOR",
        "* EN ESTE JUEGO, VAMOS A PROBAR TU CONOCIMIENTO SOBRE UNA VARIEDAD DE TEMAS!",
        "* SIMPLEMENTE ESCOGES UNA DIFICULTAD ANTES DE SELECCIONAR TU CUESTIONARIO, Y EMPIEZAS A CONTESTAR LAS PREGUNTAS!",
        "* PERO NO COMETAS MUCHOS ERRORES, POR QUE SI FALLAS MUCHAS PREGUNTAS...",
        "* MORIRAS!!!",
        "* ENTONCES, ¿COMENZAMOS?"
    ];
    
    let currentMessage = 0;
    let typingTimeout; // To track the typing timeout
    const typewriterBox = $("#typewriter-box");
    const skipButton = $('a[class="skip-button"]');
    
    // Initial display
    startTypingEffect(messages[currentMessage]);
    
    // Click handler to cycle through messages
    typewriterBox.on("click", function() {
        // Immediately stop current typing and go to next message
        clearTimeout(typingTimeout);
        goToNextMessage();
    });
    
    // Skip button handler
    skipButton.on("click", function(e) {
        e.preventDefault();
        window.location.href = "selector";
    });
    
    function startTypingEffect(text) {
        typewriterBox.empty();
        let i = 0;
        
        function type() {
            if (i < text.length) {
                typewriterBox.append(text.charAt(i));
                
                i++;
                typingTimeout = setTimeout(type, 30);
            } else {
                // If this was the last message, redirect after delay
                if (currentMessage === messages.length - 1) {
                    setTimeout(function() {
                        window.location.href = "selector";
                    }, 1000);
                }
            }
        }
        
        type();
    }
    
    function goToNextMessage() {
        currentMessage++;
        
        if (currentMessage < messages.length) {
            startTypingEffect(messages[currentMessage]);
        } else {
            // If we've gone past the last message, redirect immediately
            window.location.href = "selector";
        }
    }
});