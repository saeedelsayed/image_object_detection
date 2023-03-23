const image_input = document.querySelector("#image_input");
var uploaded_image = "";

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
alert(this.innerHTML);
});
}