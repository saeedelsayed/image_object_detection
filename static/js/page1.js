const canvas = document.getElementById('myCanvas');
const ctx = canvas.getContext('2d');
let img = new Image();

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
});