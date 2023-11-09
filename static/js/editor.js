const toolList = document.querySelector("#tool");
const optionList = document.querySelectorAll(".option");

function selectTool() {
  let preSelect = document.querySelector(".selected");
  preSelect.classList.remove("selected");
  this.classList.add("selected");

  let preOpt = document.querySelector(".select");
  console.log(preOpt);
  if (preOpt != null) {
    preOpt.classList.remove("select");
  }
  let curopt = this.getAttribute("id") + "Option";
  let curoptDom = document.querySelector(`#${curopt}`);
  if (curoptDom != null) {
    curoptDom.classList.add("select");
  }
}
for (let i = 0; i < toolList.childElementCount; i++) {
  toolList.children[i].addEventListener("click", selectTool);
}

var inputFile = document.querySelector("#inputFile");
var inputUrl = document.querySelector("#inputUrl");
var URLbutton = document.querySelector("#URLbutton");
var upload = document.querySelector("#upload");
var editor = document.querySelector("#editor");

function checkimg(file) {
  var ext = /(.*?)\.(jpg|jpeg|png|gif|bmp)$/;
  if (file.match(ext)) {
    return true;
  } else {
    return false;
  }
}
function checkvalid(src, callback) {
  const img = new Image();
  img.src = src;
  img.onload = function() {
    callback(true);
  }
  img.onerror = function() {
    callback(false);
  }
}
function urlEdit() {
  var value = inputUrl.value;
  checkvalid(value, function(isValid) {
    if (isValid) {
      upload.classList.remove("activate");
      upload.classList.add("hidden");
      editor.classList.remove("hidden");
      editor.classList.add("activate");
    } else {
      alert("이미지 파일이 아닙니다");
    }
  });
}
function fileEdit() {
  if (inputFile.files && inputFile.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      var dataURL = e.target.result;
      checkvalid(dataURL, function(isValid) {
        if (isValid) {
          upload.classList.remove("activate");
          upload.classList.add("hidden");
          editor.classList.remove("hidden");
          editor.classList.add("activate");
        } else {
          alert("이미지 파일이 아닙니다");
        }
      });
    };
    reader.readAsDataURL(inputFile.files[0]);
  }
}
var closeButton = document.querySelector("#close");
function close() {
  editor.classList.remove("activate");
  editor.classList.add("hidden");
  upload.classList.remove("hidden");
  upload.classList.add("activate");
  document.querySelector(".select").classList.remove("select");
  inputUrl.value="";
}
URLbutton.addEventListener("click", urlEdit);
inputFile.addEventListener("change", fileEdit);
closeButton.addEventListener("click", close);
