jQuery(function($) {
    $(document).ready( function() {

        function scrollToAnchor(aid){
            var aTag = $("#"+ aid);
            $('html,body').animate({scrollTop: aTag.offset().top}, 1000);
        }

        function emptyBookInfo() {
            $("#book-info").addClass("hidden");
            $("#book-loading").removeClass("hidden");
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
        }

        function goToISBNList() {
            scrollToAnchor('isbn-list');
            window.location.href = "#isbn-list";
        }

        function getBookInfo() {
            $("#book-loading").addClass("hidden");
            $("#book-info").removeClass("hidden");
        }

        function displayBook() {
            emptyBookInfo();
            goToISBNList();
            setTimeout(getBookInfo, 2000);
        }

        function postISBN(isbn, callback) {

            var request = $.ajax({
                url: "/",
                type: "post",
                data: {
                    'isbn': isbn,
                    csrfmiddlewaretoken: $.cookie("csrftoken")
                }
            });

            request.done(function (response, textStatus, jqXHR){
                console.log("Hooray, it worked!");
                callback();
            });

            // Callback handler that will be called on failure
            request.fail(function (jqXHR, textStatus, errorThrown){
                // Log the error to the console
                console.error(
                    "The following error occurred: "+
                    textStatus, errorThrown
                );
            });

            // Callback handler that will be called regardless
            // if the request failed or succeeded
            request.always(function () {
                // Reenable the inputs
            });
        }

        console.log('Here')

        $(".isbn-submit").click(function(event) {
            console.log('Here2')
            isbn = $("#isbn-value").val();
            if (isbn === "") {
                return;
            }
            event.preventDefault();
            console.log(isbn);
            postISBN(isbn, displayBook)
        });
    });
});