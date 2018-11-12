'use strict';
(function(){
    // @import constanst.js
    // @import HelperImages.js

    window.loadApp = function() {
        // Initialize Firebase
        firebase.initializeApp(FIREBASE_CONFIG);
        /*Storeage config*/
        var storageRef = firebase.storage().ref();
        var imagesRef = storageRef.child(BUCKET_DIR);
        
        // INPUT LOAD FUNCTION
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

})();