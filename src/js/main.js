var $template_block = null;
var currentItem = 0;

$(document).ready(function() {
    $template_block = $('#template_block');
    
    $.getJSON("/v1/newsletter")
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
        $.getJSON("/v1/newsletter/" + currentItem + "/next")
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
