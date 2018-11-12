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
            var imageHelper = new ImageHelper('#RESULT');
            imageHelper.onSelectImage(event);
        });
    }

    class ImageHelper {

        constructor(strPasteCssSelector) {
            this.pasteSelector = strPasteCssSelector;
        }
        
        onSelectImage(inputEvent) {
            var self = this;
            var files = inputEvent.target.files;
            for (let i = 0, fileToLoad; fileToLoad = files[i]; i++) {
                console.log('File_to_read', fileToLoad);

                var reader = new FileReader();
                reader.onload = ((fileLoaded) => (event) => {
                    console.log('File_reader_target_bloop: ', event.target.result, 'File_reader_fileLoaded: ', fileLoaded);
                    // Send to firebase upload
                    var fileName = fileToLoad.name;
                    var inputFile = event.target.result;
                    FirebaseStorage.uploadImage(inputFile, fileName, (snapshot) => {
                        console.log('Uploaded_a_blob_or_file:', snapshot);
                        EndpointsImage.getImageInfo(fileName, (response) => {
                            self.printImageInfo(response, self.pasteSelector)
                        });
                    });

                })(fileToLoad);
                // excecute
                reader.readAsArrayBuffer(fileToLoad);
            }
        }

        printImageInfo(imageInfoData, pasteSelector) {
            var labels = imageInfoData.labels;
            var responseStr = '';

            for (let indx=0;indx < imageInfoData.labels.length; indx++ ) {
                responseStr += `<li><b>${labels[indx].label}</b>: ${labels[indx].score}% </li>`;
            }

            document.querySelector(pasteSelector).innerHTML = `<ul>${responseStr}</ul>`;
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

        static getImageInfo(imageName, callBack) {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var response = JSON.parse(this.responseText);
                    console.log(response);
                    callBack(response);
                }
            };
            xhttp.open("GET", "/get-image/" + imageName, true);
            // excecute
            xhttp.send();
        }
    }

    class FirebaseStorage {
        constructor() {}

        static uploadImage(inputFile, fileName, callBack) {
            var storageRef = firebase.storage().ref();
            var mountainImagesRef = storageRef.child(BUCKET_DIR + '/' + fileName);
            console.log(mountainImagesRef.fullPath);
            // Upload to firebase 
            mountainImagesRef.put(inputFile).then(callBack);
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