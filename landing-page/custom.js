function timer_tick() {
  //@TODO make this safe against slow computers - what if not called every second?
  window.current_time += 1;
  var mins = Math.floor(window.current_time/60)
  var secs = window.current_time - mins*60
  window.el_timer.innerHTML = mins.toString().padStart(2, '0') + ":" + secs.toString().padStart(2, '0')
}

function click_abstract_link(abstract_index) {
  //@TODO What if they already clicked that?
  window.current_time = 0;
  window.el_timer = document.getElementById('abstract-'+abstract_index+'-time');
  window.timer_interval = window.setInterval(timer_tick, 1000);
  document.getElementById('abstract-'+abstract_index+'-done').disabled = false;
}

function click_abstract_done(abstract_index) {
  window.clearInterval(window.timer_interval);
  $(' <span class="badge badge-success" style="margin-left: .5em">Done!</span>').insertBefore('#abstract-'+abstract_index+'-time');
  $('#abstract-'+abstract_index).collapse('hide');
  $('#abstract-'+(abstract_index+1)).collapse('show');
}
