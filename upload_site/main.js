/** Drag and Drop **/
function dragHover(e) {
  e.stopPropagation();
  e.preventDefault();

  if (e.type === "dragover") {
    e.target.className = "over";
  } else {
    e.target.className = "";
  }
}

// document.getElementById("dropDiv").addEventListener("dragover", dragHover);
// document.getElementById("dropDiv").addEventListener("dragleave", dragHover);
// document.getElementById("dropDiv").addEventListener("drop", function(e) {
//   event.preventDefault();

//   var items = event.dataTransfer.items;
//   for (var i = 0; i < items.length; i++) {
//     // webkitGetAsEntry is where the magic happens
//     var item = items[i].webkitGetAsEntry();
//     if (item) {
//       traverseFileTree(item);
//     }
//   }
// });

function traverseFileTree(item, path) {
  path = path || "";
  if (item.isFile) {
    // Get file
    item.file(function(file) {
      console.log("File:", path + file.name);
    });
  } else if (item.isDirectory) {
    // Get folder contents
    var dirReader = item.createReader();
    dirReader.readEntries(function(entries) {
      for (var i = 0; i < entries.length; i++) {
        traverseFileTree(entries[i], path + item.name + "/");
      }
    });
  }
}
