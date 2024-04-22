// Code here was made by Emilio for early testings of encryption, not used for our end result of the notes app
document.getElementById("encryptButton").addEventListener("click", function () {
    const messageElement = document.getElementById("message");
    const uidElement = document.getElementById("uid");
    const message = messageElement.textContent;
    const shift = parseInt(uidElement.textContent, 10); // Convert text content to an integer

    // Convert message to ASCII
    const asciiChars = convertToASCII(message);
    const asciiOutputElement = document.getElementById("asciiOutput");
    asciiOutputElement.textContent = "ASCII representation: " + asciiChars.join(", ");

    // Encrypt ASCII message using shift cipher
    const shiftedMessage = shiftCipher(asciiChars, shift); // shift is based on UID
    const shiftOutputElement = document.getElementById("shiftOutput");
    shiftOutputElement.textContent = "Shifted message: " + shiftedMessage.join(", "); // Join shifted array for display
});

// Function to convert message to ASCII characters
function convertToASCII(message) {
    const asciiArray = [];
    for (let i = 0; i < message.length; i++) {
        asciiArray.push(message.charCodeAt(i));
    }
    return asciiArray;
}

// Function to encrypt ASCII using shift cipher
function shiftCipher(message, shift) {
    const shiftedMessage = [];
    for (let i = 0; i < message.length; i++) {
        if (!isNaN(message[i])) {
            shiftedMessage.push(message[i] + shift);
        } else {
            shiftedMessage.push(message[i]);
        }
    }
    return shiftedMessage;
}
