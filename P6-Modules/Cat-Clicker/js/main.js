var octopus = {

  init: function() {
    // default the current cat to the first
    cats.currentCat = cats.cats[0];

    // initialize the views
    catListView.init();
    catView.init();
  },

  getCurrentCat: function() {
    return cats.currentCat;
  },

  setCurrentCat: function(cat) {
    cats.currentCat = cat;
  },

  incrementCount: function() {
    cats.currentCat.clickCount++;
    catView.render();
  }

};

var catListView = {

  init: function() {
    $CATLIST = $('.cat-list');
    $CATLISTITEM = $('.cat-list-item');
    this.render();
  },

  render: function() {
    $.each(cats.cats, function(index, cat) {
      $CATLIST.append(
        '<li class="cat-list-item ' + index + '">' + cat.name + '</li>'
      );

      var catIndexClass = '.' + index;
      $CATLIST.on('click', catIndexClass, function() {
        octopus.setCurrentCat(cat);
        catView.render();
      });
    });
  }

};

var catView = {
  init: function() {
    $CATNAME = $('.cat-name');
    $CATGENDER = $('.cat-gender');
    $CATIMAGE = $('.cat-image');
    $CATCLICKCOUNT = $('.cat-clickCount');

    $CATIMAGE.on('click', function() {
      octopus.incrementCount();
    });

    this.render();
  },

  render: function() {
    var currentCat = octopus.getCurrentCat();
    $CATNAME.html(currentCat.name);
    $CATCLICKCOUNT.html(currentCat.clickCount);
    $CATGENDER.html(currentCat.gender);
    $CATIMAGE.html('<img src="' + currentCat.image + '" />');
  }

}

octopus.init();
