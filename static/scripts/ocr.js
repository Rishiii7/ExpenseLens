let draggableFileArea = document.querySelector(".drag-file-area");
let browseFileText = document.querySelector(".browse-files");
let uploadIcon = document.querySelector(".upload-icon");
let dragDropText = document.querySelector(".dynamic-message");
let fileInput = document.querySelector(".default-file-input");
let uploadedFile = document.querySelector(".file-block");
let fileName = document.querySelector(".file-name");
let fileSize = document.querySelector(".file-size");

fileInput.addEventListener("change", e => {
  uploadIcon.innerHTML = 'check_circle';
  dragDropText.innerHTML = 'File Dropped Successfully!';
  fileName.innerHTML = fileInput.files[0].name;
  fileSize.innerHTML = (fileInput.files[0].size/1024).toFixed(1) + " KB";
  uploadedFile.style.cssText = "display: flex;";
});
