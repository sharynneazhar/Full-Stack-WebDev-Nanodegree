$('document').ready(function() {

  // get cat pictures from api
  var CAT_API = 'http://thecatapi.com/api/images/get?format=xml&type=jpg&size=small&results_per_page=2';
  var imgTag = '<img src="%data%" alt="Cat" />'

  var cat0Clicks = 0;
  var cat1Clicks = 0;

  $.ajax({
    url: CAT_API,
    dataType: 'xml'
  }).done(function(data) {
    $(data).find('image').each(function(index) {
      var url = $(this).find("url").text();
      $('body').append(
        '<div id="cat' + index + '">'
        + imgTag.replace('%data%', url)
        + '<div class="clicks">Number of clicks: <span class="count"></span></div>'
        + '</div>'
      );
    });

    $('#cat0 .count').html(cat0Clicks);
    $('#cat1 .count').html(cat1Clicks);

  }).fail(function() {
    $('body').html('<h1>An error occurred. Try again later.</h2>')
  });

});
