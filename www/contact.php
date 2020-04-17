<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us | Giftr</title>
    <link rel='icon' href='img/favicon.ico' type='image/x-icon'>
    <link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.0.13/css/all.css'><link rel="stylesheet" href="src/style.css">
    <link rel="stylesheet" href="src/contact.css">

</head>
	
<?php
	$success = false;
	if ($_POST["message"]){
		$subject = "Contact from:";
		$name = $_POST["name"];
		$subject = $subject.$name;
		$message = $_POST["message"];
		$email = $_POST["email"];
		mail("walkr121@gmail.com", $subject, $message, $email);
		$success = true;
	}
?>
	
<body>
     <div id="page-container">
         <div id="content-wrap">
             <div class="header">
                 <center>
                    <a href= "index.html">
                         <img src="img/logo.png" alt="Logo" width="410" height="120"> 
                    </a>
                    <br>Our motto goes here
                 </center>
             </div>
             <div class="giftbank">
                 <img src="img/gift.png" alt="Gift icon" width="30" height="30">
                 <a href="#">Gift Bank</a>
             </div>
             <div class="wrapper">
                 <nav class="tabs">
                     <div class="selector"></div>
                     <a href="#" class="active"><i class="fas fa-home"></i>Home</a>
                     <a href="#"><i class="fas fa-search"></i>Search for gift</a>
                     <a href="#"><i class="fas fa-gift"></i>Item suggestion</a>
                     <a href="#"><i class="fas fa-user"></i>My profile</a>
                 </nav>
             </div>

             <div class= "writing">
                <h1>Contact Us</h1>
                <p>Maybe you want to suggest new items that you are interested in and would like to add them to our wesbite or other improvements we could make...</p>
                <p>Or maybe you would like us to add your products on our website...</p>
                <p>Or maybe you have encountered a bug that won't go away...</p>
                <p>Whatever your reason may be, you can reach us by filling in the form here.</p>
             </div>
             <div class="container">
            <div class="form">
                <form action="contact.php" method="post" enctype="text/plain">
                    <p class="name">
                        <input name="name" type="text" class="feedback-input" required placeholder="Name" id="name" />
                    </p>
                    <p class="email">
                        <input name="email" type="email" required class="feedback-input" id="email" placeholder="Email" />
                    </p>
                    <p class="text">
                        <textarea name="message" class="feedback-input" id="comment" placeholder="Message"></textarea>
                    </p>
                    <div class="submit">
                        <button type="submit" class="button-blue">Submit</button>
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
            
             <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js'></script><script  src="src/script.js"></script>  
         </div>
         <div class="footer">
             <a href="about.html">About Us</a>
             |
             <a href="contact.html">Contact Us</a>
             |
             <a href="#">Privacy Policy</a>
         </div>
    </div>
    
</body>
</html>
