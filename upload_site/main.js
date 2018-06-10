window.onload = function() {
  initConverter();
  toggleInputsDisabled(false);
};

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

function toggleInputsDisabled(bool) {
  const $inputs = $("input, button");
  const $loader = $(".loader");
  console.log(`$inputs: ${JSON.stringify($inputs)}`);
  $inputs.attr("disabled", bool);
  $loader[bool ? "show" : "hide"]();
}
