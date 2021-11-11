const api_key = "AIzaSyA4e_3-TfKWc1UZSBbJJyUbeJV_Ql8Nv_s";

var video_id = "";
var generating = false;

// https://stackoverflow.com/questions/14934089/convert-iso-8601-duration-with-javascript
// from Luke Stevenson
function parseDurationString( durationString ){
    var stringPattern = /^PT(?:(\d+)D)?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d{1,3})?)S)?$/;
    var stringParts = stringPattern.exec( durationString );
    return (
             (
               (
                 ( stringParts[1] === undefined ? 0 : stringParts[1]*1 )  /* Days */
                 * 24 + ( stringParts[2] === undefined ? 0 : stringParts[2]*1 ) /* Hours */
               )
               * 60 + ( stringParts[3] === undefined ? 0 : stringParts[3]*1 ) /* Minutes */
             )
             * 60 + ( stringParts[4] === undefined ? 0 : stringParts[4]*1 ) /* Seconds */
           );
}


function get_youtube_details(url) {

  if (result = url.match(/youtube\.com.*(\?v=|\/embed\/)(.{11})/)) {

    const vid_id = result.pop();
    video_id = vid_id;
    const endpoint =  "https://www.googleapis.com/youtube/v3/videos?part=snippet&id=" +
              vid_id + "&key=" + api_key + "&part=contentDetails";
    var abcd = $.getJSON(endpoint)
      .done(function(data) {
        console.log(data);
        var title = data.items[0].snippet.title;
        var description = data.items[0].snippet.description;
        var channel = data.items[0].snippet.channelTitle;
        var duration = parseDurationString(data.items[0].contentDetails.duration);
        $("#vid-title").text(title);
        $("#vid-description").text(description);
        document.getElementById('vid-duration').value = duration;
        document.getElementById("currentvid").src = data.items[0].snippet.thumbnails.high.url;
        document.getElementById("seconds-per-sample").value = duration / 720;
        $("#video-info").css("display", "inline-block");
      })
      .fail(function() {
        alert("Couldn't get information from youtube.");
        $("#video-info").css("display", "none");
        $("#generate-info").css("display", "none");
      });
  } else {
    alert("Couldn't locate a video at that location.");
    $("#video-info").css("display", "none");
  }

}
https://www.youtube.com/watch?v=SRWrQMwGYsQ
function update_video_thumbnail() {
  //var thumbnail = document.getElementById("currentvid");
  var linkbox = document.getElementById("linkbox");
  //thumbnail.src = get_youtube_thumbnail(linkbox.value, 'high');
  get_youtube_details(linkbox.value);
}


function genImage() {

  if (!generating) {

    generating = true;

    $("#final-img-div").css("display", "inline-block");
    $("#loader").css("display", "block");
    console.log("Displaying final div");

    const url = "http://0.0.0.0:5000/get_image?vid_id=" + video_id +
    "&total_samples=" + document.getElementById("totalsamples").value +
    "&title=" + document.getElementById("vid-title").textContent;
    $.ajax({
      url: url,
      type: 'post',
      success: function (resp) {
        console.log(resp);
        console.log("/static/img/"+resp);
        document.getElementById("final_img").src='/static/img/'+resp;
        $("#loader").css("display", "none");
        $("#final_img").css("display", "block");
        generating = false;
      },
      error: function() {
        console.log("Gen Image Error");
        $("#loader").css("display", "none");
        generating = false;
      }
    });
  }




}

