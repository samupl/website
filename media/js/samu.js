var pageGlobals = {
    subTitle: '',
    previousId: '',
    topMenu: null
};

(function ($) {
    $.fn.comments = function () {
        return this.each(function () {
            $comments = $(this);
            var url = $comments.data('url');

            var $loader = $('<i class="fa fa-spinner fa-spin""></i> <span>Loading...</span>');
            $comments.html($loader);

            $.get(url, function (data) {
                var comment, $comment, $image, $body, $header, $date;

                $comments.html("");

                for (c in data.comments) {
                    comment = data.comments[c];
                    $comment = $('<div></div>');
                    $comment.addClass('media')

                    $image = $('<img>');
                    $image.addClass('media-object');
                    $image.addClass('pull-left');
                    $image.attr('src', comment.avatar);

                    $comment.append($image);

                    $body = $('<div></div>');
                    $body.addClass('media-body');

                    $comment.append($body);

                    $header = $('<h4></h4>');
                    $header.addClass('media-heading');
                    $header.html(comment.username);
                    $body.append($header);

                    $date = $('<small></small>')
                    $date.html(comment.date);
                    $header.append($date);

                    $body.append(comment.content);
                    $comments.append($comment);
                }
            });
        });
    };
}(jQuery));

function changeTitle(id) {
    var subTitle = $('#' + id).data('title');
    if (subTitle)
        document.title = pageGlobals.baseTitle + ' ' + subTitle;
    else
        console.log('Could not find title for id: ' + id);
}

function windowScrollCallback() {
    if (window.location.pathname != '/') return;

    // region Auto-active on user scroll
    var topMenu = pageGlobals.topMenu;
    var topMenuHeight = topMenu.outerHeight() + 15;
    //// All list items
    var menuItems = pageGlobals.menuItems;
    //// Anchors corresponding to menu items
    var scrollItems = menuItems.map(function () {
        var href = $(this).attr("href");
        if (href[0] == "/") href = href.substr(1);
        var item = $(href);
        if (item.length) {
            return item;
        }
    });

    // Get container scroll position
    var fromTop = $(this).scrollTop() + topMenuHeight;

    // Get id of current scroll item
    var cur = scrollItems.map(function () {
        if ($(this).offset().top < fromTop)
            return this;
    });
    // Get the id of the current element
    cur = cur[cur.length - 1];
    var id = cur && cur.length ? cur[0].id : "";

    // If user has scrolled to the bottom, then set the id to 'contact'.
    if(pageGlobals.window.scrollTop() + pageGlobals.window.height() > pageGlobals.document.height() - 100) {
        id = 'contact';
    }

    if (id == pageGlobals.previousId) return;

    // Set/remove active class
    menuItems
        .parent().removeClass("active")
        .end().filter("[href*=#" + id + "]").parent().addClass("active");

    changeTitle(id);
    history.pushState(null, null, '#'+id);
    pageGlobals.previousId = id;
    // alert(id);
}

function setJquerySelectors() {
    pageGlobals.topMenu = $("#top");
    pageGlobals.menuItems = $("a.scroll");
    pageGlobals.window = $(window);
    pageGlobals.document = $(document);
}

function renderCategories() {
    var $categories = $("#categories");
    if ($categories.length == 0) return;
    var url = $categories.data('url');
    var labelBaseUrl = $categories.data('category-url');

    // Clean categories div
    $categories.children().remove();

    $.get(url)
        .success(function(data) {
            $.each(data.label_stats, function(i, obj) {
                var label = $('<a></a>').addClass('list-group-item');
                label.text(obj.label);
                label.attr('href', labelBaseUrl.replace('__replace__', obj.label));
                label.appendTo($categories);

                var badge = $('<span></span>').addClass('badge');
                badge.text(obj.count);
                badge.appendTo(label);
            })
        });
}

$(document).ready(function () {

    pageGlobals.baseTitle = document.title;
    setJquerySelectors();

    if (window.location.pathname == '/')
        document.title = pageGlobals.baseTitle + ' ' + 'Home';

    // Dynamically load projects modal content
    $('#modal-projects').on('show.bs.modal', function (e) {
        var $source = $(e.relatedTarget);
        var that = this;
        var url = $source.data('url');
        var title = $source.data('title');

        $.get(url, function (data) {
            $(that).find('.modal-body').html(data);
            $(that).find('h4.modal-title').text(title);
        });
    })

    // Dynamically load comments for a post
    $(".ajax-load-comments").comments()

    // Contact form
    var $contact_form = $(".ajax-form");
    $contact_form.find('button[type="submit"]').click(function () {
        var $button = $(this);
        var $form = $button.parents('form');

        // Remove all has-error classes and all error messages and alerts
        $contact_form.find('span.error_message').remove();
        $contact_form.find('.has-error').removeClass('has-error');
        $button.attr('disabled', 'disabled');
        $button.find('.spinner').show();
        $("#mail-sent-ok").addClass('hide');

        // Make the AJAX request
        $.ajax({
            type: 'POST',
            url: $contact_form.attr('action'),
            data: $contact_form.serialize(),
            success: function (data) {
                $form.find(".ajax-form-ok").removeClass('hide');
                $button.attr('disabled', false);
                $button.find('.spinner').hide();
                $form.find('img.captcha').attr('src', data['__captcha_image_src']);
                $form.find('input#id_captcha_0').val(data['__captcha_key']);
                $form.trigger('ajax-form:success');
            },
            error: function (jqXRH) {
                var data = JSON.parse(jqXRH.responseText);

                $form.find('img.captcha').attr('src', data['__captcha_image_src']);
                $form.find('input#id_captcha_0').val(data['__captcha_key']);

                for (var item in data) {
                    // Construct ids and error messages for them

                    // A hack for Captcha MultiValueField, where first item is a hidden input
                    var item_id = item;
                    if (item_id == 'captcha') item_id = 'captcha_1';

                    var field_id = "#id_" + item_id;
                    var field_error = data[item][0];

                    // Find element to add .has-error
                    var $input = $(field_id);
                    var $error_obj = $input.parents('.form-group');
                    $error_obj.addClass('has-error');

                    // Create a span.help-block with the error message
                    var $error_msg = $('<span class="error_message pull-right label label-danger"></span>');
                    $error_msg.text(field_error);

                    // Put the error message block next to the form input
                    $error_msg.insertAfter($input);
                    // var $label = $('label[for="id_' + item_id + '"]').append($error_msg);
                }
                $button.attr('disabled', false);
                $button.find('.spinner').hide();
            }
        });

    });

    // Smooth scrolling
    $("a.scroll").click(function (e) {
        if (window.location.pathname != '/') return;
        e.preventDefault();

        var target = this.hash;
        var $target = $(target);
        var target_top = $target.offset().top;
        target_top -= 50;
        if (target == '#top') target_top = 0;

        // Switch active urls

        $('html, body').stop().animate({
            'scrollTop': target_top
        }, 900, 'swing', function () {
            window.location.hash = target;
        });
    });

    // Bind to scroll
    $(window).scroll(windowScrollCallback);
    // endregion

    renderCategories();
});
