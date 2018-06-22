setInterval(function() {
  $.get( "status", function( status_data ) {
    var html = ""
    html += "<table>"
    html += "<tr><th>fanID</th><th>state</th><th>ip</th><th>last_ping_date</th></tr>"
    for (var fanID in status_data.online_fans) {
      var fan = status_data.online_fans[fanID];
      var state = fan.state;
      if (state == "idle") {
        state = "loading"
      }
      var colorSquare = '<font color="green">▉</font>'
      if (new Date() - new Date(fan.last_ping_date) > 2000) {
        colorSquare = '<font color="orange">▉</font>'
      }
      if (new Date() - new Date(fan.last_ping_date) > 15000) {
        colorSquare = '<font color="red">▉</font>'
      }

      html += "<tr><td>" + fanID + "</td><td>" + state + "</td><td>" + fan.ip + "</td><td>" + colorSquare + " " + fan.last_ping_date + "</td></tr>"
    }
    html += '<div class="row"> <div class="col-sm-8"> <table>'
    $( ".fans_status" ).html(html);
    
    var html = '<h3>Playlist: </h3> <table style="width:100%">'
    html += '<tr><th>Sequence Name</th><th>Duration</th></tr>'

    html += "Current Animation Starting Time: " + status_data.current_animation_starting_time + "</br>"
    html += "Current Server State: " + status_data.current_server_state + "</br>"

    for (var i=0; i < status_data.playlist.length; i++) {      
      var current = status_data.current_asset_index == i;
      if (current) { html += '<tr style="background-color: lightgreen">' }
      else { html += "<tr>" }
      
      html += "<td>" + status_data.playlist[i].asset + "</td>";
      
      html += "<td>" + status_data.playlist[i].duration + "</td>";
    }
    html += "</table></div></div>";

    $( ".server_status" ).html(html);

  });
}, 1000);

setInterval(function() {
  $.get( "status", function( status_data ) {
    var addressArray = [
     'https://giphy.com/embed/KhdQ2Ia3FJuKs',
     'https://giphy.com/embed/7ovf4vzAh8yoo',
     'https://giphy.com/embed/1Dijze4ok9bbO',
     'https://giphy.com/embed/1045EJrPMmPmaQ',
      'https://giphy.com/embed/SpPwVAdTgC0Za',
    ]
    var randomIndex = Math.floor(Math.random() * addressArray.length);
    var addressToUse = addressArray[randomIndex];
    var gifhtml = '<iframe src='+ addressToUse + ' width="300px" height="300px" frameBorder="0" ></iframe>'
    $( ".gif" ).html(gifhtml);
  });
}, 15000);


function send_command(command) {
  $.get( "server_command?type="+command);
}