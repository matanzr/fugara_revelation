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
      html += "<tr><td>" + fanID + "</td><td>" + state + "</td><td>" + fan.ip + "</td><td>" + fan.last_ping_date + "</td></tr>"
    }
    html += "</table>"
    $( ".fans_status" ).html(html);

    var html = "Playlist: " + JSON.stringify(status_data.playlist) + "</br>"
    html += "Current Asset: " + status_data.playlist[status_data.current_asset_index].asset + "</br>"
    html += "Current Animation Starting Time: " + status_data.current_animation_starting_time + "</br>"
    html += "Current Server State: " + status_data.current_server_state + "</br>"

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
