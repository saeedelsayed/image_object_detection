const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
let img = new Image();

function loadImage() {
  img.onload = function() {
    ctx.drawImage(img, 0, 0);
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
    ctx.drawImage(img, 0, 0);
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(startX, startY, endX - startX, endY - startY);
  }
});

canvas.addEventListener('mouseup', function(e) {
  isDragging = false;
  console.log(`Selected region: (${startX}, ${startY}) - (${endX}, ${endY})`);
<<<<<<< Updated upstream:static/js/page1.js
});
=======

  let formData = new FormData();
  formData.append("startX",startX.toString());
  formData.append("startY",startY.toString());
  formData.append("endX",endX.toString());
  formData.append("endY",endY.toString());
  console.log
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
>>>>>>> Stashed changes:static/js/contourPage.js
