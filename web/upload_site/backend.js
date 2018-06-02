const storageService = firebase.storage();
const database = firebase.database();
const db = database.ref("fugara-revelations");
const storageRef = storageService.ref();
const $fileNameStatus = $(".file-name-status");
const $progressStatus = $(".progress-status");

document
  .querySelector(".file-select")
  .addEventListener("change", handleFileUploadChange);
document
  .querySelector(".file-submit")
  .addEventListener("click", handleFileUploadSubmit);

let selectedFiles;
function handleFileUploadChange(e) {
  selectedFiles = e.target.files;
}

function handleFileUploadSubmit(e) {
  const $email = $(".email-field");
  if (!$email.val()) {
    alert("הכנס כתובת אי מייל");
    return;
  }
  for (var i = 0; i < selectedFiles.length; i++) {
    uploadOneFile($email.val(), selectedFiles[i]);
  }
}

function uploadOneFile(folder, file) {
  folder = folder.replace(/\./g, "-dot-");
  const path = `${folder}/${file.name}`;
  console.log(path);
  const uploadTask = storageRef.child(path).put(file); //create a child directory called images, and place the file inside this directory
  $fileNameStatus.html(`טוען את קובץ: ${file.name}`);
  uploadTask.on(
    "state_changed",
    snapshot => {
      console.log("state_changed...");
      $progressStatus.html(
        `${100 *
          Math.floor(snapshot.bytesTransferred / snapshot.totalBytes)}% נטען`
      );
      // Observe state change events such as progress, pause, and resume
    },
    error => {
      // Handle unsuccessful uploads
      console.log(error);
      $fileNameStatus.html(
        `פישלנו.. משהו לא עובד.... הפאק הזה עלינו אז תודיעו לנו בבקשה :)`
      );
    },
    () => {
      // Do something once upload is complete
      writeUserData(folder, file.name);
      $fileNameStatus.html(`בום! סיימנו!`);
      console.log("success");
    }
  );
}

function writeUserData(folder, fileName) {
  db.once("value").then(function(snapshot) {
    const fileStructure = snapshot.toJSON();
    const newFileStrocture = Object.assign({}, fileStructure, {
      [folder]: folder
    });
    db.set(newFileStrocture);
  });
}
