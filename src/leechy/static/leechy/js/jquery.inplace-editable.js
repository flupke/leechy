/**
 * $.fn.inplaceEditable()
 *
 * In-place editable elements.
 */

(function($)
{

var instances = [];

function nl2br(str)
{
    return str.replace(/\n/g, "<br>");
}

function br2nl(str)
{
    return str.replace(/\n/g, "").replace(/<br>/g, "\n");
}

var methods = {
    /**
     * Initialize an in-place editable HTML element, replaced by a text input when
     * clicked.
     *
     * Options:
     *   * callback: a function called when editing successfully finished, with
     *     the new value entered by the user.
     *   * validate: a function called before finishing the edition with the actual
     *     value of the input that returns false if the value is not valid.
     *   * validation_error_callback: a function called when validate() returned
     *     false.
     *   * textarea: if true, use a textarea instead of an input (default: false)
     *   * resizable: make the edition widget resizable if true 
     *     (default: false, requires jQuery UI)
     *   * placeholder_text: if the text is equal to this value at the end of
     *     edition, don't trigger *callback*
     *   * input_class: a CSS class to apply to the edition input.
     */
    init: function(options) 
        {
            var settings = {
                callback: null,
                validate: null,
                validation_error_callback: null,
                textarea: false,
                resizable: false,
                placeholder_text: null,
                input_class: null
            };
            $.extend(settings, options);

            return this.each(function()
            {
                var $this = $(this);
                instances.push($this);

                // Store settings
                $this.data("inplaceEditable", {
                    settings: settings, 
                });
                var data = $this.data("inplaceEditable");

                // Put placeholder text in matching element
                if (settings.placeholder_text !== null && $.trim($this.html()) === "") {
                    $this.html(settings.placeholder_text);
                }

                $this.click(function()
                {
                    var input, initial_value = $.trim($this.html());
                    if (initial_value === settings.placeholder_text) {
                        initial_value = "";
                    }
                    if (settings.textarea) {
                        input = $('<textarea>' + br2nl(initial_value) + "</textarea>");
                        input.css("width", ($this.width() - 10) + "px");
                        input.css("height", $this.height() + "px");                    
                    } else {
                        input = $('<input type="text" value="' + initial_value + '" />');
                    }
                    if (settings.input_class !== null) {
                        input.addClass(settings.input_class);
                    }
                    data.input = input;
                    // Call accept() on all inplaceEditable instances (fixes a
                    // bug on FF where blur event is not fired when clicking on
                    // another inplaceEditable)
                    $.each(instances, function(index, instance) 
                    {
                        if (instance !== $this) {
                            instance.inplaceEditable("accept");
                        }
                    });

                    // Install event handlers
                    input.blur(function(e)
                    {
                        $this.inplaceEditable("accept");
                    });
                    input.keyup(function(e)
                    {
                        var code = e.keyCode || e.which; 
                        if (code == 13 && !settings.textarea) {
                            // User pressed Return key
                            $this.inplaceEditable("accept");
                        } else if (code == 27) {
                            // User pressed Escape key
                            $this.inplaceEditable("reject");
                        }
                    });

                    // Replace original element with input
                    input.insertBefore($this);
                    if (data.settings.resizable) {
                        input.resizable();
                    }
                    input.focus();
                    input.select();
                    $this.hide();
                });                
            });   
        },
    /**
     * Accept edition.
     *
     * If the data validates, put back the original item (filled with the new
     * value) and run callback function.
     */
    accept: function()
        {
            return this.each(function() 
            {
                // Get edited value and validate it
                var $this = $(this);
                var data = $this.data("inplaceEditable");
                var input = data.input, settings = data.settings;
                if (!input) {
                    // This element is not in edit mode
                    return true;
                }
                var value = input.val();
                if (settings.validate && !settings.validate(value)) {
                    // Invalid input
                    if (settings.validation_error_callback) {
                        settings.validation_error_callback(value);
                    }                            
                    // We use setTimeout to put focus back to the input because
                    // using focus() in the blur() handler doesn't work
                    setTimeout(function() {
                        input.focus();
                        input.select();
                    }, 100);
                    return;
                }
                // Value is OK, put back the original element and launch callback
                input.remove();
                data.input = undefined;
                if (settings.placeholder_text && !value) {
                    $this.html(settings.placeholder_text);
                } else {
                    $this.html(nl2br(value));
                    if (settings.callback) {
                        if (value !== settings.placeholder_text) {
                            settings.callback.apply(this, [value]);
                        }
                    }
                }
                $this.show();
            });
        },
    /**
     * Cancel edition and put back the original item in place of the input.
     */
    reject: function()
        {
            return this.each(function()
            {
                var $this = $(this);
                var input = $this.data("inplaceEditable").input;
                if (!input) {
                    // This element is not in edit mode
                    return true;
                }
                input.remove();
                $this.removeData("input");
                $this.show();
            });
        }
};

$.fn.inplaceEditable = function(method) 
{
    // Dispatch to methods
    if (methods[method]) {
        return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
    } else if (typeof method === 'object' || !method ) {
        return methods.init.apply(this, arguments);
    } else {
        $.error('Method ' + method + ' does not exist on jQuery.inplaceEditable');
    }
};

})(jQuery);
