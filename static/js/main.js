const imageInput = document.getElementById("input-btn");
const inputImage = document.getElementById("input-img");
const submitBtn = document.getElementById("submit-btn");

let cropper;
let imageFile;

imageInput.addEventListener("change", function (_) {
    const file = imageInput.files[0];
    inputImage.src = URL.createObjectURL(file);
    imageFile = file;
    makeCropper();
});

function makeCropper() {
    cropper = new Cropper(inputImage, {
        aspectRatio: 1,
        viewMode: 1,
        guides: 0,
        dragMode: "move"
    });
}

submitBtn.addEventListener("click", function () {
    sendData();
    sendImageFile(imageFile);
})


function sendData() {
    let formData = new FormData();
    formData.append("cropperData", JSON.stringify(cropper.getData(true)));
    $.ajax({
        type: "POST",
        url: "/data",
        enctype: "multipart/form-data",
        data: formData,
        processData: false,
        contentType: false,
        async: true,
        success: function (res) {

            console.log(res);
        },
    });

}

function sendImageFile(imagefile) {
    let formData = new FormData();
    formData.set("image", imagefile);
    $.ajax({
        type: "POST",
        url: "/activeContour",
        enctype: "multipart/form-data",
        data: formData,
        processData: false,
        contentType: false,
        async: true,
        success: function (res) {
            console.log(res)
        },
    });
}

