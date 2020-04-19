<?php
/**
	$success = false;
	echo "a";
	if ($_POST["submit"]){
		$subject = "Contact from: ";
		$name = $_POST["name"];
		$subject = $subject.$name; 
		$message = $_POST["message"];
		$email = $_POST["email"];
		mail("walkr121@gmail.com", $subject, $message, "From: walkr121@gmail.com");
		$success = true;
	}
	*/
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us | Giftr</title>
    <link rel='icon' href='{{ url_for('static', filename='img/favicon.ico') }}' type='image/x-icon'>
    <link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.0.13/css/all.css'>
    <link rel="stylesheet" href="{{ url_for('static', filename='src/style.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='src/contact.css') }}">

</head>	
		
<body>
	    <!-- nav bar-->
    <nav class="navbar navbar-inverse">
        <div class="container-fluid">
          <div class="navbar-header">
            <a href="{{ url_for('index') }}">
            <img src="{{ url_for('static', filename='img/logo.png') }}" alt="Logo" width="120" draggable="false" style="margin-top: 8px; margin-right: 10px;"> 
            </a>
          </div>
          <ul class="nav navbar-nav">
            <li class="active"><a href="{{ url_for('index') }}">Home</a></li>
            <li><a href="{{ url_for('suggestion') }}">Item suggestion</a></li>
          </ul>
          <form class="navbar-form navbar-left" action="/action_page.php">
            <div class="input-group">
              <input type="text" class="form-control" placeholder="Search for gift" name="search">
              <div class="input-group-btn">
                <button class="btn btn-default" type="submit">
                  <i class="glyphicon glyphicon-search"></i>
                </button>
              </div>
            </div>
          </form>
              <ul class="nav navbar-nav navbar-right">
                {% if 'loggedin' in session %}
                <li><a href="{{ url_for('home') }}"><span class="glyphicon glyphicon-user"></span>My profile</a></li>
                {% else %}
                <li><a href="{{ url_for('login') }}"><span class="glyphicon glyphicon-log-in"></span> Login</a></li>
                <li><a href="{{ url_for('register') }}"><span class="glyphicon glyphicon-user"></span> Sign Up</a></li>
                {% endif %}
          </ul>
        </div>
      </nav>
	
	
     <div id="page-container">
         <div id="content-wrap">
             <div class="header">
                 <center>
                    <a href= "{{ url_for('index') }}">
                         <img src="{{ url_for('static', filename='img/logo.png') }}" alt="Logo" width="410" height="120"> 
                    </a>
                    <br>Gifts that never disappoint
                 </center>
             </div>
              <div class="giftbank" onmouseover="onH(this)" onmouseout="onE(this)">
                <img src="{{ url_for('static', filename='img/gift.png') }}" alt="Gift icon" width="30" height="30" draggable="false">
                <a href="{{ url_for('wishlist') }}">Gift Bank</a>
            </div>
            <script type="text/javascript">
                function onH(x){
                    x.getElementsByTagName('img')[0].src = "{{ url_for('static', filename='img/gift-black.png') }}";
                    x.getElementsByTagName('a')[0].style.color = "black";
                }
                function onE(x){
                    x.getElementsByTagName('img')[0].src = "{{ url_for('static', filename='img/gift.png') }}";
                    x.getElementsByTagName('a')[0].style.color = "white";
                }
            </script>

             <div class= "writing">
                <h1>Contact Us</h1>
                <p>Maybe you want to suggest new items that you are interested in and would like to add them to our wesbite or other improvements we could make...</p>
                <p>Or maybe you would like us to add your products on our website...</p>
                <p>Or maybe you have encountered a bug that won't go away...</p>
                <p>Whatever your reason may be, you can reach us by filling in the form here.</p>
             </div>
             <div class="container">
            <div class="form">
                <form action="{{ url_for('contact') }}" method="post">
                    <p class="name">
                        <input name="name" type="text" class="feedback-input" required placeholder="Name" id="name" />
                    </p>
                    <p class="email">
                        <input name="email" type="email" required class="feedback-input" id="email" placeholder="Email"/>
                    </p>
                    <p class="text">
                        <textarea name="message" class="feedback-input" id="comment" placeholder="Message"></textarea>
                    </p>
                    <div class="submit">
                        <button type="submit" class="button-blue" name="submit">Submit</button>
                    </div>
		<?php
			if($success == true){
		?>
				<p> Email Sent! </p>
					
		<?php
			}
		?>		
                    </form>
             </div>
             </div>
            
             <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script>
         </div>
         <div class="footer">
             <a href="{{ url_for('about') }}">About Us</a>
             |
             <a href="{{ url_for('contact') }}">Contact Us</a>
             |
             <a href="{{ url_for('privacy') }}">Privacy Policy</a>
         </div>
    </div>
    
</body>
</html>
