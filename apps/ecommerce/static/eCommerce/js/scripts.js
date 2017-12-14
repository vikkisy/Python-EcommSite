$(document).ready(function(){
  $('#search_bar').submit(function(e){
  e.preventDefault()
  });
  $('#search_name').keyup(function(){
  $.ajax({
    url: '/search',
    method: 'post',
    data: $(this).parent().serialize(),
    success: function(serverResponse) {
      $('#allitems').html(serverResponse)
      }
    })
  });

  $('#form_adminsearch').submit(function(e){
  e.preventDefault()
  });
  $('#adminsearch_name').keyup(function(){
  $.ajax({
    url: '/adminsearch',
    method: 'post',
    data: $(this).parent().serialize(),
    success: function(serverResponse) {
      console.log(serverResponse)
      $('.infohere').html(serverResponse)
      }
    })
  });

  $(document).on('submit', '#search_bar_cat', function(e){
    e.preventDefault()
    $.ajax({
      url:$(this).attr('action'),
      method: 'post',
      data: $(this).serialize(),
      success: function(serverResponse) {
        $('#allitems').html(serverResponse)
      }
    })
  });
  $(document).on('change', '#sorted', function(){
    $.ajax({
      url:'/sortby',
      method: 'post',
      data: $(this).parent().serialize(),
      success: function(serverResponse){
        $('#allitems').html(serverResponse)
      }
    })
  })
});
