{% load i18n %}
$(function()
{
    // Files and directories checkboxes handler
    $(".entry_checkbox").change(function()
    {
        var $this = $(this);
        $.get("{% url leechy_update_file_metadata key=key %}", {
            path: $this.closest("tr").attr("path"), 
            attr: "checked",
            value: $this.prop("checked")
        });
        $this.parent().toggleClass("checked");
    });

    // Settings persistence
    $(".toolbar input[type=checkbox]").change(function()
    {
        var $this = $(this);
        $.get("{% url leechy_update_settings key=key %}", {
            attr: $this.attr("id"),
            value: $this.prop("checked")
        });
    });

    // Hide/unhide checked entries
    function hide_checked_entries()
    {
        if ($("#hide_checked").prop("checked")) {
            $(".item.checked").hide();
        } else {
            $(".item.checked").show();
        }
    }

    $("#hide_checked").change(hide_checked_entries);

    // Keep the toolbar on top
    var toolbar = $(".toolbar");
    var toolbar_initial_offset = toolbar.offset();
    var toolbar_initial_width = toolbar.width();

    function pin_toolbar()
    {
        if ($(document).scrollTop() > toolbar_initial_offset.top) {
            toolbar.addClass("pinned");
            toolbar.css("left", toolbar_initial_offset.left + "px");
            toolbar.css("width", toolbar_initial_width + "px");
        } else {
            toolbar.removeClass("pinned");
            toolbar.css("left", "");
            toolbar.css("width", "");
        }
    }

    $(window).scroll(pin_toolbar);
    $(window).resize(pin_toolbar);

    // Search
    var search_input = $(".search"), search_helper = "{% trans 'Search...' %}";

    function filter_items()
    {
        var words = [], search_text = $.trim(search_input.val());
        if (search_text === search_helper || search_text === "") {
            // Empty search
            $(".item").show();
            hide_checked_entries();
            return;
        }
        $.each(search_text.split(" "), function(index, word)
        {
            if ($.trim(word) !== "") {
                words.push(word.toLowerCase());
            }
        });
        $(".item").each(function()
        {
            var item = $(this), item_words = item.attr("search_words").toLowerCase(), match_count = 0, i;
            for (i = 0 ; i < words.length ; i++) {
                if (item_words.indexOf(words[i]) !== -1) {
                    match_count += 1;
                }
            };
            if (match_count === words.length) {
                item.show();
            } else {
                item.hide();
            }
        });
    }

    search_input.focus(function()
    {
        if (search_input.val() == search_helper){ 
            search_input.val("");
            search_input.removeClass("dim");
        }
    }).blur(function()
    {
        if (search_input.val() == "") {
            search_input.val(search_helper);
            search_input.addClass("dim");
        }
    }).keyup(filter_items);

    $(".search_container .reset").click(function()
    {
        search_input.val(search_helper);
        search_input.addClass("dim");
        filter_items();
    });

    // TableSorter
    $.tablesorter.addParser({
        id: "dir_entry",
        is: function() { return false; },
        format: function(text, table, cell) {
            text = $.trim(text.toLowerCase());
            if ($(cell).hasClass("directory")) {
                // Put directories in front of the ASCII sorting order
                return "                 " + text;
            }
            return text;
        },
        type: "text",
    });

    $.tablesorter.addParser({
        id: "tablesorter_attr",
        is: function() { return false; },
        format: function(text, table, cell) {
            return $.tablesorter.formatFloat($(cell).attr("tablesorter"));
        },
        type: "numeric",
    });

    $("#browser_table").tablesorter({
        headers: {
            0: {sorter: "dir_entry"},
            1: {sorter: "tablesorter_attr"},
            2: {sorter: "tablesorter_attr"}
        },
        sortList: [[0, 0]],
        cssAsc: "sort_up",
        cssDesc: "sort_down"
    });

    // Setup initial state
    hide_checked_entries();
    pin_toolbar();
    if (search_input.val() != search_helper) {
        search_input.removeClass("dim");
    }
    filter_items();

    // Tags
    $(".tags").inplaceEditable({
        input_class: "tags",
        placeholder_text: '<span class="hint">{% trans "Click here to add tags" %}</span>',
        callback: function(tags) {
            $.get("{% url leechy_update_file_metadata key=key %}", {
                path: $(this).closest("tr").attr("path"), 
                attr: "tags",
                value: tags
            });
        }
    });
    $(".tags_cloud a").click(function(e) 
    {
        e.preventDefault();
        $("input.search").removeClass("dim").val("[" + $(this).html() + "]");
        filter_items();
    });

    // Shoutbox
    var shoutbox_hide_target = {
        width: '40px',
        height: '80px',
        opacity: 0
    };
    var shoutbox_show_target = {
        opacity: 1
    };

    $("#shoutbox .hide_line").click(function() 
    {
        shoutbox_show_target["height"] = $("#shoutbox").height() + 'px';
        shoutbox_show_target["width"] = $("#shoutbox").width() + 'px';
        $("#shoutbox").animate(shoutbox_hide_target, 400, 'swing', function()
        {
            $("#shoutbox").hide();
            $("#show_shoutbox").show();
        });
    });

    $("#show_shoutbox").click(function()
    {
        $("#show_shoutbox").hide();
        $("#shoutbox").show();
        $("#shoutbox").animate(shoutbox_show_target, 400, 'swing');
    });

    $("#shoutbox textarea").keyup(function(event)
    {
        if (event.keyCode === 13 && !event.shiftKey) {
            $("#shoutbox form").submit();
        }
    });

    $("#shoutbox .messages").scrollTop($("#shoutbox .messages").height() + 100);
});
