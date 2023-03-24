const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
const image_input = document.querySelector("#inputImage");
let img = new Image();
image_input.addEventListener("change", function(){
  loadImage();
});


function loadImage() {
  img.onload = function() {
    const width = canvas.width;
    const scaleFactor = width / img.width;
    const height = img.height * scaleFactor;
    canvas.height = height;
    ctx.drawImage(img, 0, 0, width, height);
  };
  img.src = URL.createObjectURL(document.getElementById('inputImage').files[0]);
}

let isDragging = false;
let startX, startY, endX, endY;

canvas.addEventListener('mousedown', function(e) {
  startX = e.offsetX;
  startY = e.offsetY;
  isDragging = true;
});

canvas.addEventListener('mousemove', function(e) {
  if (isDragging) {
    endX = e.offsetX;
    endY = e.offsetY;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(startX, startY, endX - startX, endY - startY);
  }
});

canvas.addEventListener('mouseup', function(e) {
  isDragging = false;
  console.log(`Selected region: (${startX}, ${startY}) - (${endX}, ${endY})`);
  let formData = new FormData();
  formData.append("cropperData", JSON.stringify({
    startX: startX,
    startY: startY,
    endX: endX,
    endY: endY
  }));
  $.ajax({
    type: "POST",
    url: "/activeContour",
    data: formData,
    contentType: "application/json",
    success: function (res) {
      console.log(res);
    }
  })
});
