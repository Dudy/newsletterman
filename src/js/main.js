var BASE_URI = "/v1";
var $template_block = null;
var currentItem = 0;

var navActionHandler = function(event) {
    event.preventDefault();
    var url = BASE_URI + "/content/" + event.target.href.substring(event.target.href.indexOf("#") + 1);
    $.get(url)
    .done(function(content) {
        $('#mainContent').empty();
        $('#mainContent').append(content);
    })
    .fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.log("Request Failed: " + err);
    });
};

$(document).ready(function() {
    $template_block = $('#template_block');
    
    // register action handler
    $('.action').on('click touch', navActionHandler);
    
    $.getJSON(BASE_URI + "/api/newsletter")
    .done(function(newsletteritems) {
        newsletteritems.forEach(function(item) {
            var $newItem = $template_block.clone();
            $newItem.removeAttr('id');
            $newItem.find('img').attr('src', item.imageUrl);
            $newItem.find('h4').text(item.title);
            $newItem.find('span').text(item.text);
            $newItem.insertBefore($template_block);
        });
        currentItem = newsletteritems.length;
    })
    .fail(function(jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.log("Request Failed: " + err);
    });
    
    $('#next').on('click touch', function(event) {
        event.preventDefault();
        $.getJSON(BASE_URI + "/api/newsletter/" + currentItem + "/next")
        .done(function(item) {
            var $newItem = $template_block.clone();
            $newItem.removeAttr('id');
            $newItem.find('img').attr('src', item.imageUrl);
            $newItem.find('h4').text(item.title);
            $newItem.find('span').text(item.text);
            $newItem.insertBefore($template_block);
            currentItem = currentItem + 1;
        })
        .fail(function(jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.log("Request Failed: " + err);
        });
    });
});
