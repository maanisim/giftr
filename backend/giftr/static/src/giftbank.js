function onH(x){
  x.getElementsByTagName('img')[0].src = "{{ url_for('static', filename='img/gift-black.png') }}";
  x.getElementsByTagName('a')[0].style.color = "black";
}

function onE(x){
  x.getElementsByTagName('img')[0].src = "{{ url_for('static', filename='img/gift.png') }}";
  x.getElementsByTagName('a')[0].style.color = "white";
}
