function submitForm (){
    let form = document.getElementById('upload-form')
    var formData = new FormData(form);
    $.ajax({
        url: window.location.origin + '/api/buckets',
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

function deleteImage (element){
    imageName = element.dataset.image;
    console.log(imageName);
    parentLi = element.parentElement
    console.log(parentLi)
    $.ajax({
        url: window.location.origin + '/api/buckets?filename='+imageName,
        type: 'DELETE',
        async: true,
        cache: false,
        contentType: false,
        processData: false,
    })
    .done(function(val){
        console.log(val);
        parentLi.remove();
    })
    .fail(function(val){
        console.log("Error removing file: ");
        console.log(val);
    })
}