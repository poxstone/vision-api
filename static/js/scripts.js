'use strict';
(function(){
    // @import constanst.js

    window.loadApp = function() {
        // Initialize Firebase
        firebase.initializeApp(FIREBASE_CONFIG);
        /*Storeage config*/
        var storageRef = firebase.storage().ref();
        var imagesRef = storageRef.child(BUCKET_DIR);
        
        // add Event to upload button
        document.querySelector('#UPLOAD_FILE').addEventListener('change', (event) => {
            var imageHelper = new ImageHelper();
            var pasteSelector = '#RESULT';
            // Upload pipe
            ImageHelper.prepareImage(event).then((inputFile, fileName) => {

                FirebaseStorage.uploadImage(inputFile, fileName).then( (snapshot) => {

                    console.log('info_Uploaded_a_blob_or_file:', snapshot);
                    
                    EndpointsImage.getImageInfo(fileName).then((imageInfoData) => {
                        var labels = imageInfoData.labels;
                        var responseStr = '';

                        for (let indx=0;indx < imageInfoData.labels.length; indx++ ) {
                            responseStr += `<li><b>${labels[indx].label}</b>: ${labels[indx].score}% </li>`;
                        }

                        document.querySelector(pasteSelector).innerHTML = `<ul>${responseStr}</ul>`;
                    });
                });
            });
        });
    };

    class ImageHelper {

        constructor() {}
        
        static prepareImage(inputEvent) {
            var files = inputEvent.target.files;
            
            return new Promise((resolve, reject) => {
                for (let i = 0, fileToLoad; fileToLoad = files[i]; i++) {
                    console.log('File_to_read', fileToLoad);
    
                    var reader = new FileReader();
                    reader.onload = ((fileLoaded) => (event) => {
                        console.log('File_reader_target_bloop: ', event.target.result, 'File_reader_fileLoaded: ', fileLoaded);
                        // Send to firebase upload
                        var fileName = fileToLoad.name;
                        var inputFile = event.target.result;

                        resolve(inputFile, fileName);
    
                    })(fileToLoad);
                    // excecute
                    reader.readAsArrayBuffer(fileToLoad);
                }
            })

        }
    }

    class FirebaseLoging {
        constructor() {}

        static login (event) {
            firebase.auth().signInAnonymously().then((response) => {
                console.log('click_login:', response);
            }).catch((error) => {
                console.log('error_loging: ', error);
            });
        }
    }
    
    class EndpointsImage {
        constructor() {}

        static getImageInfo(imageName) {
            return new Promise((resolve, reject) => {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = function() {
                    if (this.readyState == 4 && this.status == 200) {
                        var response = JSON.parse(this.responseText);
                        console.log(response);
                        resolve(response);
                    }
                };
                xhttp.open("GET", "/get-image/" + imageName, true);
                // excecute
                xhttp.send(); 
            });            
        }
    }

    class FirebaseStorage {
        constructor() {}

        static uploadImage(inputFile, fileName) {
            var storageRef = firebase.storage().ref();
            var mountainImagesRef = storageRef.child(BUCKET_DIR + '/' + fileName);
            console.log(mountainImagesRef.fullPath);
            // Upload to firebase promise
            return mountainImagesRef.put(inputFile);
        }
    }

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
    

})();