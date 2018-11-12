'use strict';

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
