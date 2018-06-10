var save = false;

var canvas, ctx, myImageData;
var targetImageColumns = 400;
var output_div;

function downloadURI(uri, name) {
  var link = document.createElement("a");
  link.download = name;
  link.href = uri;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  delete link;
}

var img = new Image();
var images_queue = [];

function load_next() {
  var next_image = images_queue.pop();
  if (next_image) {
    img.src = next_image[1];
    img.setAttribute("id", next_image[0]);
  } else {
    toggleInputsDisabled(false);
  }
}

img.onload = function() {
  // canvas2 = document.getElementById('canvas2');
  var canvas2 = document.createElement("canvas");
  canvas2.setAttribute("width", 400);
  canvas2.setAttribute("height", 144);
  canvas2.setAttribute("id", img.getAttribute("id"));

  output_div.appendChild(canvas2);
  var res_ctx = canvas2.getContext("2d");

  ctx.drawImage(img, 0, 0);
  img.style.display = "none";
  var img_data = ctx.getImageData(0, 0, img.width, img.height).data;

  var imageDiameter = img.width;
  var target_imageDiameter = 144;
  myImageData = res_ctx.createImageData(
    targetImageColumns,
    target_imageDiameter
  );
  var new_data = myImageData.data;
  var theta = 0;
  var theta_increment = 2 * Math.PI / targetImageColumns;
  for (var j = 0; j < targetImageColumns; j++) {
    var dx = Math.cos(theta);
    var dy = Math.sin(theta);
    var dd = imageDiameter / target_imageDiameter;

    for (var k = 0; k < target_imageDiameter; k++) {
      var xk = dd * (-target_imageDiameter / 2 + k) * dx + img.width / 2;
      var yk = dd * (-target_imageDiameter / 2 + k) * dy + img.height / 2;

      if (xk > img.width || yk > img.height || xk < 0 || yk < 0) {
        console.error("Assert: Trying to sample pixels out of image");
      }

      var cur_data = ctx.getImageData(xk, yk, 1, 1).data;
      new_data[4 * (k * targetImageColumns + j)] = cur_data[0];
      new_data[4 * (k * targetImageColumns + j) + 1] = cur_data[1]; // green
      new_data[4 * (k * targetImageColumns + j) + 2] = cur_data[2]; // blue
      new_data[4 * (k * targetImageColumns + j) + 3] = cur_data[3]; // alpha
    }
    theta += theta_increment;
  }

  res_ctx.putImageData(myImageData, 0, 0);

  load_next();
};

var sem = 0;
function handleFileSelect(evt) {
  toggleInputsDisabled(true);

  var files = evt.target.files; // FileList object
  const $thumbList = $("#list");
  $thumbList.empty();
  // Loop through the FileList and render image files as thumbnails.
  for (var i = 0, f; (f = files[i]); i++) {
    // Only process image files.
    if (!f.type.match("image.*")) {
      continue;
    }

    var reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function(theFile) {
      return function(e) {
        images_queue.push([theFile.name, e.target.result]);
        // Render thumbnail.
        var span = document.createElement("span");
        span.innerHTML = [
          '<img class="thumb" src="',
          e.target.result,
          '" title="',
          escape(theFile.name),
          '"/>'
        ].join("");
        $thumbList.append(span, null);

        sem--;
        if (sem == 0) {
          load_next();
        }
      };
    })(f);

    // Read in the image file as a data URL.
    reader.readAsDataURL(f);
    sem++;
  }
}

function generate_zip(callback) {
  var zip = new JSZip();
  var images = output_div.children;

  for (var i = 0; i < images.length; i++) {
    zip.file(
      images[i].getAttribute("id"),
      images[i].toDataURL("image/png").substr(22),
      { base64: true }
    );
  }

  zip.generateAsync({ type: "blob" }).then(callback);
}

function download_zip() {
  generate_zip(function(content) {
    var link = document.createElement("a");
    link.download = "sequence.zip";
    link.href = window.URL.createObjectURL(content);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
  });
}

function appendConverterDomElements() {
  const $thumbList = $("#list").empty();
  const $converterContainer = $(".converter-dom-elements-container");
  $converterContainer.empty();
  const domElement = $.parseHTML(`
      <div style="display:block; width: 40%">
        <p>Input: (Recommended size 400x400)</p>
        <canvas id="canvas" width="400" height="400"></canvas>
      </div>
      <div style="display:inline-block; width: 40%">
        <p>Output</p>
        <div id="image-output"></div>
      </div>
    `);
  $converterContainer.append(domElement);
}

function initConverter() {
  appendConverterDomElements();

  document
    .getElementById("files")
    .addEventListener("change", handleFileSelect, false);

  // var file_name = "cube020.png";
  // img.src = './cube/' + file_name;
  canvas = document.getElementById("canvas");
  ctx = canvas.getContext("2d");
  output_div = document.getElementById("image-output");
}
