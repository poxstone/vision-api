'use strict';

// Initialize Firebase
firebase.initializeApp(FIREBASE_CONFIG);

/*loging*/
function login(event) {
    firebase.auth().signInAnonymously().then((response) => {
        console.log('click_login:', response);
    }).catch((error) => {
        console.log('error_loging: ', error);
    });
}

/*load json ajax*/
function getImageInfo(imageName) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            console.log(response);

            var labels = response.labels;
            var responseStr = '';
            for (let indx=0;indx < response.labels.length; indx++ ) {
                responseStr += `<li><b>${labels[indx].label}</b>: ${labels[indx].score}% </li>`;
            }

            document.getElementById("result").innerHTML = `<ul>${responseStr}</ul>`;
        }
    };
    xhttp.open("GET", "/get-image/" + imageName, true);
    xhttp.send();
}


/*STORAGE*/
var storageRef = firebase.storage().ref();
var imagesRef = storageRef.child(BUCKET_DIR);

function uploadImage(file, fileName) {
    var storageRef = firebase.storage().ref();
    var mountainImagesRef = storageRef.child(BUCKET_DIR + '/' + fileName);
    console.log(mountainImagesRef.fullPath);

    mountainImagesRef.put(file).then(function(snapshot) {
        console.log('Uploaded_a_blob_or_file:', snapshot);
        getImageInfo(fileName);
    });
}

// Load files
function handleFileSelect(evt) {
    var files = evt.target.files;
    for (let i = 0, fileToLoad; fileToLoad = files[i]; i++) {
        console.log('File_to_read', fileToLoad);

        var reader = new FileReader();
        reader.onload = ((fileLoaded) => (event) => {
            console.log('File_reader_target_bloop: ', event.target.result, 'File_reader_fileLoaded: ', fileLoaded);
            uploadImage(event.target.result, fileToLoad.name);

        })(fileToLoad);

        reader.readAsArrayBuffer(fileToLoad);
    }
}

// camera
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


function takePicture() {
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var video = document.getElementById('video');
	context.drawImage(video, 0, 0, 640, 480);
	var jpegUrl = canvas.toDataURL("image/jpeg");
	console.log("Hola", jpegUrl);

};
