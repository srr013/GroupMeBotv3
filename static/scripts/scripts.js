function submitForm (){
    let form = document.getElementById('upload-form')
    var formData = new FormData(form);
    $.ajax({
        url: 'http://localhost:5000/api/buckets',
        type: 'POST',
        data: formData,
        async: true,
        cache: false,
        contentType: false,
        processData: false,
    })
    .done(function(val){
        console.log(val)
        $("#imageUploadForm-uploadStatus").html("Upload status: " + val.text)
    })
    .fail(function(val){
        $("#imageUploadForm-uploadStatus").html("Error uploading file: " + val.text)
        console.log("Error uploading file: ")
        console.log(val)
    })
}