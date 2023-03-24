const image_input = document.getElementById("image_input");
const submit_btn = document.getElementById("submit-btn");
var uploaded_image = "";

submit_btn.addEventListener("click", function(){
    const formData = new FormData();
    formData.append("image", uploaded_image);
    $.ajax({
        type: "POST",
        url: "/hough",
        enctype: "multipart/form-data",
        data: formData,
        processData: false,
        contentType: false,
        async: true,
        success: function (res) {
            console.log(res);
        },
    });
});

image_input.addEventListener("change", function(){
    const reader = new FileReader();
    reader.addEventListener("load", ()=> {
        uploaded_image = reader.result;
        document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`;
    });
    reader.readAsDataURL(this.files[0]);
    
    const display_image = document.querySelector("#display_image");
    const img = new Image();
    img.onload = function() {
      const width = display_image.width;
      const scaleFactor = width / img.width;
      const height = img.height * scaleFactor;
      display_image.height = height;
      display_image.style.backgroundSize = "100% 100%";
    };
    img.src = URL.createObjectURL(this.files[0]);
})



// Get the button element
var dropdown = document.getElementsByClassName("dropbtn")[0];

// Get all options inside the dropdown
var options = document.getElementsByClassName("dropdown-content")[0].getElementsByTagName("a");

// Add click event listener to each option
for (var i = 0; i < options.length; i++) {
  options[i].addEventListener("click", function() {
  console.log(this.innerHTML);
  option = this.innerHTML;
  });
}