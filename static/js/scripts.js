'use strict';
(function(){
// @import constanst.js
// @import HelperImages.js

    // Initialize Firebase
    firebase.initializeApp(FIREBASE_CONFIG);
    /*Storeage config*/
    var storageRef = firebase.storage().ref();
    var imagesRef = storageRef.child(BUCKET_DIR);

    // vue js
    window.APP = new Vue({
        el: '#app',
        data: {
            fruitName: '',
            isDataEmpty: true,
            isImageReaded: false,
            menuToShow: 0,
            nutriList: [],
            tagsList: [],
            colorList: [],
            imgFruitSrc: ''
        },
        methods: {
            loadImage: function(event) {loadImage(event)},
            showMenu: function(tabNumber) {this.menuToShow = tabNumber;}
        },
        watch: {
            tagsList: function(newTagsList, oldTagsList) {
                this.isDataEmpty = newTagsList && newTagsList.length ? false : true;
            },
            imgFruitSrc: function(newImageSrc, oldImageSrc) {
                this.isImageReaded = newImageSrc ? true : false;
            }
        }
    })

    // INPUT LOAD FUNCTION
    function loadImage(event) {
        var fileToLoad = event.target.files[0];
        var fileName = fileToLoad.name;
        APP.$data.fruitName = fileName;

        // render image
        ImageHelper.imageToDataUrl(fileToLoad).then((imgDataUrl) => {
            console.log('image to render: ', fileName, imgDataUrl);
            clearData();
            APP.$data.imgFruitSrc = imgDataUrl;
        });

        // Upload pipe
        ImageHelper.imageToBuffer(fileToLoad).then((bufferFile) => {

            FirebaseStorage.uploadImage(bufferFile, fileName).then( (snapshot) => {

                console.log('info_Uploaded_a_blob_or_file:', snapshot);
                
                EndpointsImage.getImageInfo(fileName).then((imageInfoData) => {
                    var labels = imageInfoData.labels;
                    var colors = imageInfoData.colors;

                    var tagsList = [];
                    for (let indx=0;indx < imageInfoData.labels.length; indx++ ) {
                        tagsList.push({
                            title: labels[indx].label,
                            value: labels[indx].score
                        });
                    }

                    APP.$data.tagsList = tagsList;
                    APP.$data.colorList = colors;
                    
                    EndpointsImage.getImageSheet(labels).then((nutriData) => {
                        console.log(nutriData);
                        if (nutriData.length) {
                            nutriData =   [{
                                title: 'No se encontraron resultados en la hoja de clculo',
                                value:''
                            }];
                        }
                       
                        APP.$data.nutriList = nutriData;
                        APP.$data.fruitName = values[1];
                        
                    })
                });
            });
        });
    };

    function clearData() {
        APP.$data.nutriList = [];
        APP.$data.tagsList = [];
        APP.$data.colorList = [];
        APP.$data.imgFruitSrc = '';
        APP.$data.menuToShow = 0;
    }

})();