$(document).ready(function () {
    function updateText(btn, newCount, verb) {
        btn.attr("data-likes", newCount)
        btn.text(newCount + " " + verb)
    }

    $(".like-btn").click(function (e) {
        e.preventDefault()
        var this_ = $(this)
        var likeUrl = this_.attr("data-href")
        var likeCount = parseInt(this_.attr("data-likes")) | 0
        var addLike = likeCount + 1
        var removeLike = likeCount - 1
        if (likeUrl) {
            $.ajax({
                url: likeUrl,
                method: "GET",
                data: {},
                success: function (data) {
                    console.log(data)
                    var newLikes;
                    if (data.liked) {
                        updateText(this_, addLike, "Unlike")
                    } else {
                        updateText(this_, removeLike, "Like")
                        // remove one like
                    }

                }, error: function (error) {
                    console.log(error)
                    console.log("error")
                }
            })
        }

    })
})
