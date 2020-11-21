const FILESELECTED = document.querySelector("#id_images").files;
const FILES = document.querySelector("#id_images");
const SUBMITBUTTON = document.querySelector("#add-image-button");
const SUBMITERRORMSG = document.querySelector("#add-image-error-message");

// Make sure 3 or more images are selected
FILES.addEventListener('change', (event) => {
    if (FILESELECTED.length > 0 && FILESELECTED.length < 3) {
        SUBMITBUTTON.disabled = true;
        SUBMITBUTTON.classList.add("disabled");
        SUBMITERRORMSG.classList.remove("d-none");
        SUBMITERRORMSG.innerHTML = "Select 3 or more images!"
    } else {
        SUBMITBUTTON.disabled = false;
        SUBMITBUTTON.classList.remove("disabled");
        SUBMITERRORMSG.classList.add("d-none");
    }
});