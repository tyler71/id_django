const FILESELECTED = document.querySelector("#id_images").files;
const FILES = document.querySelector("#id_images");
const SUBMITBUTTON = document.querySelector();

FILES.addEventListener('change', (event) => {
    if (FILESELECTED > 0 && FILESELECTED < 4) {
        console.log("no good!")
    }
});