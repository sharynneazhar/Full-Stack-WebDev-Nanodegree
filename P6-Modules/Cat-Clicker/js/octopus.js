var octopus = {

  init: function() {
    // default the current cat to the first
    cats.currentCat = cats.cats[0];

    // initialize the views
    catListView.init();
    catView.init();
  },

  getCats: function() {
    return cats.cats;
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
