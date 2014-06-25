var extractFilename = function (path) {
  var pieces = path.split(/(\\|\/)/g);
  return pieces[pieces.length - 1];
};


$(function() {
  $('#file-btn').click(function() {
    $('#jar_file').click();
  });

  $('#jar_file').change(function() {
    var filename = extractFilename($(this).val());
    $('#selected-file').text(filename);
  });


  if (window.showOnLoad && window.showOnLoad.length > 0) {
    for (var i = 0; i < window.showOnLoad.length; i++) {
      var selector = '#' + window.showOnLoad[i];
      $(selector).modal('show');
    }
  }
});
