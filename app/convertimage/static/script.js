
// Make sure 3 or more images are selected
const FILES = document.querySelector("#id_images");
if (FILES != null) {
    FILES.addEventListener('change', (event) => {
        let numberFiles = FILES.files.length;
        const submitbutton = document.querySelector("#add-image-button");
        const submiterrormsg = document.querySelector("#add-image-error-message");
        if (numberFiles > 0 && numberFiles < 3) {
            submitbutton.disabled = true;
            submitbutton.classList.add("disabled");
            submiterrormsg.classList.remove("d-none");
            submiterrormsg.innerHTML = "Select 3 or more images!"
        } else {
            submitbutton.disabled = false;
            submitbutton.classList.remove("disabled");
            submiterrormsg.classList.add("d-none");
        }
    });
}
