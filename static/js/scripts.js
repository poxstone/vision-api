'use strict';
(function(){
// @import constanst.js
// @import HelperImages.js

    // Initialize Firebase
    firebase.initializeApp(FIREBASE_CONFIG);
    /*Storeage config*/
    var storageRef = firebase.storage().ref();
    var imagesRef = storageRef.child(BUCKET_DIR);
    
    var APP = new Vue({
        el: '#app',
        data: {
            fruitName: ''
        }
    })

    // INPUT LOAD FUNCTION
    document.querySelector('#UPLOAD_FILE').addEventListener('change', (event) => {
        const ELEMENT_INFO = document.querySelector('#IMG_INFO');
        const ELEMENT_TAGS = document.querySelector('#IMG_TAGS');
        const IMG_PREVIEW = document.querySelector('#IMG_UPLOADED');
        const IMG_NAME = document.querySelector('#IMG_NAME'); 
        const IMG_TITLE = document.querySelector('#IMG_TITLE_CONT'); 
        const BODY_ELEMENT = document.querySelector('html > body');
        const EMPTY_CLASS = 'data-empty';
        var fileToLoad = event.target.files[0];
        var fileName = fileToLoad.name;

        // render image
        ImageHelper.imageToDataUrl(fileToLoad).then((imgDataUrl) => {
            console.log('image to render: ', fileName, imgDataUrl);
            IMG_PREVIEW.setAttribute('src', imgDataUrl);
            APP.$data.fruitName = fileName;
            BODY_ELEMENT.classList.remove(EMPTY_CLASS);

            // Clear Divs
            ELEMENT_INFO.innerHTML = '';
            ELEMENT_TAGS.innerHTML = '';
        });

        // Upload pipe
        ImageHelper.imageToBuffer(fileToLoad).then((bufferFile) => {

            FirebaseStorage.uploadImage(bufferFile, fileName).then( (snapshot) => {

                console.log('info_Uploaded_a_blob_or_file:', snapshot);
                
                EndpointsImage.getImageInfo(fileName).then((imageInfoData) => {
                    var labels = imageInfoData.labels;
                    var colors = imageInfoData.colors;

                    var responseStr = '';
                    for (let indx=0;indx < imageInfoData.labels.length; indx++ ) {
                        responseStr += `<li class="item">
                                <b class="i-key">${labels[indx].label}</b>
                                <i class="i-value">${labels[indx].score}%</i>
                            </li>`;
                    }

                    ELEMENT_TAGS.innerHTML = `${responseStr}`;
                    
                    EndpointsImage.getImageSheet(labels).then((imageNutriData) => {
                        console.log(imageNutriData);
                        var rows = imageNutriData;

                        if (!rows.length || !rows[0].length || !rows[1].length) {
                            alert('No se encontraron resultados');
                            return false;
                        }
                        
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
                        ELEMENT_INFO.innerHTML = `${responseStr}`;
                        APP.$data.fruitName = values[1];

                        
                    })
                });
            });
        });
    });

})();