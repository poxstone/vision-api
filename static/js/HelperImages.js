'use strict';

class ImageHelper {
    constructor() {}
    
    static imageToBuffer(fileToLoad) {
        
        return new Promise((resolve, reject) => {
            var reader = new FileReader();
            reader.onload = ((fileToLoad) => (event) => {
                console.log('File_reader_target_bloop: ', event.target.result, 'File_reader_fileToLoad: ', fileToLoad);
                // Send to firebase upload
                var bufferFile = event.target.result;

                resolve(bufferFile);

            })(fileToLoad);
            // excecute
            reader.readAsArrayBuffer(fileToLoad);
        });
    }

    static imageToDataUrl(fileToLoad) {

        return new Promise((resolve, reject) => {
            var reader = new FileReader();
            reader.onload = function(fileRender) {
                var imgDataUrl = fileRender.target.result
                resolve(imgDataUrl);
            }
            reader.readAsDataURL(fileToLoad);
        });
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

    static getImageSheet(fruit_labels=null) {
        return new Promise((resolve, reject) => {
            // Prepare tags
            var tags = '';
            if (fruit_labels && fruit_labels.length){
                for (let indx=0;indx < fruit_labels.length; indx++) {
                    tags += fruit_labels[indx].label + ',';
                }
            }
            tags = tags.replace(/,$/,'');

            // Prepare ajax
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    var response = JSON.parse(this.responseText);
                    console.log(response);
                    resolve(response);
                } else {
                    console.log('backend error', this.status, this.responseText);
                }
            };
            xhttp.open("GET", "/sheet/?fruit_tags=" + tags, true);
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
