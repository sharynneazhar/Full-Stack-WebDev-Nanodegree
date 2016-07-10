var Cat = function(data) {
  this.clickCount = ko.observable(data.clickCount);
  this.name = ko.observable(data.name);
  this.gender = ko.observable(data.gender);
  this.nicknames = ko.observableArray(data.nicknames);
  this.description = ko.observable(data.description);
  this.imgSrc = ko.observable(data.image);

  this.level = ko.pureComputed(function() {
    var clicks = this.clickCount();
    if (clicks < 10) {
      return 'Newborn';
    } else if (clicks < 50) {
      return 'Infant';
    } else if (clicks < 100) {
      return 'Child';
    } else if (clicks < 200) {
      return 'Teen';
    } else if (clicks < 500) {
      return 'Adult';
    } else {
      return 'Ninja';
    }
  }, this);
}

var ViewModel = function() {
  var self = this;

  this.catList = ko.observableArray([]);

  cats.forEach(function(catItem) {
    self.catList.push(new Cat(catItem));
  });

  this.currentCat = ko.observable(this.catList()[0]);

  this.incrementCounter = function() {
    self.currentCat().clickCount(self.currentCat().clickCount() + 1);
  };

  this.setCat = function(cat) {
    self.currentCat(cat);
  };

}

ko.applyBindings(new ViewModel());
