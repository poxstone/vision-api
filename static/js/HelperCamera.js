'use strict';
class CameraHelper {
    constructor() {}

    cameraStart () {
        var video = document.getElementById('video');
        // Get access to the camera!
        if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Not adding `{ audio: true }` since we only want video now
        navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        
            try {
            video.srcObject = stream;
            } catch (error) {
            video.src = window.URL.createObjectURL(stream);
            }
        
            video.play();
        });
        }
    }

    takePicture() {
        var canvas = document.getElementById('canvas');
        var context = canvas.getContext('2d');
        var video = document.getElementById('video');
        context.drawImage(video, 0, 0, 640, 480);
        var jpegUrl = canvas.toDataURL("image/jpeg");
        console.log("Hola", jpegUrl);

    };
}
