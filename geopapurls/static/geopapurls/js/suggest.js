  $('document').ready((function() {
    $("#id_source").autocomplete({
      source: availableTags
    });
  }));