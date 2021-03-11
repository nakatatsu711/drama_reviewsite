$(function() {
  $('.stars').raty({
    readOnly: true,
    score: function() {
      return $(this).attr('data-score');
    },
    path: '../static',
    path: '../../static'
  });
});
