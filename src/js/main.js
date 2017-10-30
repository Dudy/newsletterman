$template_block = $('#template_block');
var BASE_URI = "/v1";
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

var openInNewTab = function(body) {
    var newTab = window.open();
    newTab.document.open();
    newTab.document.write(body);
    newTab.document.close();
};

var loadFirstBatch = function() {
    $.getJSON(BASE_URI + "/api/newsletter")
    .done(function (newsletteritems) {
        newsletteritems.forEach(function (item) {
            var $newItem = $template_block.clone();
            $newItem.removeAttr('id');
            $newItem.find('img').attr('src', item.imageUrl);
            $newItem.find('h4').text(item.title);
            $newItem.find('span').text(item.text);
            $newItem.insertBefore($template_block);
            $newItem.on('click touch', function() {openInNewTab(item.body);});
        });
        currentItem = newsletteritems.length;
    })
    .fail(function (jqxhr, textStatus, error) {
        var err = textStatus + ", " + error;
        console.log("Request Failed: " + err);
    });
    
    $('#next').on('click touch', function (event) {
        event.preventDefault();
        $.getJSON(BASE_URI + "/api/newsletter/" + currentItem + "/next")
        .done(function (item) {
            var $newItem = $template_block.clone();
            $newItem.removeAttr('id');
            $newItem.find('img').attr('src', item.imageUrl);
            $newItem.find('h4').text(item.title);
            $newItem.find('span').text(item.text);
            $newItem.insertBefore($template_block);
            $newItem.on('click touch', function() {openInNewTab(item.body);});
            currentItem = currentItem + 1;
        })
        .fail(function (jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.log("Request Failed: " + err);
        });
    });
};

$(document).ready(function() {
    // register action handler
    $('nav a:not(.dropdown-toggle)').on('click touch', navActionHandler);
    
    loadFirstBatch();
});

function isBlank(str) {
    return (!str || /^\s*$/.test(str));
}