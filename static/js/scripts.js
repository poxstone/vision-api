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
            const ELEMENT_INFO = '#IMG_INFO';
            const ELEMENT_TAGS = '#IMG_TAGS';
            const IMG_PREVIEW = '#IMG_UPLOADED';
            var fileToLoad = event.target.files[0];
            var fileName = fileToLoad.name;

            // render image
            ImageHelper.imageToDataUrl(fileToLoad).then((imgDataUrl) => {
                console.log('image to render: ', fileName, imgDataUrl);
                document.querySelector(IMG_PREVIEW).setAttribute('src', imgDataUrl);
            });

            // Upload pipe
            ImageHelper.imageToBuffer(fileToLoad).then((bufferFile) => {

                FirebaseStorage.uploadImage(bufferFile).then( (snapshot) => {

                    console.log('info_Uploaded_a_blob_or_file:', snapshot);
                    
                    EndpointsImage.getImageInfo(fileName).then((imageInfoData) => {
                        var labels = imageInfoData.labels;

                        var responseStr = '';
                        for (let indx=0;indx < imageInfoData.labels.length; indx++ ) {
                            responseStr += `<li class="item">
                                    <b class="i-key">${labels[indx].label}</b>
                                    <i class="i-value">${labels[indx].score}%</i>
                                </li>`;
                        }

                        document.querySelector(ELEMENT_TAGS).innerHTML = `${responseStr}`;
                        
                        EndpointsImage.getImageSheet().then((imageNutriData) => {
                            console.log(imageNutriData);
                            var rows = imageNutriData.values;
                            var titles = rows[0];
                            var values = rows[1];
                            
                            var responseStr = '';
                            for (let indx=0;indx < titles.length; indx++ ) {
                                var title = titles[indx];
                                var value = values[indx];
                                responseStr += `<li class="item">
                                        <b class="i-key">${title}</b>
                                        <i class="i-value">${value}</i>
                                    </li>`;
                            }
                            document.querySelector(ELEMENT_INFO).innerHTML = `${responseStr}`;
                        })
                    });
                });
            });
        });
    };

})();