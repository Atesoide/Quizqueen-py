$(document).ready(function() {
    const messages = [
        {
            text: "¿Estás listo para poner a prueba tus conocimientos en una divertida trivia?",
            mascota: "tortugaIntro_1.png"
        },
        {
            text: "Selecciona una dificultad y comienza a jugar",
            mascota: "tortugaIntro_2.png"
        },
        {
            text: "Recuerda no cometer demasiados errores, podrías quedarte sin oportunidades para responder",
            mascota: "tortugaIntro_1.png"
        },
        {
            text: "¡Buena suerte!",
            mascota: "tortugaIntro_2.png"
        }
    ];
    
    let currentMessage = 0;
    let typingTimeout;
    const typewriterBox = $("#typewriter-box");
    const skipButton = $('a[class="skip-button"]');
    
    // Initial display
    startTypingEffect(messages[currentMessage]);
    
    // Click handler to cycle through messages
    typewriterBox.on("click", function() {
        clearTimeout(typingTimeout);
        goToNextMessage();
    });
    
    // Skip button handler
    skipButton.on("click", function(e) {
        e.preventDefault();
        window.location.href = "selector";
    });
    
    function startTypingEffect(messageObj) {
        typewriterBox.empty();
        
        // Cambiar la mascota
        cambiarMascotaIntro(messageObj.mascota);
        
        let i = 0;
        const text = messageObj.text;
        
        function type() {
            if (i < text.length) {
                typewriterBox.append(text.charAt(i));
                i++;
                typingTimeout = setTimeout(type, 30);
            } else {
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
            window.location.href = "selector";
        }
    }
});