$(document).ready(function () {

  setTimeout(function () {
    $('#flash-container .alert').each(function () {
      $(this).fadeOut(500, function () { $(this).remove(); });
    });
  }, 4000);

  var currentPath = window.location.pathname;
  $('.navbar-nav .nav-link').each(function () {
    var href = $(this).attr('href');
    if (href && href !== '/' && currentPath.startsWith(href)) {
      $(this).addClass('active');
    } else if (href === '/' && currentPath === '/') {
      $(this).addClass('active');
    }
  });

  $('a[href="#top"]').on('click', function (e) {
    e.preventDefault();
    $('html, body').animate({ scrollTop: 0 }, 400);
  });

  if ($('#course-grid').length) {
    $('#course-grid .course-item').each(function (i) {
      var $item = $(this);
      setTimeout(function () {
        $item.css({ opacity: 0, transform: 'translateY(20px)' });
        $item.animate({ opacity: 1 }, {
          duration: 400,
          step: function (now) {
            $(this).css('transform', 'translateY(' + (20 * (1 - now)) + 'px)');
          }
        });
      }, i * 80);
    });
  }

  var $backTop = $('<button class="lh-back-top btn lh-btn-primary"><i class="bi bi-arrow-up"></i></button>');
  $backTop.css({
    position: 'fixed', bottom: '24px', right: '24px',
    width: '44px', height: '44px',
    border: 'none', border_radius: '50%',
    display: 'none', 'z-index': 9999,
    'border-radius': '50%', padding: '0',
    'box-shadow': '0 4px 16px rgba(0,0,0,0.15)'
  });
  $('body').append($backTop);

  $(window).on('scroll', function () {
    if ($(this).scrollTop() > 300) $backTop.fadeIn(200);
    else $backTop.fadeOut(200);
  });

  $backTop.on('click', function () {
    $('html, body').animate({ scrollTop: 0 }, 400);
  });

  var tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltipEls.forEach(function (el) {
    new bootstrap.Tooltip(el);
  });

});
