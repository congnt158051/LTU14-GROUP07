$(document).ready(function () {
 
    $("#btnSubmit").click(function (event) {
 
        //stop submit the form, we will post it manually.
        var file = $('#img_file').get(0).files[0]
        var formData = new FormData();
        formData.append('img_file', file);
        $("#btnSubmit").prop("disabled", true);
        $.ajax({
            type: "POST",
            mimeType: 'multipart/form-data',
            url: document.getElementById('myform').action,
            data: formData,
            processData: false,
            contentType: false,
            async: true,
            crossDomain: true,
            success: function (data) {
                console.log("SUCCESS : ", data);
                var img = document.getElementById("image");
                // var ctx = c.getContext("2d");
                var width = img.width;
                var height = img.height
                var d = JSON.parse(data)
                d.detection.map(function (id) {
                    var d = document.getElementById("myCanvas");
                    var dtx = d.getContext("2d");
                    var left = (id.xmin*768)/width;
                    var top = (id.ymin*550)/height;
                    var right = (id.xmax*768)/width;
                    var bot = (id.ymax*550)/height;
                    dtx.beginPath();
                    dtx.strokeStyle = "#00FF00";
                    dtx.lineWidth=3
                    dtx.rect(left, top, right - left, bot - top);
                    dtx.stroke();
                    var canvas = document.getElementById("myCanvas");
                    var etx = canvas.getContext("2d");
                    etx.fillStyle = "red";
                    etx.font = "15px Arial";
                    top = top-4
                    if (left < 0) {
                        left = 10
                    }
                    if (top < 0) {
                        top = 10
                    }
                    etx.fillText(`${id.label}:${id.percent.toString().slice(0, 4)}`, left, top);
                })
                $("#btnSubmit").prop("disabled", false);
            },
            error: function (e) {
 
                $("#output").text(e.responseText);
                console.log("ERROR : ", e);
                $("#btnSubmit").prop("disabled", false);
 
            }
        });
    });
 
});
function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('#image').attr('src', e.target.result);
        var c = document.getElementById("myCanvas");
        var ctx = c.getContext("2d");
        var img = document.getElementById("image");
        img.onload = function(){
            ctx.drawImage(img, 0, 0,768,550);
        }
      }
      
      reader.readAsDataURL(input.files[0]);
    }
};
$("#img_file").change(function() {
    readURL(this);
});
