function loadData() {
  const GOOGLE_STREET_API = 'http://maps.googleapis.com/maps/api/streetview?size=600x300&location=';

  var $body = $('body');
  var $wikiElem = $('#wikipedia-links');
  var $nytHeaderElem = $('#nytimes-header');
  var $nytElem = $('#nytimes-articles');
  var $greeting = $('#greeting');

  // form variables
  var $street = $('#street');
  var $city = $('#city');
  var $submitBtn = $('#submit-btn');

  // clear out old data before new request
  $wikiElem.text("");
  $nytElem.text("");

  // load streetview
  if ($street.val() && $city.val()) {
    var streetView = '<img class="bgimg" src="%data%" />';
    var address = $street.val() + ", " + $city.val();

    $body.append(
      streetView.replace('%data%', GOOGLE_STREET_API + address)
    );

    $greeting.text(address.toUpperCase());

  } else {
    $('form').append(
      '<p class="error">Please fill in both fields.</p>'
    );

    setTimeout(function() {
      $('.error').slideUp("slow");
    }, 2000);
  }


  return false;
};

$('document').ready(function() {
  $('#form-container').submit(loadData);

});
